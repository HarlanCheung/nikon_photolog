from PIL import Image

def create_bottom_border_canvas(img: Image.Image, border_ratio: float = 0.10, border_color=(255, 255, 255)) -> Image.Image:
    w, h = img.size
    bottom_border = int(h * border_ratio)
    new_h = h + bottom_border

    # 创建新画布
    new_img = Image.new("RGB", (w, new_h), color=border_color)

    # 将原图粘贴到顶部
    new_img.paste(img, (0, 0))

    return new_img