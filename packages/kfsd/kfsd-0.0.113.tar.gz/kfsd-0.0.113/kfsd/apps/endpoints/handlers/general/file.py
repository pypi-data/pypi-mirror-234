from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.general.file import FileModelSerializer
from kfsd.apps.models.tables.general.file import File
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.time import Time
from PIL import Image
from io import BytesIO


def gen_file_handler(instance):
    handler = FileHandler(instance.identifier, False)
    qsData = FileModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


class FileHandler(BaseHandler):
    DEFAULT_MIME_TYPE = "text/html"

    def __init__(self, fileIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=FileModelSerializer,
            modelClass=File,
            identifier=fileIdentifier,
            isDBFetch=isDBFetch,
        )

    def getFileExtn(self):
        return DictUtils.get_by_path(self.getModelQSData(), "file.extension")

    def getFilePath(self):
        return DictUtils.get_by_path(self.getModelQSData(), "file.path")

    def getFileExpiryTime(self):
        expiryTime = Time.future_time(
            {"minutes": DictUtils.get(self.getModelQSData(), "expiry_in_mins", 0)},
            True,
            "%a, %d %b %Y %H:%M:%S GMT",
        )
        return expiryTime

    def getRespContentType(self):
        fileExtn = self.getFileExtn()
        mimeMap = self.get_file_extn_mime_map()
        if fileExtn in mimeMap:
            return mimeMap[fileExtn]
        else:
            return self.DEFAULT_MIME_TYPE

    def getFile(self):
        filePath = self.getFilePath()
        with open(filePath, "rb") as f:
            fileContent = f.read()
            return fileContent

    def getImageExtentions(self):
        image_extensions = [
            ".jpg",
            ".jpeg",  # JPEG
            ".png",  # Portable Network Graphics
            ".gif",  # Graphics Interchange Format
            ".bmp",  # Bitmap
            ".tif",
            ".tiff",  # Tagged Image File Format
            ".webp",  # WebP
            ".ico",  # Icon
            ".svg",  # Scalable Vector Graphics
            ".psd",  # Adobe Photoshop Document
            ".ai",  # Adobe Illustrator
            ".eps",  # Encapsulated PostScript
            ".pdf",  # Portable Document Format, often includes images
            ".raw",  # Raw image format
            ".cr2",  # Canon Raw Image
            ".nef",  # Nikon Electronic Format
            ".arw",  # Sony Alpha Raw
            ".orf",  # Olympus Raw Format
            ".rw2",  # Panasonic Raw Format
            ".dng",  # Digital Negative Format
        ]
        return image_extensions

    def getImageThumbnail(self):
        filePath = self.getFilePath()
        img = Image.open(filePath)
        img.thumbnail((100, 100))
        thumbnail_io = BytesIO()
        img.save(thumbnail_io, format="PNG")
        return thumbnail_io.getvalue()

    def getThumbnailMimeType(self):
        return self.get_file_extn_mime_map()[".png"]

    def getDefaultThumbnail(self, fileExtn):
        filePath = "uploads/defaults/doc.png"
        with open(filePath, "rb") as f:
            fileContent = f.read()
            return fileContent

    def getThumbnail(self):
        fileExtn = self.getFileExtn()
        if fileExtn in self.getImageExtentions():
            return self.getImageThumbnail()
        return self.getDefaultThumbnail(fileExtn)

    def get_file_extn_mime_map(self):
        file_extension_to_mime = {
            ".3g2": "video/3gpp2",
            ".3gp": "video/3gpp",
            ".aac": "audio/aac",
            ".ai": "application/postscript",
            ".aif": "audio/x-aiff",
            ".aiff": "audio/x-aiff",
            ".apk": "application/vnd.android.package-archive",
            ".asp": "application/x-aspx",
            ".avi": "video/x-msvideo",
            ".bmp": "image/bmp",
            ".bz2": "application/x-bzip2",
            ".c": "text/x-c",
            ".cpp": "text/x-c",
            ".css": "text/css",
            ".csv": "text/csv",
            ".doc": "application/msword",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".exe": "application/x-msdownload",
            ".flac": "audio/flac",
            ".gif": "image/gif",
            ".gz": "application/gzip",
            ".h": "text/x-c",
            ".html": "text/html",
            ".ico": "image/vnd.microsoft.icon",
            ".jpeg": "image/jpeg",
            ".jpg": "image/jpeg",
            ".js": "application/javascript",
            ".json": "application/json",
            ".m4a": "audio/mp4",
            ".mid": "audio/midi",
            ".midi": "audio/midi",
            ".mkv": "video/x-matroska",
            ".mov": "video/quicktime",
            ".mp3": "audio/mpeg",
            ".mp4": "video/mp4",
            ".mpg": "video/mpeg",
            ".pdf": "application/pdf",
            ".png": "image/png",
            ".ppt": "application/vnd.ms-powerpoint",
            ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            ".py": "text/x-python",
            ".rar": "application/x-rar-compressed",
            ".rtf": "application/rtf",
            ".sh": "application/x-sh",
            ".svg": "image/svg+xml",
            ".tar": "application/x-tar",
            ".ttf": "font/ttf",
            ".txt": "text/plain",
            ".wav": "audio/wav",
            ".webm": "video/webm",
            ".wma": "audio/x-ms-wma",
            ".wmv": "video/x-ms-wmv",
            ".xml": "application/xml",
            ".zip": "application/zip",
        }
        return file_extension_to_mime
