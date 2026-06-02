"""
generate_plates.py

Generates an HTML 96-well plate viewer for BIOSCAN specimen images.
Plate IDs are read from image_plates.txt (or a file specified via --input).

Usage:
    python generate_plates.py
    python generate_plates.py --input my_plates.txt --output my_viewer.html
    python generate_plates.py --investigate investigate_wells.txt
"""

import argparse
import os

# Well layout constants
ROWS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
COLS = range(1, 13)
IMAGE_BASE_URL = "https://tol-bioscan-images.cog.sanger.ac.uk/processed_images"


def read_plates(filepath):
    """Read plate IDs from a text file. Skips blank lines and comment lines."""
    plates = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                plates.append(line)
    return plates


def read_investigate_wells(filepath, known_plates):
    """Parse investigate_wells.txt and return a set of (plate_id, well_id) tuples.

    Each line is matched against known plate IDs. The well ID is the token
    immediately after the matched plate ID, e.g.:
        CONTROL_NEG_LYSATE_FACE_362_H12  ->  plate=FACE_362, well=H12
    Lines that don't match any known plate are skipped with a warning.
    """
    flagged = set()
    if not os.path.exists(filepath):
        return flagged

    with open(filepath, 'r') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            matched = False
            for plate_id in known_plates:
                marker = f"_{plate_id}_"
                idx = line.find(marker)
                if idx != -1:
                    well_id = line[idx + len(marker):]
                    well_id = well_id.split('_')[0].strip()
                    if well_id:
                        flagged.add((plate_id, well_id))
                        matched = True
                        break
            if not matched:
                print(f"Warning: no known plate found in investigate line: {line!r}")

    return flagged


def generate_html(plates, flagged_wells=None):
    if flagged_wells is None:
        flagged_wells = set()
    html = """\
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>BIOSCAN 96-Well Plate Viewer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .plate-container {
            margin-bottom: 40px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .plate-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }
        .plate {
            display: inline-block;
            border: 2px solid #333;
            background: #fff;
        }
        .plate-row {
            display: flex;
        }
        .well {
            width: 60px;
            height: 60px;
            border: 1px solid #ccc;
            position: relative;
            overflow: hidden;
        }
        .well img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .well-label {
            position: absolute;
            top: 2px;
            left: 2px;
            background: rgba(255, 255, 255, 0.8);
            font-size: 8px;
            padding: 1px 3px;
            border-radius: 2px;
            font-weight: bold;
        }
        .loading {
            background: #e0e0e0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            color: #666;
        }
        .error {
            background: #ffebee;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            color: #c62828;
        }
        .investigate {
            box-shadow: inset 0 0 0 3px #ff6600;
            z-index: 1;
        }
        .investigate .well-label {
            background: rgba(255, 102, 0, 0.85);
            color: white;
        }
        .investigate-legend {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 12px;
            font-size: 13px;
            color: #555;
        }
        .investigate-legend-swatch {
            width: 16px;
            height: 16px;
            box-shadow: inset 0 0 0 3px #ff6600;
            display: inline-block;
        }
        .row-header, .col-header {
            width: 60px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 12px;
        }
        .col-header {
            height: 60px;
            width: 20px;
            writing-mode: vertical-rl;
        }
        .headers-row {
            display: flex;
        }
        .plate-wrapper {
            display: flex;
        }
    </style>
</head>
<body>
"""

    if flagged_wells:
        html += """\
    <div class="investigate-legend">
        <span class="investigate-legend-swatch"></span>
        Wells flagged for investigation
    </div>
"""

    for plate_id in plates:
        html += f"""
    <div class="plate-container">
        <div class="plate-title">{plate_id}</div>
        <div class="plate-wrapper">
            <div class="col-header-container">
                <div style="height: 20px;"></div>
"""
        for row in ROWS:
            html += f'                <div class="col-header">{row}</div>\n'

        html += """\
            </div>
            <div>
                <div class="headers-row">
                    <div style="width: 20px;"></div>
"""
        for col in COLS:
            html += f'                    <div class="row-header">{col}</div>\n'

        html += """\
                </div>
                <div class="plate">
"""
        for row in ROWS:
            html += '                    <div class="plate-row">\n'
            html += '                        <div class="row-header"></div>\n'

            for col in COLS:
                well_id = f"{row}{col}"
                specimen_id = f"{plate_id}_{well_id}"
                image_url = f"{IMAGE_BASE_URL}/{specimen_id}.jpg"
                extra_class = " investigate" if (plate_id, well_id) in flagged_wells else ""

                html += f"""\
                        <div class="well loading{extra_class}" id="{plate_id}_{well_id}">
                            <div class="well-label">{well_id}</div>
                            <img src="{image_url}"
                                 alt="{specimen_id}"
                                 onload="this.parentElement.classList.remove('loading')"
                                 onerror="this.parentElement.classList.add('error'); this.parentElement.classList.remove('loading'); this.style.display='none';">
                        </div>
"""
            html += '                    </div>\n'

        html += """\
                </div>
            </div>
        </div>
    </div>
"""

    if flagged_wells:
        html += """\
    <p style="font-size:12px; color:#888; margin-top:10px;">
        Wells flagged for investigation are shown with an orange border.
    </p>
"""
    html += "</body>\n</html>\n"
    return html


def main():
    parser = argparse.ArgumentParser(
        description="Generate a BIOSCAN 96-well plate HTML viewer."
    )
    parser.add_argument(
        '--input', default='image_plates.txt',
        help="Text file containing plate IDs (default: image_plates.txt)"
    )
    parser.add_argument(
        '--output', default='bioscan_plates.html',
        help="Output HTML file (default: bioscan_plates.html)"
    )
    parser.add_argument(
        '--investigate', default='investigate_wells.txt',
        metavar='FILE',
        help="Text file of well strings to highlight (default: investigate_wells.txt if present)"
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: input file '{args.input}' not found.")
        raise SystemExit(1)

    plates = read_plates(args.input)
    if not plates:
        print(f"Error: no plate IDs found in '{args.input}'.")
        raise SystemExit(1)

    print(f"Loaded {len(plates)} plate(s): {', '.join(plates)}")

    flagged_wells = read_investigate_wells(args.investigate, plates)
    if flagged_wells:
        print(f"Flagged {len(flagged_wells)} well(s) for investigation: "
              + ", ".join(f"{p}_{w}" for p, w in sorted(flagged_wells)))
    elif os.path.exists(args.investigate):
        print(f"No matching wells found in '{args.investigate}'.")

    html = generate_html(plates, flagged_wells)

    with open(args.output, 'w') as f:
        f.write(html)

    print(f"HTML viewer written to: {args.output}")


if __name__ == '__main__':
    main()
