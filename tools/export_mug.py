"""Export the demo mug to assets/mug.glb using headless Chrome and three.js' GLTFExporter.

    python tools/export_mug.py

MIT License, Ahmet Tasdemir.
"""
import base64
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "tools" / "export-mug.html"
OUT = ROOT / "assets" / "mug.glb"
CHROME = os.environ.get("CHROME", r"C:\Program Files\Google\Chrome\Application\chrome.exe")

cmd = [CHROME, "--headless=new", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
       "--virtual-time-budget=30000", "--dump-dom", PAGE.as_uri()]
dom = subprocess.run(cmd, capture_output=True, timeout=180).stdout.decode("utf-8", "replace")
if "@@GLB@@" not in dom:
    sys.exit("Export failed:\n" + dom[-1500:])
data = "".join(dom.split("@@GLB@@", 1)[1].split("@@END@@", 1)[0].split())
OUT.parent.mkdir(exist_ok=True)
OUT.write_bytes(base64.b64decode(data))
print("wrote %s (%.1f KB)" % (OUT.relative_to(ROOT), OUT.stat().st_size / 1024))
