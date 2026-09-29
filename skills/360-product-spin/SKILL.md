---
name: 360-product-spin
description: Add a 360° product spin (a draggable image sequence) to a product page, and produce the frames by photographing the product on a turntable or rendering a 3D model with three.js. Use when the user wants a 360 view, a spin or rotating product photos, "turn the product around", a 360 product viewer, sprite sheets for product rotation, or has product photos but no 3D model. Uses the zero-dependency Spin360 web component.
license: MIT
metadata:
  version: 1.0.0
  author: Ahmet Tasdemir
---

# 360° Product Spin

A 360° spin is a sequence of photos or renders, shown one at a time as the shopper drags. Compared with real-time 3D:

| | 360° spin | Real-time 3D |
|---|---|---|
| Source | Photos, or renders from a 3D model | A glTF model |
| Realism | **Photographic**: exactly what the camera saw | Depends on the model and materials |
| Shopper can | Turn it around one axis | Orbit freely, zoom, configure, AR |
| Weight | ~200–300 KB for 36 WebP frames | Model plus runtime; usually larger |
| Best for | Apparel, shoes, jewelry, food, anything with no good 3D model | Configurable products, furniture, AR |

Use a spin when the product is photographed rather than modeled, or when photographic realism matters more than interactivity.

## Embed with Spin360

[Spin360](https://github.com/ahmettasdemirusa/spin360) is a zero-dependency web component, under 5 KB gzipped:

```html
<script type="module" src="https://cdn.jsdelivr.net/gh/ahmettasdemirusa/spin360@v1.0.0/spin360.js"></script>

<spin-360 src="/images/mug/{i}.webp" frames="36" pad="2" alt="Ceramic mug, 360° view" autoplay></spin-360>
```

- `{i}` is replaced by the frame index, and `pad="2"` gives `00`–`35`.
- **Sprite sheet (one request):** `<spin-360 sprite="/images/mug-sprite.webp" frames="36" columns="6">`
- **Colorways:** change the `src` attribute; the current angle is kept.
- **Built in:** drag with inertia, keyboard control, lazy loading, and autoplay that respects reduced motion. It is an accessible slider.

Live demo: https://ahmettasdemirusa.github.io/spin360/

## Producing frames: photography

1. **Turntable:** a manual one with degree marks, or a motorized one that triggers the camera.
2. **Fix everything except the rotation:** the camera on a tripod, with manual exposure, focus and white balance, and constant lighting (no flash variation).
3. **Center the product** on the turntable's axis. Off-center products wobble in the spin.
4. **Shoot 24, 36 or 72 frames** at equal steps: 15°, 10° or 5°. 36 is the sweet spot for smoothness against weight.
5. **Batch-process identically:** the same crop, background removal and color correction, and the same output size. Name the files `00.webp` … `35.webp`.

## Producing frames: rendering from a 3D model

When a 3D model exists, render the frames instead. They come out perfectly consistent, and you can render every colorway without a photoshoot.

The Spin360 repo includes a working renderer: [`tools/render-frames.html`](https://github.com/ahmettasdemirusa/spin360/blob/main/tools/render-frames.html) plus [`tools/render.py`](https://github.com/ahmettasdemirusa/spin360/blob/main/tools/render.py). It:

1. builds or loads the model in three.js, with studio lighting and a shadow
2. rotates it by `360 / frames` degrees per frame, rendering each one to a canvas
3. runs in **headless Chrome** (software WebGL via `--use-angle=swiftshader`) and reads the frames from `--dump-dom`
4. writes WebP frames and a sprite sheet with Pillow

Two lessons from building it:

- **Keep each `--dump-dom` output small.** Output of several megabytes was unreliable in testing. Render about 12 WebP frames per run, not 36 PNGs at once.
- **Use delimiters that can't appear in base64,** e.g. `@@FRAMES@@`. A marker like `END` can occur inside base64 data by chance and silently cut a frame.

To adapt it to a real product, replace the procedural mug with `GLTFLoader` loading your `.glb` (see the threejs-product-viewer skill), and keep the camera fixed while you rotate the model.

## Sizes and formats

- **Frames:** 600–1000 px on the long edge. Serve 2× only when it will be shown large on desktop.
- **Format:** WebP at quality 75–85 (AVIF is smaller, but slower to encode). 36 frames of a 600 px product come to about 200–250 KB.
- **Sprite sheet or separate files:** a sprite is one request and loads atomically. Separate files let the first frame appear sooner, and Spin360 loads the visible frame first.

## Verify

- [ ] The spin is smooth, with no jumps between the last and first frame (frame 36 must not duplicate frame 0).
- [ ] The product stays centered; there is no wobble.
- [ ] Exposure and color are identical across all frames.
- [ ] It works with touch on a phone, and vertical scrolling still scrolls the page.
- [ ] The `alt` text describes the product.
