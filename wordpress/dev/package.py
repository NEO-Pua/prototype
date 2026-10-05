# -*- coding: utf-8 -*-
"""
Make the two files the developers upload in the WordPress admin:

  wordpress/dist/hanajirushi.zip       外観 → テーマ → 新規追加 → テーマのアップロード
  wordpress/dist/hanajirushi-core.zip  プラグイン → 新規追加 → プラグインのアップロード
  wordpress/dist/blueprint-zip.json    local test site that installs the two zips

Run:  python wordpress/dev/package.py   (runs sync.py first, so the zips match the mockup)

Each zip holds one folder named like the theme / plugin, as WordPress expects.
"""
import json, os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
WP = os.path.dirname(HERE)
DIST = os.path.join(WP, "dist")
SKIP_DIRS = {"__pycache__", ".git"}
SKIP_FILES = {"Thumbs.db", "Desktop.ini", ".DS_Store"}


def pack(name):
    src = os.path.join(WP, name)
    out = os.path.join(DIST, name + ".zip")
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(src):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for f in sorted(files):
                if f in SKIP_FILES:
                    continue
                full = os.path.join(root, f)
                z.write(full, os.path.join(name, os.path.relpath(full, src)).replace(os.sep, "/"))
                n += 1
    print(f"{os.path.relpath(out, WP)}  {n} files  {os.path.getsize(out) // 1024} KB")


def main():
    sys.path.insert(0, HERE)
    import sync
    sync.main()
    os.makedirs(DIST, exist_ok=True)
    pack("hanajirushi")
    pack("hanajirushi-core")
    zip_blueprint()


def zip_blueprint():
    """dist/blueprint-zip.json: the local test site, installing the two zips the way the admin
    upload does (instead of the folders). Playground reads files next to the blueprint only."""
    with open(os.path.join(HERE, "blueprint.json"), encoding="utf-8") as fh:
        bp = json.load(fh)
    steps = [s for s in bp["steps"] if s["step"] not in ("activatePlugin", "activateTheme")]
    at = next(i for i, s in enumerate(steps) if s["step"] == "runPHP")
    steps[at:at] = [
        {"step": "installPlugin", "pluginData": {"resource": "bundled", "path": "hanajirushi-core.zip"}, "options": {"activate": True}},
        {"step": "installTheme", "themeData": {"resource": "bundled", "path": "hanajirushi.zip"}, "options": {"activate": True}},
    ]
    bp["steps"] = steps
    with open(os.path.join(DIST, "blueprint-zip.json"), "w", encoding="utf-8") as fh:
        json.dump(bp, fh, ensure_ascii=False, indent="	")


if __name__ == "__main__":
    main()
