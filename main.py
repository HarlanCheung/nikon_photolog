import os
import argparse
import glob
from PIL import Image
import rawpy
from metadata import get_nef_metadata
from tqdm import tqdm

from border import create_bottom_border_canvas,create_blurred_background,create_border
from compose import *

def load_image(image_path):
    ext = os.path.splitext(image_path)[1].lower()
    if ext == ".nef":
        with rawpy.imread(image_path) as raw:
            rgb = raw.postprocess()
        return Image.fromarray(rgb)
    else:
        return Image.open(image_path).convert("RGB")

def process_single_file(nef_path, output_path, author, border, border_color=(255, 255, 255)):
    img = load_image(nef_path)
    meta = get_nef_metadata(nef_path)
    print("Metadata:", meta)

    img_with_border = create_border(img, border, border_color=border_color)

    if img_with_border.width > img_with_border.height:
        final_img = compose_photo_card_horizon(
            img_with_border, meta, nikon_logo_path="logos/Nikon_logo.png",
            author=author, border=border
        )
    else:
        final_img = compose_photo_card_vertical(
            img_with_border, meta, nikon_logo_path="logos/Nikon_logo.png",
            author=author, border=border
        )

    final_img.save(output_path)
    print(f"✅ Saved with bottom border: {output_path}")

def batch_process_images(input_dir, output_dir, author, border, progress_callback=None, border_color=(255, 255, 255)):
    os.makedirs(output_dir, exist_ok=True)
    nef_files = glob.glob(os.path.join(input_dir, "*.nef")) + glob.glob(os.path.join(input_dir, "*.jpg"))
    total = len(nef_files)
    if progress_callback:
        for idx, image_path in enumerate(nef_files):
            filename = os.path.splitext(os.path.basename(image_path))[0] + "_processed.jpg"
            output_path = os.path.join(output_dir, filename)
            process_single_file(image_path, output_path, author, border, border_color=border_color)
            progress_callback(idx + 1, total)
    else:
        for image_path in tqdm(nef_files, desc="Processing images"):
            filename = os.path.splitext(os.path.basename(image_path))[0] + "_processed.jpg"
            output_path = os.path.join(output_dir, filename)
            process_single_file(image_path, output_path, author, border, border_color=border_color)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Nikon photo log image.")
    parser.add_argument("nef_path", type=str, help="Path to input NEF file or folder")
    parser.add_argument("output_path", type=str, help="Path to save output image or folder")
    parser.add_argument("--author", type=str, default="Harlan", help="Author name (optional)")
    parser.add_argument("--border", type=str, default="basic", help="blur or basic border")
    parser.add_argument("--batch", action="store_true", help="Enable batch processing mode")
    args = parser.parse_args()

    if args.batch:
        batch_process_images(args.nef_path, args.output_path, args.author, args.border)
    else:
        process_single_file(args.nef_path, args.output_path, args.author, args.border)
