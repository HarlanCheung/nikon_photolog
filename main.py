import os
import argparse
from PIL import Image
import rawpy
from metadata import get_nef_metadata
from border import create_bottom_border_canvas
from compose import compose_photo_card

def load_nef_as_image(nef_path):
    with rawpy.imread(nef_path) as raw:
        rgb = raw.postprocess()
    return Image.fromarray(rgb)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Nikon photo log image.")
    parser.add_argument("nef_path", type=str, help="Path to input NEF file")
    parser.add_argument("output_path", type=str, help="Path to save output image")
    parser.add_argument("--author", type=str, default="Harlan", help="Author name (optional)")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    nef_path = args.nef_path
    output_path = args.output_path
    author = args.author

    img = load_nef_as_image(nef_path)
    meta = get_nef_metadata(nef_path)
    print("Metadata:", meta)

    img_with_border = create_bottom_border_canvas(img)

    final_img = compose_photo_card(img_with_border, meta, nikon_logo_path="logos/Nikon_logo.png", author=author)

    final_img.save(output_path)
    print(f"✅ Saved with bottom border: {output_path}")