from PIL import Image, ImageDraw, ImageFont
from fractions import Fraction
import io

def color_control(border):
    i=0
    if border == "blur":
        i=256
    return i

def extract_black_area(image_path, threshold=50):
    # 打开图片并转换为灰度模式
    img = Image.open(image_path).convert("L")

    # 创建一个新的 RGBA 图片（带透明通道）
    result = Image.new("RGBA", img.size, (0, 0, 0, 0))  # 全透明背景
    pixels = img.load()
    result_pixels = result.load()

    # 遍历所有像素
    for y in range(img.height):
        for x in range(img.width):
            if pixels[x, y] < threshold:  # 只保留黑色部分
                result_pixels[x, y] = (0, 0, 0, 255)  # 纯黑色，不透明

    # 将图片存入内存并返回
    img_io = io.BytesIO()
    result.save(img_io, format="PNG")
    img_io.seek(0)

    return Image.open(img_io)  # 直接返回 PIL 图片对象


def compose_photo_card_horizon(img_with_border: Image.Image, metadata: dict, nikon_logo_path: str, author: str ,border: str) -> Image.Image:
    w, h = img_with_border.size
    border_top = int(h / 1.10)

    # 添加nikon logo
    nikon_logo_img = Image.open(nikon_logo_path).convert("RGBA")
    #nikon_logo_img = (extract_black_area(nikon_logo_path)).convert("RGBA")

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
        model_logo_img = (extract_black_area(model_logo_path)).convert("RGBA")
        target_height_model = target_height - 30 # 与 Nikon logo 一致高度
        scale_m = target_height_model / model_logo_img.height
        model_logo_resized = model_logo_img.resize((int(model_logo_img.width * scale_m), target_height_model), Image.LANCZOS)

        img_with_border.paste(model_logo_resized, (current_x, y), model_logo_resized)
        current_x += model_logo_resized.width + int(w * 0.01)

    # 绘制竖线
    i = color_control(border)
    line_color = (i, i, i)
    line_height = int(border_height * 0.6)
    line_x = current_x
    line_y1 = border_top + (border_height - line_height) // 2
    line_y2 = line_y1 + line_height + 50
    draw = ImageDraw.Draw(img_with_border)
    draw.line((line_x, line_y1, line_x, line_y2), fill=line_color, width=4)
    current_x += int(w * 0.01)

    # 镜头型号（上）
    lens_text = metadata.get("Lens", "")
    lens_font_size = int(border_height * 0.3)
    try:
        lens_font = ImageFont.truetype("fonts/texgyreadventor-bold.otf", lens_font_size)
    except:
        lens_font = ImageFont.load_default()
    lens_y = line_y1 - 50
    draw.text((current_x, lens_y), lens_text, font=lens_font, fill=(i, i, i))

    # 拍摄时间（下）
    date_text = metadata.get("Date", "").replace(":", "/", 2)
    date_font_size = int(border_height * 0.2)
    try:
        date_font = ImageFont.truetype("fonts/Arial.ttf", date_font_size)
    except:
        date_font = ImageFont.load_default()
    date_y = line_y1 + int(border_height * 0.5) -50
    draw.text((current_x, date_y), date_text, font=date_font, fill=(128, 128, 128))

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
    param_y = lens_y
    draw.text((right_x - param_text_width, param_y), param_text, font=param_font, fill=(i, i, i))

    # 作者信息
    author_text = f"Shot by {author}"
    author_font_size = int(border_height * 0.2)
    try:
        author_font = ImageFont.truetype("fonts/Arial.ttf", author_font_size)
    except:
        author_font = ImageFont.load_default()

    author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
    author_text_width = author_bbox[2] - author_bbox[0]
    #author_y = line_y1 + int(border_height * 0.5)
    author_y = date_y
    draw.text((right_x - author_text_width, author_y), author_text, font=author_font, fill=(128, 128, 128))

    return img_with_border

from PIL import Image, ImageDraw, ImageFont
from fractions import Fraction

def compose_photo_card_vertical(img_with_border: Image.Image, metadata: dict, nikon_logo_path: str, author: str, border: str, model_logo_scale: float = 0.4) -> Image.Image:
    w, h = img_with_border.size
    is_portrait = h > w  # 竖屏检测
    border_top = int(h / (1.10 if is_portrait else 1.15))  # 竖屏边框稍大

    # 添加 Nikon Logo
    nikon_logo_img = Image.open(nikon_logo_path).convert("RGBA")
    border_height = h - border_top
    target_height = int(border_height * 0.8 if is_portrait else 1.0)  # 竖屏稍微小一点
    scale = target_height / nikon_logo_img.height
    logo_resized = nikon_logo_img.resize((int(nikon_logo_img.width * scale), target_height), Image.LANCZOS)

    padding = int(w * 0.01)
    #x_nikon = (w // 2) - logo_resized.width - padding +180 # Nikon Logo 放在左侧
    x_nikon = (w // 2) - logo_resized.width + 150
    y = border_top + (border_height - target_height) // 2
    img_with_border.paste(logo_resized, (x_nikon, y), logo_resized)

    # 获取相机信息
    camera_text = metadata.get("Camera", "NIKON")
    camera_model = camera_text.lower()

    # 根据相机型号选择相机 logo
    if "z 5" in camera_model:
        model_logo_path = "logos/NikonZ5_logo.png"
    elif "d750" in camera_model:
        model_logo_path = "logos/NikonD750_logo.png"
    else:
        model_logo_path = None

    # 加载相机型号 logo
    if model_logo_path:
        model_logo_img = Image.open(model_logo_path).convert("RGBA")
        target_height_model = int(target_height * model_logo_scale)  # 可控大小
        scale_m = target_height_model / model_logo_img.height
        model_logo_resized = model_logo_img.resize((int(model_logo_img.width * scale_m), target_height_model),
                                                   Image.LANCZOS)

        # 计算相机型号 logo 的位置，使其放在右侧
        x_model = (w // 2) +padding + 150 # 相机 Logo 放在右侧
        model_logo_y = y + (target_height - model_logo_resized.height) // 2  # 垂直居中
        img_with_border.paste(model_logo_resized, (x_model, model_logo_y), model_logo_resized)

    # 文字信息
    draw = ImageDraw.Draw(img_with_border)
    lens_text = metadata.get("Lens", "")
    date_text = metadata.get("Date", "").replace(":", "/", 2)

    # 获取拍摄参数
    focal = metadata.get("FocalLength", "N/A")
    fnum = metadata.get("FNumber", "N/A")
    expo = metadata.get("ExposureTime", "N/A")
    iso = metadata.get("ISO", "N/A")

    # 格式化信息
    fnum_str = f"f/{float(Fraction(fnum)):.1f}" if fnum != "N/A" else "f/N/A"
    param_text = f"{focal}mm  {fnum_str}  {expo}s  ISO {iso}"

    # **提高竖屏模式下的字体大小**
    lens_font_size = int(border_height * (0.15 if is_portrait else 0.3))
    date_font_size = int(border_height * (0.15 if is_portrait else 0.2))
    param_font_size = int(border_height * 0.15)
    author_font_size = int(border_height * 0.15)

    try:
        lens_font = ImageFont.truetype("fonts/texgyreadventor-bold.otf", lens_font_size)
        date_font = ImageFont.truetype("fonts/Arial.ttf", date_font_size)
        param_font = ImageFont.truetype("fonts/Avenir_Heavy.ttf", param_font_size)
        author_font = ImageFont.truetype("fonts/Arial.ttf", author_font_size)
    except:
        lens_font = date_font = param_font = author_font = ImageFont.load_default()

    # **计算左侧和右侧的位置**
    left_x = padding  # 左侧对齐
    right_x = x_model + model_logo_img.width + 6.5*padding   # 右侧对齐

    i = color_control(border)
    # **镜头信息和拍摄参数居左**
    lens_y = border_top + int(border_height * 0.1) + 110  # 放在左上方
    draw.text((left_x, lens_y), lens_text, font=lens_font, fill=(i, i, i))

    param_bbox = draw.textbbox((0, 0), param_text, font=param_font)
    param_text_width = param_bbox[2] - param_bbox[0]
    param_y = lens_y + lens_font_size + 40   # 放在镜头信息下方
    draw.text((left_x, param_y), param_text, font=param_font, fill=(i, i, i))

    author_text = f"Shot by {author}"
    author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
    author_text_width = author_bbox[2] - author_bbox[0]
    author_y = lens_y  # 放在拍摄时间下方
    author_x = right_x
    draw.text((author_x, author_y), author_text, font=author_font, fill=(128, 128, 128))

    # **拍摄时间和作者信息居右**
    date_y = param_y  # 放在右上方
    draw.text((author_x, date_y), date_text, font=date_font, fill=(128, 128, 128))

    return img_with_border



