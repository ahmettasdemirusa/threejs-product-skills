---
name: 3d-asset-optimization
description: Optimize 3D models (glTF/GLB) for the web so product pages load fast on phones. Covers mesh compression (Meshopt, Draco), texture compression (KTX2, WebP, AVIF), resizing, simplification, validation and size budgets with the glTF-Transform CLI. Use when a GLB/glTF file is too large or slow, the user asks to compress, optimize, shrink or convert a 3D model, when converting from FBX/OBJ/Blender for the web, or when setting up a 3D asset pipeline.
license: MIT
metadata:
  version: 1.0.0
  author: Ahmet Tasdemir
---

# 3D Asset Optimization for the Web

Raw exports from CAD or Blender are often 20–200 MB. A product page needs **a few MB at most**. Optimize every model before it goes on a page, and keep the original as the source of truth.

## The tool: glTF-Transform

[glTF-Transform](https://gltf-transform.dev/) is a well-maintained CLI and library for glTF. One command covers most cases:

```bash
npx @gltf-transform/cli optimize input.glb output.glb --compress meshopt --texture-compress webp
```

`optimize` runs a sequence of cleanups:
- deduplication
- pruning of unused data
- instancing
- welding
- simplification, which you can tune
- resizing of textures, to a maximum of 2048 px by default
- geometry compression
- texture compression

Useful options:

| Option | Values | Notes |
|---|---|---|
| `--compress` | `meshopt` (default), `draco`, `quantize`, `false` | Geometry compression |
| `--texture-compress` | `auto` (default), `webp`, `avif`, `ktx2`, `false` | `ktx2` saves GPU memory; `webp` and `avif` save download size |
| `--texture-size` | number (default `2048`) | Maximum texture dimension |
| `--simplify` | `true` or `false` | Mesh simplification with meshoptimizer; tune with `--simplify-ratio` and `--simplify-error` |

### ⚠️ Configurable models: turn off joining and palettes

Two `optimize` steps are **on by default** and change the model's structure:

| Option | Default | What it does |
|---|---|---|
| `--join` | on | Merges meshes that share a material, to reduce draw calls |
| `--palette` | on | Can merge simple materials into one material with a palette texture |

That is fine for a static viewer. It **breaks configurators and hotspots** that find parts or materials by name.

Measured on this repo's demo mug (glTF-Transform 4.5.1):

| Command | Size | Meshes | Material names |
|---|---|---|---|
| Original export | 129 KB | 8 | kept |
| `optimize --compress meshopt --texture-compress webp` | 27 KB | **4**: parts merged | kept |
| the same plus `--palette false --join false` | 31.5 KB | 8 | kept |

For anything a script manipulates by name, use:

```bash
npx @gltf-transform/cli optimize input.glb output.glb --compress meshopt --texture-compress webp --palette false --join false
```

Run `npx @gltf-transform/cli optimize --help` to see the options of the installed version. Inspect a file with `npx @gltf-transform/cli inspect model.glb`: it lists meshes, materials, textures and their sizes.

## Choosing compression

| | Meshopt | Draco |
|---|---|---|
| Compression ratio | Good; better with gzip or brotli on the server | Usually smaller for dense meshes |
| Decode speed | Very fast | Slower; the decoder is a WASM download |
| Animations and morph targets | Supported | Geometry only |
| three.js | `loader.setMeshoptDecoder(MeshoptDecoder)` | `loader.setDRACOLoader(dracoLoader)` |

**Default to Meshopt** for product viewers. Use Draco when the file size is paramount and the mesh is static.

| Texture format | Choose when |
|---|---|
| **WebP** or **AVIF** | You want the smallest download and simple tooling |
| **KTX2** (Basis Universal) | GPU memory matters: textures stay compressed on the GPU. Best for large texture sets, many products on one page, or low-end phones. Needs `KTX2Loader` with `detectSupport(renderer)`. |

## Budgets for a single product

| Item | Target |
|---|---|
| File size (compressed) | ≤ 2–3 MB; under 1 MB is excellent |
| Triangles | ≲ 100k (simplify further if it doesn't show) |
| Textures | ≤ 2048² each; 1024² for small parts; as few as possible |
| Materials | As few as possible; merge where the look allows |
| Draw calls | ≲ 50 |

## Pipeline

1. **Export to glTF 2.0 (`.glb`)** from the source tool, e.g. Blender's File → Export → glTF 2.0.
   - Apply transforms.
   - Use metres.
   - Use +Y up (the exporter's default).
   - **Name materials deliberately.** Configurators depend on the names (product-configurator skill).
2. **Validate** with the Khronos glTF Validator, https://github.khronos.org/glTF-Validator/, or the `validate` command.
3. **Optimize** with glTF-Transform, as above.
4. **Compare** before and after in the viewer. Look for artifacts: seams from welding, blocky textures, lost detail. Loosen the settings if needed.
5. **Serve correctly:**
   - Set `Content-Type: model/gltf-binary` for `.glb`.
   - Use long cache lifetimes with versioned filenames.
   - Enable gzip or brotli (it also helps Meshopt).
   - Use HTTPS, and CORS headers if the model is on another origin.
6. **Keep the source** (`.blend`, the original `.glb`) in the repository or in storage. Never optimize an already optimized file repeatedly.

## CAD, FBX and OBJ sources

- **CAD** (STEP, SolidWorks) exports are extremely dense, with millions of triangles. Tessellate at a coarse setting, then simplify. Bake small details into normal maps.
- **FBX or OBJ:** import into Blender, check the materials (convert to Principled BSDF), and export as glTF.
- **Remove what shoppers never see:** interior parts, screws and hidden faces.

## Verify

- [ ] `inspect` shows the expected size, triangle count and texture sizes.
- [ ] The file loads in the product viewer with no console errors, including the Draco, Meshopt and KTX2 decoders.
- [ ] It looks the same as the original from normal viewing distances.
- [ ] It loads in under 2–3 s on a throttled "Fast 4G" connection in DevTools.
