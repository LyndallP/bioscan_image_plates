"""
generate_plates.py

Generates an HTML 96-well plate viewer for BIOSCAN specimen images.
Plate IDs are read from image_plates.txt (or a file specified via --input).

Usage:
    python generate_plates.py
    python generate_plates.py --input my_plates.txt --output my_viewer.html
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


def generate_html(plates):
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

                html += f"""\
                        <div class="well loading" id="{plate_id}_{well_id}">
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
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: input file '{args.input}' not found.")
        raise SystemExit(1)

    plates = read_plates(args.input)
    if not plates:
        print(f"Error: no plate IDs found in '{args.input}'.")
        raise SystemExit(1)

    print(f"Loaded {len(plates)} plate(s): {', '.join(plates)}")

    html = generate_html(plates)

    with open(args.output, 'w') as f:
        f.write(html)

    print(f"HTML viewer written to: {args.output}")


if __name__ == '__main__':
    main()
