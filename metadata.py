import exifread
import subprocess
import json

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

    def get_lens_info(tags, file_path):
        for key in ["EXIF LensModel", "MakerNote LensID", "MakerNote LensSpec"]:
            if key in tags:
                return str(tags[key])

        # 如果 exifread 无法获取，则尝试使用 exiftool
        try:
            result = subprocess.run(['exiftool', '-LensID', '-j', file_path],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            data = json.loads(result.stdout.decode())[0]
            return data.get("LensID", "Unknown LensID")
        except Exception as e:
            print("ExifTool LensID error:", e)
            return "Unknown LensID"

    metadata = {
        "Camera": get_tag("Image Model"),
        "Lens": get_lens_info(tags, file_path),
        "Filename": file_path.split("/")[-1],
        "ISO": get_tag("EXIF ISOSpeedRatings"),
        "ExposureTime": get_tag("EXIF ExposureTime"),
        "FNumber": get_tag("EXIF FNumber"),
        "FocalLength": get_tag("EXIF FocalLength"),
        "ExposureProgram": get_tag("EXIF ExposureProgram"),
        "Date": get_tag("EXIF DateTimeOriginal")
    }

    return metadata
