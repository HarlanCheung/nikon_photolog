from PIL import Image, ImageFilter,ImageDraw

def create_border(img:Image.Image,border) -> Image.Image:
    if border == "basic":
        new_img = create_bottom_border_canvas(img)
    if border == "blur":
        new_img = create_blurred_background(img)

    return new_img

def create_bottom_border_canvas(img: Image.Image, border_ratio: float = 0.10, border_color=(255, 255, 255)) -> Image.Image:
    w, h = img.size
    bottom_border = int(h * border_ratio)
    new_h = h + bottom_border

    # 创建新画布
    new_img = Image.new("RGB", (w, new_h), color=border_color)

    # 将原图粘贴到顶部
    new_img.paste(img, (0, 0))

    return new_img

def create_blurred_background(img: Image.Image,
                                                   border_ratio: float = 0.10,
                                                   blur_radius: int = 70,
                                                   corner_radius: int = 50) -> Image.Image:
    w, h = img.size
    border_size = int(min(w, h) * border_ratio)
    new_w, new_h = w + 2 * border_size, h + 2 * border_size

    # **创建毛玻璃背景**
    blurred_bg = img.copy().filter(ImageFilter.GaussianBlur(blur_radius))
    blurred_bg = blurred_bg.resize((new_w, new_h), Image.LANCZOS)

    # **创建带圆角的遮罩**
    mask = Image.new("L", (w, h), 0)  # 黑色背景
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, w, h), radius=corner_radius, fill=255)  # 白色圆角区域

    # **应用遮罩到原图**
    rounded_img = img.copy()
    rounded_img.putalpha(mask)  # 透明处理

    # **创建最终画布**
    new_img = Image.new("RGB", (new_w, new_h))
    new_img.paste(blurred_bg, (0, 0))
    new_img.paste(rounded_img, (border_size, border_size), rounded_img)  # 贴上带圆角的图片

    return new_img
