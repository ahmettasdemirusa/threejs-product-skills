# Three.js Product Skills: instructions for AI agents

This repository contains Agent Skills for building 3D product experiences on the web. Each folder in `skills/` holds a `SKILL.md` (YAML frontmatter plus instructions), and some also hold tested templates.

| Task | Read first |
|---|---|
| 3D product viewer with three.js, a GLB/glTF on a web page | `skills/threejs-product-viewer/SKILL.md` + `templates/product-viewer.html` |
| Color, material or variant picker on a 3D model; configurator | `skills/product-configurator/SKILL.md` + `templates/configurator.html` |
| Model too large or slow; compress or convert a glTF | `skills/3d-asset-optimization/SKILL.md` |
| Simple embed with AR (iOS Quick Look, Android Scene Viewer, WebXR) | `skills/model-viewer-ar/SKILL.md` |
| 360° spin from photos or renders | `skills/360-product-spin/SKILL.md` |

Ground rules:

- **Start from the templates,** and keep one pinned three.js version for the core and the addons.
- **Test in a real browser over HTTP,** not `file://`, and check the console before reporting success.
- **Never hard-code the camera to one model;** frame from the bounding box.
- **Render on demand,** and cap the pixel ratio at 2.
- **Keep material and mesh names** when optimizing models that scripts manipulate: use `--palette false --join false` with glTF-Transform.
