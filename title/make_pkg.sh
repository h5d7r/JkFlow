#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-2.1-or-later
# Copyright 2026 XxXJoker13XxX and contributors
#
# Build a fake-signed PS4 .pkg from the composed package view that
# title/make_package_inputs.sh writes.
#
#   PS4_PKGTOOL=<PkgTool.Core or PkgTool.Core.dll> \
#   bash title/make_pkg.sh <package-view> <out-dir> [APP_VER]
#
# APP_VER defaults to 01.00. The output is <out-dir>/JkFlow-<APP_VER>.pkg and
# its .sha256. Env:
#   TITLE_ID       default BLUR00001
#   TITLE          default JkFlow
#   CONTENT_ID     full 36-char id; default IV0000-<TITLE_ID>_00-<CONTENT_LABEL>
#   CONTENT_LABEL  default JKFLOW1000000000 (padded/trimmed to 16 chars)
#   PKG_NAME_VERSION  version in the output file name; default APP_VER
#                  (the release passes 1.00 while APP_VER is 01.00)
#   PS4_PKGTOOL    PkgTool.Core binary or .dll; otherwise
#                  $OO_PS4_TOOLCHAIN/bin/linux/PkgTool.Core is used
#
# The view holds the order-284 package with the JkFlow 1.00 delta on top and
# the order-284 leftovers removed (REMOVE.txt), so it is the package payload:
# eboot.bin, sce_sys/, sce_module/, win/, seed245/, blur-files/, LICENSES/
# and the licence texts. SHA256SUMS, SIZES and REMOVE.txt describe the delta
# and are not shipped inside the pkg.
set -euo pipefail

die() { echo "make_pkg: $*" >&2; exit 1; }

view="${1:?usage: make_pkg.sh <package-view> <out-dir> [APP_VER]}"
out_arg="${2:?usage: make_pkg.sh <package-view> <out-dir> [APP_VER]}"
version="${3:-01.00}"

[[ -d "$view" ]] || die "no package view: $view"
[[ -f "$view/eboot.bin" ]] || die "no eboot.bin in $view"

TITLE_ID="${TITLE_ID:-BLUR00001}"
TITLE="${TITLE:-JkFlow}"
[[ "$TITLE_ID" =~ ^[A-Z]{4}[0-9]{5}$ ]] || die "TITLE_ID must be AAAA00000, got '$TITLE_ID'"

label="${CONTENT_LABEL:-JKFLOW1000000000}"
label="${label^^}"
label="${label//[^A-Z0-9]/}"
label="${label}0000000000000000"
label="${label:0:16}"
content_id="${CONTENT_ID:-IV0000-${TITLE_ID}_00-${label}}"
[[ "$content_id" =~ ^[A-Z]{2}[0-9]{4}-[A-Z]{4}[0-9]{5}_00-[A-Z0-9]{16}$ ]] \
  || die "bad content id '$content_id'"

pkgtool="${PS4_PKGTOOL:-}"
if [[ -z "$pkgtool" && -n "${OO_PS4_TOOLCHAIN:-}" ]]; then
  for c in "$OO_PS4_TOOLCHAIN/bin/linux/PkgTool.Core" \
           "$OO_PS4_TOOLCHAIN/bin/macos/PkgTool.Core"; do
    [[ -f "$c" ]] && { pkgtool="$c"; break; }
  done
fi
[[ -n "$pkgtool" ]] || die "set PS4_PKGTOOL to PkgTool.Core (or OO_PS4_TOOLCHAIN)"
if [[ "$pkgtool" == *.dll ]]; then
  [[ -f "$pkgtool" ]] || die "no PkgTool.Core at $pkgtool"
  run_pkgtool() { dotnet "$pkgtool" "$@"; }
elif [[ -x "$pkgtool" ]]; then
  run_pkgtool() { "$pkgtool" "$@"; }
else
  die "PkgTool.Core is not executable: $pkgtool"
fi

mkdir -p "$out_arg"
out="$(cd "$out_arg" && pwd)"
stage="$out/.stage"
rm -rf "$stage"
mkdir -p "$stage"

# The composed view: symlinks into the delta folder and the order-284 package.
cp -a "$view/." "$stage/"
rm -f "$stage/SHA256SUMS" "$stage/SIZES" "$stage/REMOVE.txt"

# param.sfo (the order-284 input has none; the title's SFO is built here).
sfo="$stage/sce_sys/param.sfo"
mkdir -p "$stage/sce_sys"
rm -f "$sfo"
run_pkgtool sfo_new "$sfo" >/dev/null
sfo_set() { run_pkgtool sfo_setentry "$sfo" "$1" --type "$2" --maxsize "$3" --value "$4" >/dev/null; }
sfo_set APP_TYPE           Integer 4   1
sfo_set APP_VER            Utf8    8   "$version"
sfo_set ATTRIBUTE          Integer 4   0
sfo_set CATEGORY           Utf8    4   gd
sfo_set CONTENT_ID         Utf8    48  "$content_id"
sfo_set DOWNLOAD_DATA_SIZE Integer 4   0
sfo_set SYSTEM_VER         Integer 4   0
sfo_set TITLE              Utf8    128 "$TITLE"
sfo_set TITLE_ID           Utf8    12  "$TITLE_ID"
sfo_set VERSION            Utf8    8   "$version"

# LibOrbisPkg needs the full directory tree; create-gp4 only knows its own
# fixed sce_sys/sce_module/assets layout.
python3 -I "$(dirname "$0")/make_gp4.py" "$stage" "$stage/pkg.gp4" \
  --content-id "$content_id" \
  --exclude SHA256SUMS --exclude SIZES --exclude REMOVE.txt --exclude pkg.gp4

run_pkgtool pkg_build "$stage/pkg.gp4" "$out" >"$out/pkg-build.log" 2>&1 || {
  cat "$out/pkg-build.log" >&2
  die "PkgTool.Core pkg_build failed"
}

built="$out/$content_id.pkg"
[[ -f "$built" ]] || {
  sed -n '1,40p' "$out/pkg-build.log" >&2 || true
  die "PkgTool.Core produced no $content_id.pkg"
}

pkg="$out/JkFlow-${PKG_NAME_VERSION:-$version}.pkg"
mv -f "$built" "$pkg"
name="$(basename "$pkg")"
( cd "$out" && sha256sum "$name" > "$name.sha256" )

run_pkgtool pkg_validate "$pkg"
echo "make_pkg: $pkg ($(du -h "$pkg" | cut -f1))"
cat "$out/$name.sha256"
