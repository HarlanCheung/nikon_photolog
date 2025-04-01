from PIL import Image, ImageDraw, ImageFont
from fractions import Fraction

def compose_photo_card(img_with_border: Image.Image, metadata: dict, nikon_logo_path: str, author: str) -> Image.Image:
    w, h = img_with_border.size
    border_top = int(h / 1.10)

    # 添加nikon logo
    nikon_logo_img = Image.open(nikon_logo_path).convert("RGBA")

    # 目标高度为底部边框的 60%
    border_height = h - border_top
    target_height = int(border_height * 0.6)
    scale = target_height / nikon_logo_img.height
    logo_resized = nikon_logo_img.resize((int(nikon_logo_img.width * scale), target_height), Image.LANCZOS)

    # 放置位置：左下角，带 padding
    padding = int(w * 0.03)
    x = padding
    y = border_top + (border_height - target_height) // 2

    # 粘贴 logo
    img_with_border.paste(logo_resized, (x, y), logo_resized)

    # 添加 Camera 信息
    camera_text = metadata.get("Camera", "NIKON")
    camera_model = camera_text.lower()
    if "z 5" in camera_model:
        model_logo_path = "logos/NikonZ5_logo.png"
    elif "d750" in camera_model:
        model_logo_path = "logos/NikonD750_logo.png"
    else:
        model_logo_path = None

    current_x = x + logo_resized.width + int(w * 0.01)  # 间隔 1%

    # 加载型号 logo
    if model_logo_path:
        model_logo_img = Image.open(model_logo_path).convert("RGBA")
        target_height_model = target_height  # 与 Nikon logo 一致高度
        scale_m = target_height_model / model_logo_img.height
        model_logo_resized = model_logo_img.resize((int(model_logo_img.width * scale_m), target_height_model), Image.LANCZOS)

        img_with_border.paste(model_logo_resized, (current_x, y), model_logo_resized)
        current_x += model_logo_resized.width + int(w * 0.01)

    # 绘制竖线
    line_color = (120, 120, 120)
    line_height = int(border_height * 0.9)
    line_x = current_x
    line_y1 = border_top + (border_height - line_height) // 2
    line_y2 = line_y1 + line_height
    draw = ImageDraw.Draw(img_with_border)
    draw.line((line_x, line_y1, line_x, line_y2), fill=line_color, width=2)
    current_x += int(w * 0.01)

    # 镜头型号（上）
    lens_text = metadata.get("Lens", "")
    lens_font_size = int(border_height * 0.3)
    try:
        lens_font = ImageFont.truetype("fonts/texgyreadventor-bold.otf", lens_font_size)
    except:
        lens_font = ImageFont.load_default()
    draw.text((current_x, line_y1), lens_text, font=lens_font, fill=(0, 0, 0))

    # 拍摄时间（下）
    date_text = metadata.get("Date", "").replace(":", "/", 2)
    date_font_size = int(border_height * 0.2)
    try:
        date_font = ImageFont.truetype("Arial.ttf", date_font_size)
    except:
        date_font = ImageFont.load_default()
    date_y = line_y1 + int(border_height * 0.5)
    draw.text((current_x, date_y), date_text, font=date_font, fill=(120, 120, 120)) 

    # 右侧参数与作者信息
    right_padding = padding
    right_x = w - right_padding

    # 参数信息（焦距 光圈 快门 ISO）
    focal = metadata.get("FocalLength", "")
    fnum = metadata.get("FNumber", "")
    expo = metadata.get("ExposureTime", "")
    iso = metadata.get("ISO", "")

    fnum_val = float(Fraction(fnum))
    fnum_str = f"f/{fnum_val:.1f}"  # 保留一位小数
    param_text = f"{focal}mm {fnum_str} {expo} ISO{iso}"

    param_font_size = int(border_height * 0.3)
    try:
        param_font = ImageFont.truetype("fonts/Avenir_Heavy.ttf", param_font_size)
    except:
        param_font = ImageFont.load_default()

    param_bbox = draw.textbbox((0, 0), param_text, font=param_font)
    param_text_width = param_bbox[2] - param_bbox[0]
    param_y = line_y1
    draw.text((right_x - param_text_width, param_y), param_text, font=param_font, fill=(0, 0, 0))

    # 作者信息
    author_text = f"Photo by {author}"
    author_font_size = int(border_height * 0.2)
    try:
        author_font = ImageFont.truetype("Arial.ttf", author_font_size)
    except:
        author_font = ImageFont.load_default()

    author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
    author_text_width = author_bbox[2] - author_bbox[0]
    author_y = line_y1 + int(border_height * 0.5)
    draw.text((right_x - author_text_width, author_y), author_text, font=author_font, fill=(120, 120, 120))

    return img_with_border