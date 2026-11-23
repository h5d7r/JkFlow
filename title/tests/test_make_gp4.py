#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-2.1-or-later
# Copyright 2026 XxXJoker13XxX and contributors
"""Host test for title/make_gp4.py (no PkgTool.Core needed).

Creates a small package tree, writes the .gp4, and checks the two things
LibOrbisPkg's PfsProperties.BuildFSTree requires: every file is listed and
every ancestor directory is declared, so FindDir cannot fail.
"""
import os
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "make_gp4.py"
CONTENT_ID = "IV0000-BLUR00001_00-JKFLOW1000000000"


def declared_dirs(rootdir):
    out = set()

    def walk(node, prefix):
        for d in node.findall("dir"):
            name = d.get("targ_name")
            path = prefix + name
            out.add(path)
            walk(d, path + "/")

    walk(rootdir, "")
    return out


class MakeGp4Test(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "pkg"
        files = [
            "eboot.bin",
            "sce_sys/param.sfo",
            "sce_sys/icon0.png",
            "sce_module/libc.prx",
            "sce_module/sub/extra.prx",
            "win/wine/lib/wine/x86_64-windows/winevulkan.dll",
            "seed245/blur-native248/seed.idx",
            "LICENSES/Wine-LICENSE.txt",
            "SHA256SUMS",
            "SIZES",
            "REMOVE.txt",
        ]
        for rel in files:
            p = self.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"x")
        self.gp4 = self.root / "pkg.gp4"

    def tearDown(self):
        self.tmp.cleanup()

    def run_make(self, *extra, content_id=CONTENT_ID):
        return subprocess.run(
            [sys.executable, "-I", str(SCRIPT), str(self.root), str(self.gp4),
             "--content-id", content_id, "--volume-ts", "2026-11-23 12:00:00",
             *extra],
            capture_output=True, text=True)

    def test_tree_and_excludes(self):
        r = self.run_make("--exclude", "SHA256SUMS", "--exclude", "SIZES",
                          "--exclude", "REMOVE.txt")
        self.assertEqual(r.returncode, 0, r.stderr)
        project = ET.parse(self.gp4).getroot()
        self.assertEqual(project.get("fmt"), "gp4")
        self.assertEqual(project.get("version"), "1000")

        files = {f.get("targ_path") for f in project.find("files").findall("file")}
        self.assertIn("eboot.bin", files)
        self.assertIn("win/wine/lib/wine/x86_64-windows/winevulkan.dll", files)
        self.assertNotIn("pkg.gp4", files)
        for meta in ("SHA256SUMS", "SIZES", "REMOVE.txt"):
            self.assertNotIn(meta, files)

        dirs = declared_dirs(project.find("rootdir"))
        needed = {f.rsplit("/", 1)[0] for f in files if "/" in f}
        self.assertEqual(needed - dirs, set(),
                         "undeclared ancestor directories: %s" % (needed - dirs))
        self.assertIn("win/wine/lib/wine/x86_64-windows", dirs)

        package = project.find("volume/package")
        self.assertEqual(package.get("content_id"), CONTENT_ID)
        self.assertEqual(package.get("passcode"), "0" * 32)

    def test_rejects_bad_content_id(self):
        r = self.run_make(content_id="IV0000-BLUR00001_00-short")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("bad content id", r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
