TRANSLIT_CYRILLICS = "абвгґдеёєэжзиіїйклмнопрстуфхцчшщюяьъ"
TRANSLIT_MAPPING_LIST = ["a", "b", "v", "g", "g", "d", "e", "io", "ie", "e", "zh", "z", "y", "i", "ii", "i", "k", "l",
                         "m", "n", "o", "p", "r", "s", "t", "u", "f", "kh", "ts", "ch", "sh", "shch", "iu", "ia", "",
                         ""]

TRANSLIT_TABLE = {}
for char, trnsl in zip(TRANSLIT_CYRILLICS, TRANSLIT_MAPPING_LIST):
    TRANSLIT_TABLE[ord(char)] = trnsl
    TRANSLIT_TABLE[ord(char.upper())] = trnsl.upper()

FS_DEFAULT_GROUP = "unknown"
FS_DIRECTORY_GROUP = "directories"
FS_SYMLINK_GROUP = "symlinks"

FS_ERROR_RENAMING = "FS_ERROR_RENAMING"
FS_ERROR_FILE_EXISTS = "FILE_EXISTS"
FS_ERROR_DIR_EXISTS = "DIRECTORY_EXISTS"
ERROR_EMPTY_VALUE = "EMPTY_VALUE"
ERROR_ARCHIVE_WITHOUT_EXTENSION = "ARCHIVE_WITHOUT_EXTENSION"

FS_GROUPS = {
    "VIDS": "video",
    "IMGS": "images",
    "DOCS": "documents",
    "AUD": "audio",
    "ARCH": "archives",
    "INST": "install",
    "LOGS": "logs",
    "FONT": "fonts"
}

GROUPS_BY_EXTENSION = {
    "JPEG": FS_GROUPS["IMGS"],
    "PNG": FS_GROUPS["IMGS"],
    "JPG": FS_GROUPS["IMGS"],
    "SVG": FS_GROUPS["IMGS"],
    "AVI": FS_GROUPS["VIDS"],
    "MP4": FS_GROUPS["VIDS"],
    "MOV": FS_GROUPS["VIDS"],
    "MKV": FS_GROUPS["VIDS"],
    "DOC": FS_GROUPS["DOCS"],
    "DOCX": FS_GROUPS["DOCS"],
    "TXT": FS_GROUPS["DOCS"],
    "PDF": FS_GROUPS["DOCS"],
    "XLSX": FS_GROUPS["DOCS"],
    "XLS": FS_GROUPS["DOCS"],
    "PPTX": FS_GROUPS["DOCS"],
    "PPT": FS_GROUPS["DOCS"],
    "MP3": FS_GROUPS["AUD"],
    "OGG": FS_GROUPS["AUD"],
    "WAV": FS_GROUPS["AUD"],
    "AMR": FS_GROUPS["AUD"],
    "ZIP": FS_GROUPS["ARCH"],
    "GZ": FS_GROUPS["ARCH"],
    "TAR": FS_GROUPS["ARCH"],
    "TGZ": FS_GROUPS["ARCH"],
    "TXZ": FS_GROUPS["ARCH"],
    "TBZ": FS_GROUPS["ARCH"],
    "RAR": FS_GROUPS["ARCH"],
    "BZ2": FS_GROUPS["ARCH"],
    "XZ": FS_GROUPS["ARCH"],
    "7Z": FS_GROUPS["ARCH"],
    "MSI": FS_GROUPS["INST"],
    "LOG": FS_GROUPS["LOGS"],
    "TTF": FS_GROUPS["FONT"],
    "WOFF": FS_GROUPS["FONT"],
    "WOFF2": FS_GROUPS["FONT"]
}
