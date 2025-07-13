# Arcade iPA Patcher

This script patches iPA files for Apple Arcade apps by modifying the `Info.plist` and injecting sideloading bypass tweaks using `cyan`.

## Purpose

- Sets `NSApplicationRequiresArcade` to `false` in the `Info.plist`.
- Injects bypass `.dylib` tweaks into the iPA using `cyan` to fix crashes (might not work for every game).

## Requirements

- Python 3.x
- `cyan` installed and in your PATH
- A folder containing the required `.dylib` tweak files (included in this repository)

## Tweak Folder

If you're always using the same tweak folder, edit the `tweakFolder` variable directly in the script to avoid entering it every time
Provide the path to either a single `.ipa` file or a folder containing multiple `.ipa` files.
Optionally provide an output folder (leave empty to use the default location next to the input).

git clone https://github.com/binnichtaktiv/arcadePatcher
# or
Download ZIP → extract → use the tweak folder path

