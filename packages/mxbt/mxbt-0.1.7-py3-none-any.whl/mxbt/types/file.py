from enum import Enum
import filetype

class FileType(Enum):
    Image = 0
    Video = 1
    Other = 2

class File:

    def __init__(self, path: str) -> None:
        self.path = path
        if filetype.is_image(path):
            self.filetype = FileType.Image
        elif filetype.is_video(path):
            self.filetype = FileType.Video
        else:
            self.filetype = FileType.Other


