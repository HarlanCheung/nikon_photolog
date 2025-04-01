import exifread

def get_nef_metadata(file_path):
    """
    从 .nef 文件中提取常用拍摄参数元信息。

    参数:
        file_path (str): .nef 文件的路径

    返回:
        dict: 包含 ISO、快门时间、光圈数、焦距、曝光程序 的字典
    """
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f, stop_tag="UNDEF", details=False)

    def get_tag(name):
        return str(tags.get(name, "N/A"))

    metadata = {
        "Camera": get_tag("Image Model"),
        "Lens": get_tag("EXIF LensModel"),
        "Filename": file_path.split("/")[-1],
        "ISO": get_tag("EXIF ISOSpeedRatings"),
        "ExposureTime": get_tag("EXIF ExposureTime"),
        "FNumber": get_tag("EXIF FNumber"),
        "FocalLength": get_tag("EXIF FocalLength"),
        "ExposureProgram": get_tag("EXIF ExposureProgram"),
        "Date": get_tag("EXIF DateTimeOriginal")
    }

    return metadata
