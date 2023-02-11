from enum import Enum


class FileType(str, Enum):
    image = "Image"
    music = "Music"
    exec = "Executable"
    doc = "Document"
    video = "Video"
    code = "Code"
    other = "Other"
