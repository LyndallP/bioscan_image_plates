# BIOSCAN Image Plates

A Python tool that generates an interactive HTML viewer for **BIOSCAN 96-well plate specimen images**, loading thumbnails directly from the [Sanger Institute COG](https://tol-bioscan-images.cog.sanger.ac.uk/) image store.

---

## Overview

Each BIOSCAN plate holds up to 96 specimens arranged in an **8-row × 12-column** grid (rows A–H, columns 1–12). This tool reads a list of plate IDs from a plain text file and produces a self-contained HTML page that displays every well's specimen image in a visual plate layout.

- Images are fetched live from `https://tol-bioscan-images.cog.sanger.ac.uk/processed_images/`
- Wells with missing images are highlighted in red
- Wells that are loading show a grey placeholder

---

## Requirements

- Python 3.6 or higher
- No external packages required (standard library only)
- A web browser to view the output HTML

---

## Setup

```bash
git clone https://github.com/LyndallP/bioscan_image_plates.git
cd bioscan_image_plates
```

---

## Usage

### 1. Edit `image_plates.txt`

Add or remove plate IDs — one per line. Lines starting with `#` are treated as comments and ignored.

```
# My BIOSCAN plates
NTGC_007
WREN_038
WREN_031
```

### 2. Run the script

```bash
python generate_plates.py
```

This produces `bioscan_plates.html` in the current directory.

### 3. Open the viewer

Open `bioscan_plates.html` in any web browser. Images are loaded live from the internet, so an active connection is required.

---

## Options

```
python generate_plates.py --input my_plates.txt --output my_viewer.html
```

| Flag | Default | Description |
|------|---------|-------------|
| `--input` | `image_plates.txt` | Path to the plate ID text file |
| `--output` | `bioscan_plates.html` | Path for the generated HTML file |

---

## Input File Format (`image_plates.txt`)

- One plate ID per line
- Blank lines are ignored
- Lines beginning with `#` are comments

**Example:**
```
# NTGC plates
NTGC_007

# WREN plates
WREN_038
WREN_031
WREN_032
WREN_033
WREN_034
```

---

## Output

The generated HTML file contains one plate section per ID, each showing:

- Plate ID as a heading
- 8 × 12 well grid with row (A–H) and column (1–12) headers
- Specimen thumbnail for each well, loaded from:

  ```
  https://tol-bioscan-images.cog.sanger.ac.uk/processed_images/{PlateID}_{WellID}.jpg
  ```

  e.g. `WREN_038_A1.jpg`, `NTGC_007_H12.jpg`

- **Grey** background while an image is loading
- **Red** background if the image is not found

---

## Plate ID Format

Plate IDs follow the pattern `{PROJECT}_{NUMBER}`, e.g.:

| Plate ID | Project | Plate number |
|----------|---------|--------------|
| `NTGC_007` | NTGC | 007 |
| `WREN_038` | WREN | 038 |

---

## Project Structure

```
bioscan_image_plates/
├── generate_plates.py   # Main script
├── image_plates.txt     # List of plate IDs to process
├── LICENSE              # MIT License
└── README.md            # This file
```

The generated `bioscan_plates.html` is excluded from version control (see `.gitignore`).

---

## License

[MIT](LICENSE) — Copyright (c) 2026 LyndallP
