# Nikon PhotoLog Generator

A Python tool to generate a beautifully formatted photo card from Nikon NEF (RAW) files. The script overlays shooting information, camera and lens details, and author credits onto an image with a custom visual layout.

---

## 📸 Features

- Converts `.NEF` (Nikon RAW) files into formatted `.JPG`
- Adds white bottom border with Nikon branding and metadata
- Displays:
  - Nikon logo + camera model logo (e.g., Z5, D750)
  - Lens model
  - Shooting date (formatted as `YYYY/MM/DD HH:MM:SS`)
  - Exposure settings (focal length, aperture, shutter speed, ISO)
  - Author name (e.g., "Photo by Harlan")
- Automatically adjusts fonts and layout to image size

---

## 🧱 Project Structure

```
photolog/
├── main.py                      # Entry point script
├── border.py                   # Adds bottom border to image
├── compose.py                  # Composes text, logo, metadata onto the canvas
├── metadata.py                 # Extracts metadata from NEF using ExifRead
├── fonts/                      # Custom fonts used in rendering
│   ├── texgyreadventor-bold.otf
│   └── Avenir_Heavy.ttf
├── logos/                      # PNG logos for Nikon and models
│   ├── Nikon_logo.png
│   ├── NikonZ5_logo.png
│   └── NikonD750_logo.png
```

---

## 🚀 Usage

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the script
```bash
python main.py <input.nef> <output.jpg> --author "Your Name"
```

**Example:**
```bash
python main.py images/DSC_0003.NEF output/0003.jpg --author "Harlan"
```

---

## 📝 Requirements
- Python 3.7+
- Dependencies:
  - `rawpy`
  - `Pillow`
  - `exifread`

You can install them via:
```bash
pip install rawpy Pillow exifread
```

---

## 🧩 Customization
- To change logos: replace PNGs in `logos/`
- To use different fonts: add `.ttf/.otf` to `fonts/` and update `compose.py`
- To extend metadata display: edit the layout in `compose.py`

---

## 📄 License
MIT License. Feel free to adapt and use for your own photography workflow.

---

## 🙌 Acknowledgements
- Nikon RAW reading via [rawpy](https://pypi.org/project/rawpy/)
- EXIF metadata via [ExifRead](https://pypi.org/project/ExifRead/)
- Fonts:
  - [TeXGyre Adventor](https://www.gust.org.pl/projects/e-foundry/tex-gyre/adventor)
  - [Avenir Heavy](https://www.myfonts.com/fonts/linotype/avenir/) (used locally)

