from enum import Enum


class MIMETypes(Enum):
    bmp = "image/bmp"
    gif = "image/gif"
    jpeg = "image/jpeg"
    jpg = "image/jpeg"
    png = "image/png"
    webp = "image/webp"
    mp4 = "video/mp4"
    mpeg = "video/mpeg"
    webm = "video/webm"

    @classmethod
    def supported_types(cls):
        return cls.__members__.keys()
