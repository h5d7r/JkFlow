# JkFlow title integration

The JkFlow 1.00 title (title ID BLUR00001) is the relocatable Wine PS4 app
(`eboot.bin` + `sce_module/relocated_wine_app.prx`) with the JkFlow launcher
linked in. This folder holds the recipe that prepares the title tree, the
post-link cleans and the package-input script.

## Where the title source comes from

1. The two upstream console-port commits named in `wine/UPSTREAM.md`.
2. `wine/patches/title-base/0001-title-base.patch` (`wine/patches/series.txt`,
   part 4): the base title tree `native298-package277`. Its build entry is
   `wine/build/title/build-launcher-base.sh.example`. One file of that tree,
   the Blur logo bitmap `src/pw_blur_logo.h` (Activision artwork),
   is not published; the series names it with its hash. The JkFlow title
   does not use it: `title-blur100.patch` removes its only user (an
   uncalled start page), so the title prx holds no copy of the bitmap.
3. `r1/title-r1.patch`, `prod-audit/title-prod.patch` and
   `title-blur100.patch` of this folder, applied by `prepare_blur100.py r4`,
   with the launcher sources of `launcher/`.

## Files

| File | What |
|---|---|
| `prepare_blur100.py` | Prepares the title tree in the build root: copies the small source folders of the base tree, links the rest, sets the title IDs, copies `launcher/src` and the baked launcher files (`launcher/build/gen`), applies `r1/title-r1.patch`, `prod-audit/title-prod.patch` and `title-blur100.patch` and checks every patched file against its SHA-256. The build script it writes ends with `postlink_clean.py run`. |
| `title-blur100.patch`, `r1/title-r1.patch`, `prod-audit/title-prod.patch` | The title source changes, applied in that order (r1, then prod-audit, then blur100). |
| `postlink_clean.py` | Post-link clean of the title prx: build-host path prefixes and developer env-file names are replaced by equal-length neutral ones, with a byte-level proof against the build's own conversion. `selftest` runs on synthetic bytes. |
| `postlink-path-map.example` | Format of the build-host path map that `postlink_clean.py run`/`scan` read from `POSTLINK_PATH_MAP`. |
| `postlink_devpaths.py` | The same method for the Wine modules: developer switch paths are made unopenable (`/dev/null/...`). |
| `make_package_inputs.sh` | Collects the pinned package inputs (title, Wine modules, seed, launcher files, licence texts) into a delta folder and a composed view, and runs `launcher/tools/scan_names.py` over both with `scan-allow.txt`. |
| `make_pkg.sh` | Builds the fake-signed `.pkg` from the composed view: creates `sce_sys/param.sfo`, writes the `.gp4` and runs LibOrbisPkg's `PkgTool.Core pkg_build`/`pkg_validate`. |
| `make_gp4.py` | Writes the `.gp4` for an arbitrary package tree (all directories declared), which the OpenOrbis `create-gp4` cannot do because of its fixed `sce_sys`/`sce_module`/`assets` root. |
| `scan-allow.txt` | The approved exceptions for the name scan, each with its reason. |
| `tests/run_title_tests.sh` | Host tests of the title sources against a prepared tree. |

## Steps (Linux)

```bash
export JKFLOW_BUILD_ROOT=<build root>          # holds native298-package277 (see above) and the engine seed
bash launcher/tests/run.sh                      # bakes launcher/build/gen and runs the launcher tests
python3 -I title/prepare_blur100.py r4          # -> $JKFLOW_BUILD_ROOT/blur-launcher-r4
export POSTLINK_PATH_MAP=<path map file>        # see title/postlink-path-map.example
bash "$JKFLOW_BUILD_ROOT/blur-launcher-r4/build-launcher.sh"
bash title/tests/run_title_tests.sh "$JKFLOW_BUILD_ROOT/blur-launcher-r4"
JKFLOW_STATE_CACHE=<dxvk-native.dxvk-cache> AMAX_ZIP=<amax_client_files.zip> BLUR12_ZIP=<blur_12.zip> \
    bash title/make_package_inputs.sh
PS4_PKGTOOL=<PkgTool.Core or PkgTool.Core.dll> \
    bash title/make_pkg.sh "$JKFLOW_BUILD_ROOT/blur-launcher-r4/package-view-1.00" out 01.00
```

`make_package_inputs.sh` only hashes the two zips (to make sure no AMAX or
Activision file is shipped); it never copies them. The title's build entry
is described in `wine/BUILD.md` ("Title build entry"), the Wine PS4 runtime
in `wine/README.md`. `.github/workflows/build-pkg.yml` runs the same steps
from a prebuilt build-root artifact; its header lists the expected folders.
