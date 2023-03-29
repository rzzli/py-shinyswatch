#!/usr/bin/env python3

import json
import os
import shutil
import subprocess
import textwrap
from pathlib import Path
from typing import Dict, List

root_path = Path(__file__).parent.parent
lib_path = root_path / "shinyswatch"
bootswatch_path = lib_path / "bootswatch"
shutil.rmtree(bootswatch_path)

tag_map: Dict[str, str] = {}
theme_map: Dict[str, List[str]] = {}


def process_version(
    bs_ver: str = "5",
    tag: str = "latest",
    from_folder: str = "dist",
) -> None:
    # Download bootswatch package
    extra_args = ["--package-lock", "false", "--no-save", "--silent"]
    subprocess.run(["npm", "uninstall", "bootswatch", *extra_args])
    subprocess.run(["npm", "install", f"bootswatch@{tag}", *extra_args])
    version = (
        subprocess.run(["npm", "list", "bootswatch"], capture_output=True)
        .stdout.decode()
        .split("@")[1]
        .split(" ")[0]
    )

    # Copy files
    to_folder = bootswatch_path / bs_ver
    if to_folder.exists():
        shutil.rmtree(to_folder)
    os.makedirs(to_folder)
    os.rename(
        root_path / "node_modules/bootswatch" / from_folder,
        to_folder,
    )

    # Clean up
    shutil.rmtree(root_path / "node_modules")

    # Remove unnecessary files
    for theme in to_folder.iterdir():
        for f in theme.rglob("*"):
            if f.name.endswith(".min.css"):
                continue
            os.remove(f)

    # Save info
    tag_map[bs_ver] = version
    theme_map[bs_ver] = [f.name for f in to_folder.iterdir()]


process_version(
    "5",
    tag="latest",
    from_folder="dist",
)

theme_file = lib_path / "_themes.py"
if theme_file.exists():
    os.remove(theme_file)
with open(theme_file, "w", encoding="utf-8") as f:
    f.write(
        textwrap.dedent(
            """\
            # Do not edit this file, please dispatch GHA workflow `update-bootswatch.yaml`

            __all__ = ("versions", "themes", )

            versions = {}

            themes = {}
            """
        ).format(json.dumps(tag_map, indent=4), json.dumps(theme_map, indent=4))
    )
