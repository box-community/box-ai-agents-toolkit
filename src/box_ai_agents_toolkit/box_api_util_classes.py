from dataclasses import dataclass
from enum import Enum

from box_sdk_gen import (
    File,
)


class DocumentFiles(Enum):
    """DocumentFiles(Enum).

    An enum containing all of the supported extensions for files
    Box considers Documents. These files should have text
    representations.
    """

    DOC = "doc"
    DOCX = "docx"
    GDOC = "gdoc"
    GSHEET = "gsheet"
    NUMBERS = "numbers"
    ODS = "ods"
    ODT = "odt"
    PAGES = "pages"
    PDF = "pdf"
    RTF = "rtf"
    WPD = "wpd"
    XLS = "xls"
    XLSM = "xlsm"
    XLSX = "xlsx"
    AS = "as"
    AS3 = "as3"
    ASM = "asm"
    BAT = "bat"
    C = "c"
    CC = "cc"
    CMAKE = "cmake"
    CPP = "cpp"
    CS = "cs"
    CSS = "css"
    CSV = "csv"
    CXX = "cxx"
    DIFF = "diff"
    ERB = "erb"
    GROOVY = "groovy"
    H = "h"
    HAML = "haml"
    HH = "hh"
    HTM = "htm"
    HTML = "html"
    JAVA = "java"
    JS = "js"
    JSON = "json"
    LESS = "less"
    LOG = "log"
    M = "m"
    MAKE = "make"
    MD = "md"
    ML = "ml"
    MM = "mm"
    MSG = "msg"
    PHP = "php"
    PL = "pl"
    PROPERTIES = "properties"
    PY = "py"
    RB = "rb"
    RST = "rst"
    SASS = "sass"
    SCALA = "scala"
    SCM = "scm"
    SCRIPT = "script"
    SH = "sh"
    SML = "sml"
    SQL = "sql"
    TXT = "txt"
    VI = "vi"
    VIM = "vim"
    WEBDOC = "webdoc"
    XHTML = "xhtml"
    XLSB = "xlsb"
    XML = "xml"
    XSD = "xsd"
    XSL = "xsl"
    YAML = "yaml"
    GSLLIDE = "gslide"
    GSLIDES = "gslides"
    KEY = "key"
    ODP = "odp"
    PPT = "ppt"
    PPTX = "pptx"
    BOXNOTE = "boxnote"


class ImageFiles(Enum):
    """ImageFiles(Enum).

    An enum containing all of the supported extensions for files
    Box considers images.
    """

    ARW = "arw"
    BMP = "bmp"
    CR2 = "cr2"
    DCM = "dcm"
    DICM = "dicm"
    DICOM = "dicom"
    DNG = "dng"
    EPS = "eps"
    EXR = "exr"
    GIF = "gif"
    HEIC = "heic"
    INDD = "indd"
    INDML = "indml"
    INDT = "indt"
    INX = "inx"
    JPEG = "jpeg"
    JPG = "jpg"
    NEF = "nef"
    PNG = "png"
    SVG = "svg"
    TIF = "tif"
    TIFF = "tiff"
    TGA = "tga"
    SVS = "svs"


@dataclass
class BoxFileExtended:
    file: File
    text_representation: str = None
    ai_response: dict = None
