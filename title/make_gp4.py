#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-2.1-or-later
# Copyright 2026 XxXJoker13XxX and contributors
"""Write the .gp4 project that LibOrbisPkg's `PkgTool.Core pkg_build` needs.

    make_gp4.py ROOT OUTPUT.gp4 --content-id IV0000-BLUR00001_00-JKFLOW1000000000
                [--volume-ts "2026-11-23 12:00:00"] [--exclude PATH]...

ROOT is the staged package tree (eboot.bin, sce_sys/, sce_module/, win/,
seed245/, ...).  Every regular file becomes a <file> entry with orig_path
relative to ROOT, and every directory that holds one is declared in
<rootdir>; LibOrbisPkg resolves targ_path against that declared tree and dies
in FindDir if an ancestor is missing (which is why create-gp4's fixed
sce_sys/sce_module/assets tree cannot be used for the JkFlow layout).

The project is the `pkg_ps4_app` shape from the OpenOrbis samples: one PlayGo
chunk and one scenario, passcode all zeroes (fake PKG), no entitlement key.
"""
import argparse
import datetime
import os
import sys
from xml.sax.saxutils import quoteattr

CONTENT_ID_RE = r"^[A-Z]{2}[0-9]{4}-[A-Z]{4}[0-9]{5}_00-[A-Z0-9]{16}$"


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    p.add_argument("root", help="staged package tree")
    p.add_argument("output", help=".gp4 file to write")
    p.add_argument("--content-id", required=True,
                   help="36-character content id (XX0000-AAAA00000_00-ZZZZZZZZZZZZZZZZ)")
    p.add_argument("--volume-ts", default=None,
                   help='volume timestamp "YYYY-MM-DD HH:MM:SS" (UTC; default now)')
    p.add_argument("--volume-id", default="PS4VOLUME")
    p.add_argument("--exclude", action="append", default=[],
                   help="relative path to leave out of the package (repeatable)")
    return p.parse_args()


def check_content_id(content_id):
    import re
    if not re.match(CONTENT_ID_RE, content_id):
        sys.exit("make_gp4: bad content id %r (want XX0000-AAAA00000_00-ZZZZZZZZZZZZZZZZ)"
                 % content_id)


def collect(root, excludes):
    """Return (sorted file paths, directory tree) for ROOT."""
    files = []
    tree = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir == ".":
            rel_dir = ""
        for name in sorted(filenames):
            rel = os.path.join(rel_dir, name) if rel_dir else name
            rel = rel.replace(os.sep, "/")
            if rel in excludes:
                continue
            files.append(rel)
            node = tree
            parts = rel.split("/")[:-1]
            for part in parts:
                node = node.setdefault(part, {})
    return files, tree


def write_tree(out, node, indent):
    for name in sorted(node):
        children = node[name]
        if children:
            out.append("%s<dir targ_name=%s>" % (indent, quoteattr(name)))
            write_tree(out, children, indent + "\t")
            out.append("%s</dir>" % indent)
        else:
            out.append("%s<dir targ_name=%s />" % (indent, quoteattr(name)))


def main():
    args = parse_args()
    check_content_id(args.content_id)

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        sys.exit("make_gp4: not a directory: %s" % root)
    if not os.path.isfile(os.path.join(root, "eboot.bin")):
        sys.exit("make_gp4: no eboot.bin in %s" % root)
    if not os.path.isfile(os.path.join(root, "sce_sys", "param.sfo")):
        sys.exit("make_gp4: no sce_sys/param.sfo in %s" % root)

    ts = args.volume_ts or datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S")

    excludes = set(args.exclude)
    out_abs = os.path.abspath(args.output)
    if out_abs.startswith(root + os.sep):
        excludes.add(os.path.relpath(out_abs, root).replace(os.sep, "/"))

    files, tree = collect(root, excludes)
    if not files:
        sys.exit("make_gp4: nothing to package in %s" % root)

    out = []
    out.append('<?xml version="1.0" encoding="utf-8"?>')
    out.append('<psproject fmt="gp4" version="1000">')
    out.append('  <volume>')
    out.append('    <volume_type>pkg_ps4_app</volume_type>')
    out.append('    <volume_id>%s</volume_id>' % args.volume_id)
    out.append('    <volume_ts>%s</volume_ts>' % ts)
    out.append('    <package content_id=%s passcode="00000000000000000000000000000000" '
               'storage_type="digital50" app_type="full" />' % quoteattr(args.content_id))
    out.append('    <chunk_info chunk_count="1" scenario_count="1">')
    out.append('      <chunks>')
    out.append('        <chunk id="0" layer_no="0" label="Chunk #0" />')
    out.append('      </chunks>')
    out.append('      <scenarios default_id="0">')
    out.append('        <scenario id="0" type="sp" initial_chunk_count="1" '
               'label="Scenario #0">0</scenario>')
    out.append('      </scenarios>')
    out.append('    </chunk_info>')
    out.append('  </volume>')
    out.append('  <files img_no="0">')
    for rel in files:
        out.append('    <file targ_path=%s orig_path=%s />' % (quoteattr(rel), quoteattr(rel)))
    out.append('  </files>')
    out.append('  <rootdir>')
    write_tree(out, tree, "\t")
    out.append('  </rootdir>')
    out.append('</psproject>')
    out.append('')

    with open(args.output, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))

    print("make_gp4: %s (%d files)" % (args.output, len(files)))


if __name__ == "__main__":
    main()
