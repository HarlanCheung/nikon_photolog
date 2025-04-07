# Nikon PhotoLog Generator

A Python tool to generate a beautifully formatted photo card from Nikon NEF (RAW) files. The script overlays shooting information, camera and lens details, and author credits onto an image with a custom visual layout.

**Version:** 1.1

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
- Adds batch processing for `.NEF` and `.JPG` files in a folder

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
├── GUI.py                      # PyQt5-based GUI interface
```

---

## 🚀 Usage

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

If you're using lens detection for older Nikon lenses, make sure [ExifTool](https://exiftool.org/) is installed:

- macOS: `brew install exiftool`
- Windows: [Download here](https://exiftool.org/)
- Linux: `sudo apt install libimage-exiftool-perl`
  
### 2. Run the script
```bash
python main.py <input.nef> <output.jpg> --author "Your Name" --border "border mode:blur or basic"
```

**Example:**
```bash
python main.py images/DSC_0003.NEF output/0003.jpg --author "Harlan" --border "blur"
```

### Batch Processing Mode

To process all `.NEF` and `.JPG` files in a folder, use the `--batch` flag:

```bash
python main.py input_folder output_folder --author "Your Name" --border "blur" --batch
```

### Run the GUI (PyQt5)
```bash
python GUI.py
```

---

## 📝 Requirements
- Python 3.7+
- Dependencies:
  - `rawpy`
  - `Pillow`
  - `exifread`
  - `exiftool` (for accurate lens identification, especially with legacy Nikon lenses)
  - `PyQt5` (for GUI interface)

You can install them via:
```bash
pip install rawpy Pillow exifread
```

---

## 🆕 Changelog

**v1.1**
- Added graphical user interface (GUI) using PyQt5

**v1.0.1**
- Added batch processing support for `.NEF` and `.JPG` images in a folder

**v1.0**
- Initial release: NEF to JPG with metadata card

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
- Lens decoding via [ExifTool](https://exiftool.org/)
- Fonts:
  - [TeXGyre Adventor](https://www.gust.org.pl/projects/e-foundry/tex-gyre/adventor)
  - [Avenir Heavy](https://www.myfonts.com/fonts/linotype/avenir/) (used locally)
