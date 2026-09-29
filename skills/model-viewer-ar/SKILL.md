---
name: model-viewer-ar
description: Add a 3D product view with "view in your room" augmented reality to any website using Google's <model-viewer> web component. No three.js code is needed. Use when the user wants AR for products, "view in your space", Quick Look on iPhone, Scene Viewer on Android, a simple 3D embed for Shopify, WordPress or a static site, a 3D poster/lazy-loaded model, or material variants without a custom configurator. For fully custom scenes use threejs-product-viewer.
license: MIT
metadata:
  version: 1.0.0
  author: Ahmet Tasdemir
  model-viewer: "4.3.1"
---

# 3D and AR with `<model-viewer>`

[`<model-viewer>`](https://modelviewer.dev/) is Google's open-source web component for displaying glTF models, with AR on Android and iOS. It is the fastest route when the user needs **a good product view plus AR** rather than a custom 3D experience.

## Minimal embed

```html
<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js"></script>

<model-viewer
  src="/models/mug.glb"
  alt="Ceramic mug in tomato red"
  poster="/models/mug-poster.webp"
  camera-controls
  auto-rotate
  shadow-intensity="1"
  tone-mapping="neutral"
  environment-image="neutral"
  ar
  ar-modes="webxr scene-viewer quick-look"
  style="width: 100%; height: 480px;">
</model-viewer>
```

## Attributes that matter for products

| Attribute | Use |
|---|---|
| `src` | The `.glb`. Optimize it first (3d-asset-optimization skill). |
| `alt` | **Required for accessibility:** describe the product. |
| `poster` | An image shown until the model loads. Use a render of the default view, so the swap is invisible. |
| `loading="lazy"` / `reveal="manual"` | Defer loading below the fold, or until a "View in 3D" click. |
| `camera-controls`, `auto-rotate` | Let shoppers orbit; spin until they interact. |
| `tone-mapping="neutral"`, `environment-image="neutral"` | Color-accurate, studio-style lighting. |
| `shadow-intensity` | A soft contact shadow; `1` is a good default. |
| `ar`, `ar-modes` | Turn on AR. The modes are tried in order: WebXR, then Android Scene Viewer, then iOS Quick Look. |
| `ios-src` | An optional pre-made `.usdz` for iOS Quick Look. If it's missing, model-viewer generates a USDZ from the GLB on the fly. Supply your own for complex materials or for faster AR start. |
| `ar-placement="wall"` | For wall-mounted items (art, mirrors, cabinets, TVs). Floor is the default. |
| `ar-scale="fixed"` | Stop the shopper from resizing the product in AR, so it always shows at true size. |

## Real-world scale is everything in AR

AR shows the model at its **glTF size in metres**. A mug exported at 9.5 units appears 9.5 m tall. Check the model's dimensions before shipping, e.g. with `npx @gltf-transform/cli inspect model.glb`, or fix the scale in the source file. Don't fix it with CSS.

## Variants (colors and materials)

If the glTF contains `KHR_materials_variants`:

```html
<model-viewer id="mv" src="/models/chair.glb" camera-controls ar></model-viewer>
<select id="variant"></select>
<script type="module">
  const mv = document.querySelector('#mv');
  const select = document.querySelector('#variant');
  mv.addEventListener('load', () => {
    for (const name of mv.availableVariants) select.add(new Option(name, name));
  });
  select.addEventListener('change', () => { mv.variantName = select.value; });
</script>
```

For options the file doesn't contain as variants (arbitrary colors, prices, URL state), use the product-configurator skill with three.js.

## Custom AR button

```html
<model-viewer src="/models/mug.glb" ar ar-modes="webxr scene-viewer quick-look" camera-controls>
  <button slot="ar-button" class="ar-btn">View in your room</button>
</model-viewer>
```

The slotted button is shown only on devices that can start AR. Listen to `ar-status` events to track `session-started` and `failed`, e.g. for analytics.

## Platform notes

- **Android:** WebXR in Chrome, or Scene Viewer as a fallback.
- **iOS:** Quick Look through Safari, using the provided or generated USDZ.
- **Desktop:** no AR, just the 3D view. Don't show an AR button there; the slotted button handles this.
- **Serve over HTTPS.** Set the `model/gltf-binary` MIME type for `.glb` and `model/vnd.usdz+zip` for `.usdz`.

## Verify

1. The model looks right on desktop, and the poster matches the first view.
2. On an Android phone, AR opens, the product is at true size, and it sits on the floor or wall as intended.
3. On an iPhone, Quick Look opens, and the materials and scale are correct.
4. The page still works, and the `alt` text is present, when WebGL is unavailable.

Docs and examples: https://modelviewer.dev/
