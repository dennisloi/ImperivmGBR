

# Pak Tools

**Pak Tools** is a set of utilities for managing and manipulating `.pak` files used in the **Imperivm GBR** game. These `.pak` files function as archives that can store any type of file.

## File Structure

* The first **16 bytes** represent the file magic:

  ```
  "HMMSYS PackFile\n"
  ```

* This is followed by a constant 16-byte header:

  ```
  1A 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  ```

* Then:

  * **4 bytes**: Number of files (little-endian).
  * **4 bytes**: Unknown value (purpose still under investigation).

* For each file entry:

  * **2 bytes**: The difference between these two represents the length of the path. The meaning of the single bytes is still unknown.
  * **N bytes**: File path (ASCII).
  * **4 bytes**: Offset of the file within the archive.
  * **4 bytes**: File size.

* This header is followed by the file contents, as referenced in the file table.


## Extraction

To extract all `.pak` files from the game:

```bash
tools/paktool/extractPakFromGame.sh path_to_game_root
```

This script will automatically extract all `.pak` files found in:

* `path_to_game_root/Packs`
* `path_to_game_root/local`


To extract a single `.pak` file manually:

```bash
python3 extractPak.py path_to_pak output_folder
```

**Example:**

```bash
python3 extractPak.py "game_path/Packs/UI.pak" "assets/Packs/UI"
```

---

## Packing

Repacking `.pak` files can be attempted using the same script, but be aware:

> Note: Since parts of the file format (especially unknown header bytes) are not fully understood, repacked files may not function correctly in the game.

To pack a folder into a `.pak` file:

```bash
python3 extractPak.py input_folder output_file.pak
```
