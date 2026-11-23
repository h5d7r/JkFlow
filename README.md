![JkFlow](launcher/assets/sce_sys/pic1.png)

# JkFlow

Play your own PC copy of **Blur** on a PS4 with GoldHEN: offline career, split screen, and online races through AMAX.

[![release](https://img.shields.io/github/v/release/Salru13/JkFlow)](https://github.com/Salru13/JkFlow/releases/latest)
[![downloads](https://img.shields.io/github/downloads/Salru13/JkFlow/total?label=downloads)](https://github.com/Salru13/JkFlow/releases)
[![visits](https://hits.sh/github.com/Salru13/JkFlow.svg?label=visits)](https://hits.sh/github.com/Salru13/JkFlow/)
![platform](https://img.shields.io/badge/platform-PS4%20(GoldHEN)-0070d1)
![license](https://img.shields.io/badge/launcher-LGPL--2.1--or--later-blue)

JkFlow is a PS4 app with its own launcher, a Wine runtime for the console and a native DXVK renderer. You bring the game; JkFlow checks your Blur folder, installs what it needs and starts Blur. This repository holds the source of the launcher, the title integration, the Wine PS4 runtime (`wine/`) and the Mesa patch (`mesa/`) of JkFlow 1.00, and the licence texts shipped in the package. Player guide: [README-player.md](README-player.md).

## Requirements

- A PS4 with GoldHEN.
- A way to copy files to the PS4: FTP (GoldHEN has an FTP server), or a USB drive and a file manager app on the PS4.
- Your own copy of Blur (PC). It is not included.
- About 1 GB for JkFlow, plus your Blur game folder (about 8 GB).
- Internet only for online play.

## Download

`JkFlow-1.00.pkg` from [Releases](https://github.com/Salru13/JkFlow/releases). The release notes give its SHA-256.

## Getting started

1. Over FTP, create the folder `/data/JkFlow/Blur` and copy all your Blur files into it. `Blur.exe` must be directly in that folder.
2. Download `JkFlow-1.00.pkg` from [Releases](https://github.com/Salru13/JkFlow/releases), install it with GoldHEN and open JkFlow.
3. In JkFlow, open **Patch** and choose **Patch for offline play**, or **Patch for online play (AMAX)** to also download the AMAX online client.
4. Press **Play**.

### Offline patch or online patch

| | Patch for offline play | Patch for online play (AMAX) |
|---|---|---|
| Installs | Only the JkFlow files. Your own `Blur.exe` stays. | The JkFlow files, the AMAX online client and Blur 1.2, downloaded from amax-emu.com. Your own `Blur.exe` goes to the backup. |
| Internet | Not needed | Needed, or put the two zips in `/data/JkFlow` yourself (see FAQ) |
| Play | Career and split screen | Online, career and split screen |
| Races | 30 FPS; 60 FPS only if your `Blur.exe` is the verified Blur 1.2 | 30 FPS, or 60 FPS (PS4 Pro recommended) |
| Split screen | 30 FPS | 30 FPS |

A `Blur.exe` that JkFlow does not recognise always runs at 30 FPS, menus included. **Patch for offline play** puts your own `Blur.exe` back at any time.

### Online play

1. Create an account on the AMAX website: [amax-emu.com/how_to_play](https://amax-emu.com/how_to_play).
2. In JkFlow, open **Patch** and choose **Patch for online play (AMAX)**. It downloads the AMAX online client.
3. Open **Settings > Online account**, enter the **username** and **password** you created on the AMAX website and choose **Save**. JkFlow keeps them on the PS4 (the password in plain text, because AMAX needs it), and Blur signs in with them.
4. Press **Play** and choose online in Blur.

### Bring your save (optional)

Have a Blur save from a PC? On the PC it is in `%APPDATA%\Bizarre Creations\Blur\save`. Copy only the file `blursave` over FTP to `/data/JkFlow/System/import/blursave`, then open **Patch** and press Cross. Already patched? Just copy the save file and run **Patch** again.

- No save on the PS4 yet: it is imported.
- A save already on the PS4: JkFlow asks. **Keep** (the default) leaves your save as it is; **Use import** first backs up your current save, then imports.

The import is used once, then renamed so it is never applied twice. Only the save is imported, never Blur's settings.

### Settings

| Setting | What it does |
|---|---|
| **Frame rate** | 30 FPS (default, recommended for PS4 and PS4 Slim: races 30, menus 60) or 60 FPS (PS4 Pro with Boost Mode, verified Blur). Split screen always runs at 30 FPS. |
| **Show FPS / ms** | Shows the frame rate and frame time on screen while you race. |
| **Enable logs** | Writes detailed logs while you play. Off by default; turn it on only when something goes wrong. **clear logs** deletes them. |
| **Online account** | Your AMAX username and password for online play. **Remove account** deletes them. |
| **Save support bundle** | Collects the logs and your settings (never your account or saves) into `/data/JkFlow/Logs/support/<date-time>`. |

The full guide is [README-player.md](README-player.md).

## FAQ

### Offline patch or online patch: which one?

- **Patch for offline play** installs only the JkFlow files. Your own `Blur.exe` stays and no internet is needed. Career and split screen work.
- **Patch for online play (AMAX)** also downloads `amax_client_files.zip` and `blur_12.zip` from amax-emu.com, checks them and installs them. Your own `Blur.exe` and game data go to the backup. Online, career and split screen work.

Choose online if you want to play online, or if your `Blur.exe` is not verified and you want 60 FPS on a PS4 Pro. You can switch at any time: **Patch for offline play** removes the AMAX files and puts your own `Blur.exe` back. On the Patch screen, pressing Triangle twice puts back every file Patch changed.

### 30 FPS or 60 FPS?

Choose it in **Settings > Frame rate**.

- **30 FPS** (default, recommended for PS4 and PS4 Slim): races run at a steady 30 FPS, menus at 60.
- **60 FPS**: races run at up to 60 FPS. Made for a PS4 Pro with Boost Mode on (PS4 Settings > System > Boost Mode). It may work on other models, but races can be less stable.

Split screen always runs at 30 FPS, in every mode.

### What is a "verified" Blur.exe?

JkFlow is tested with one `Blur.exe`: Blur 1.2. It recognises that file by its size and SHA-256 hash. Any other `Blur.exe` (for example a retail or Steam copy) still runs, but always at 30 FPS, menus included, and 60 FPS cannot be selected.

To get the verified exe, run **Patch for online play (AMAX)** once: it installs Blur 1.2 from `blur_12.zip`. After that you can turn on 60 FPS (PS4 Pro). **Patch for offline play** puts your own `Blur.exe` back, and with it the 30 FPS limit.

### How do I play online (AMAX)?

1. Create an account on [amax-emu.com/how_to_play](https://amax-emu.com/how_to_play).
2. Run **Patch for online play (AMAX)**.
3. Open **Settings > Online account**, enter the AMAX username and password (1 to 31 plain characters, no accents) and choose **Save**.
4. Press **Play** and choose online in Blur.

The account is stored on the PS4 in `/data/JkFlow/System/state/account.cfg`. The password is saved **in plain text**, because AMAX needs it that way. It is sent only to the AMAX servers, never written to logs and never put in a support bundle. At Play, JkFlow hands it to the AMAX client through a small file in the Blur folder, which is deleted once it has been read. **Remove account** deletes both.

AMAX refuses logins when the PS4 clock is more than 30 minutes off: set the date and time first (see below).

### Logs and the support bundle

- **Enable logs** is off by default. Turn it on only when something goes wrong: it writes detailed game logs while you play.
- A few small logs are always written (start and session events, runtime errors). Old ones are rotated automatically; **Enable logs > clear logs** deletes them.
- **Settings > Save support bundle** (or Square on the "blur didn't start" screen) collects the logs and your settings into `/data/JkFlow/Logs/support/<date-time>`. Copy that folder to a PC over FTP. Your AMAX account, your saves, your PS4 user name and LAN addresses are not included.
- JkFlow has no contact address; see [Support](#support).

### How do I get back to JkFlow?

Quit Blur from its own main menu. You come back to JkFlow.

### Split screen

Sign in each player on the PS4 first (every controller needs a signed-in user), then press **Play**. Split screen runs at 30 FPS.

### "The PS4 date and time are wrong"

The online download and AMAX login need the right time. Use **Sync the time in GoldHEN**, or set it in PS4 Settings > Date and Time.

### No internet on the PS4

Offline play works without internet. For online play, on a computer download `amax_client_files.zip` and `blur_12.zip` from amax-emu.com (How to play). **Do not unzip them.** Copy both into `/data/JkFlow` (next to the `Blur` folder) over FTP, then run **Patch for online play (AMAX)**.

### Where are my saves and settings? What happens if I uninstall?

Everything JkFlow keeps is in `/data/JkFlow`: your `Blur` folder, `System` (settings, account, saves, backups) and `Logs`. Uninstalling, reinstalling or updating JkFlow does not touch it. Deleting `/data/JkFlow` deletes your saves, your AMAX account and your settings.

### Can I use a USB drive?

Yes, to copy the files. Use a file manager app on the PS4 to copy them from the USB drive into `/data/JkFlow/...`, or copy them over FTP. JkFlow does not run the game from the USB drive: your Blur folder must be in `/data/JkFlow/Blur`.

### Can I bring my PC save?

Yes, see [Bring your save](#bring-your-save-optional).

To take it back to a PC, copy `/data/JkFlow/System/prefix/drive_c/users/BLUR/AppData/Roaming/Bizarre Creations/Blur/save/blursave` over FTP (keep a copy of the PC's own `blursave` first).

## Support

JkFlow has no contact address. If something goes wrong:

1. Read the [FAQ](#faq) and Help in JkFlow (Square on the Start or Patch screen).
2. Make a support bundle (**Settings > Save support bundle**) and copy its folder to a PC over FTP.
3. Open an issue on [GitHub Issues](https://github.com/Salru13/JkFlow/issues): say what you did and what you saw (the error code, if any), and attach the support bundle files. Never share your AMAX password.

## Repository layout

| Path | What |
|---|---|
| `launcher/` | The JkFlow launcher UI: Start carousel, Patch, settings, help, its own on-screen keyboard and the loader shown while the game starts. It calls no PS4 API; the title plugs it in through a table of service callbacks (`bl_frontend_run`). |
| `title/` | The title integration: `prepare_blur100.py` prepares the title tree and applies `r1/title-r1.patch`, `prod-audit/title-prod.patch` and `title-blur100.patch`; the post-link cleans, `make_package_inputs.sh` and the title host tests. See [title/README.md](title/README.md). |
| `wine/` | The Wine PS4 runtime source and the title base (patches against the upstream commits, build scripts, every `win/wine` file with its hash). See [wine/README.md](wine/README.md). |
| `mesa/` | Our PS4 window-system patch for Mesa (MIT). See [mesa/README.md](mesa/README.md). |
| `LICENSE`, `THIRD_PARTY.md`, `SOURCES.txt`, `LICENSES/` | The licence texts shipped in the package. |

### Launcher

| Path | What |
|---|---|
| `launcher/src/bl_ui.h/.c` | Software renderer: glass cards and panels, pills, light trails, glow, additive logo, text, background. Frame format BGRX. |
| `launcher/tools/bake_assets.sh` | Generates `bl_font.h`, `bl_font_data.c` (Nunito glyph atlases) and `bl_logo.c` into a build directory. The outputs are not committed. |
| `launcher/tools/bake_font.c` | FreeType-based atlas baker. Nunito is a variable font: Black = weight 900, ExtraBold = weight 800. |
| `launcher/tools/make_art.c` | Draws JkFlow's own artwork (typographic wordmark in Nunito, "PS4", neon streaks): `launcher/assets/sce_sys/icon0.png`, `pic0.png`, `pic1.png`; and `logo.png` (on black), installed as `launcher/assets/logo/blur-icon0.png`. No official Blur artwork is used. |
| `launcher/tools/bake_logo.py` | Crops the wordmark out of `launcher/assets/logo/blur-icon0.png`, with feathered edges. |
| `launcher/tools/make_manifest.py` | Writes the Patch manifest of the package's `blur-files`. |
| `launcher/tools/scan_names.py` | Name and path scanner for package trees. Private names (for example build-host account names) are read from a file given with `--private` or `SCAN_NAMES_PRIVATE`; `launcher/tools/scan-names-private.example` is an empty example. |
| `launcher/assets/font/` | Nunito, SIL OFL 1.1 (`OFL.txt`). Downloaded from `github.com/google/fonts` `ofl/nunito` on 2026-11-13. `Nunito-VF.ttf` sha256 `bb55a5ca5c2042335b3991af27c4d0705d0ef41cac6164ac737fd8f2a1e85207`, `Nunito-Italic-VF.ttf` sha256 `b520cc871868b0acfca1beda875df7f4a44ebce914f8a89f83977fc9c09529c8`. |
| `launcher/assets/blur-files/` | Files Patch installs into the player's Blur folder: `model-base.ini` and the account plugin for the online overlay. |
| `launcher/tests/run.sh` | Builds the assets and runs every `launcher/tests/test_*.c` with ASan and UBSan, then the `test_*.sh` checks (Linux). The screen tests compare rendered frames with `launcher/tests/golden/*.sha256`. |
| `launcher/tests/preview_ui.c` | Writes PNG previews of the primitives. |

## Building

Launcher tests (Linux; Ubuntu 24.04 tested):

```bash
sudo apt install build-essential python3 libfreetype-dev
bash launcher/tests/run.sh
```

Needs a C compiler with ASan/UBSan, Python 3 and FreeType. `FREETYPE_INCLUDE`
(default `/usr/include/freetype2`) names the FreeType headers and
`FREETYPE_LIB` (default `/usr/lib/x86_64-linux-gnu/libfreetype.so.6`) the
library (see `launcher/tools/bake_assets.sh`). The screen goldens were made with
FreeType 2.13.

The title build is described in [title/README.md](title/README.md), the Wine PS4 runtime in [wine/README.md](wine/README.md) and [wine/BUILD.md](wine/BUILD.md) (including its known gaps), the Mesa patch in [mesa/README.md](mesa/README.md).

The release `.pkg` is built by [`.github/workflows/build-pkg.yml`](.github/workflows/build-pkg.yml) with no manual input: it finds a `jkflow-build-root*.tar.zst` release asset on its own, derives the version from the tag and attaches the package to the release. Without a build root it repacks the newest published `JkFlow-*.pkg` instead, so the workflow always produces a package. The file's header lists the build-root folders it expects.

## Licence

- The JkFlow launcher, the title integration and the build scripts in this repository are LGPL-2.1-or-later ([LICENSE](LICENSE), [LICENSES/LGPL-2.1.txt](LICENSES/LGPL-2.1.txt)). Unless a file says otherwise, everything in this repository is LGPL-2.1-or-later.
- The Wine PS4 runtime keeps Wine's LGPL-2.1-or-later; where its source comes from is in [SOURCES.txt](SOURCES.txt), and what is not yet complete is listed under "Gaps" in [wine/BUILD.md](wine/BUILD.md).
- Native DXVK (our changes in `dxvknative.prx` and `d3d9.c988.dll`) is free to use with the credit line **"Native DXVK by XxXJoker13XxX"** ([LICENSES/JkFlow-Native-DXVK.txt](LICENSES/JkFlow-Native-DXVK.txt)). Its source is not published. The DXVK base stays zlib/libpng.
- The V7 and S7 DLLs are separate files, all rights reserved, and are not in this repository.
- Third-party components: [THIRD_PARTY.md](THIRD_PARTY.md).

## Credits

- [orbis-win](https://github.com/plastikman/orbis-win) and the PS4 Wine port by [plastikman](https://github.com/plastikman). JkFlow's Wine runtime is built from them.
- The original Wine console port by [mpereiraesaa](https://github.com/mpereiraesaa).
- [orbis-compat](https://github.com/orbis-ports/orbis-compat) by Mikołaj Mikołajczyk, the [OpenOrbis](https://github.com/OpenOrbis) toolchain and the [orbis-porting-kit](https://github.com/orbis-ports/orbis-porting-kit) SDK.
- Wine, Mesa/RADV, [DXVK](https://github.com/doitsujin/dxvk) (Philip Rebohle, Joshua Ashton), LLVM and FreeType: the stack underneath. The launcher font is Nunito.
- Online play: the AMAX client and community servers by the AMAX team ([amax-emu.com](https://amax-emu.com)), downloaded by the player.
- The JkFlow launcher, Native DXVK, the V7 frame pacer and the S7 shader fixes by XxXJoker13XxX.

## Disclaimer

JkFlow is an unofficial fan project. It is not affiliated with or endorsed by Activision, Bizarre Creations, AMAX or Sony Interactive Entertainment. Blur is a trademark of Activision; PlayStation and PS4 are trademarks of Sony Interactive Entertainment. JkFlow contains no game files: use only a copy of Blur you own. Homebrew on a PS4 is at your own risk.
