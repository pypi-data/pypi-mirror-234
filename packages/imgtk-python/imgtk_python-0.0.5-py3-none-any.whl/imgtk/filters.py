import os

from PIL import ImageFilter
from pypipeline.filter import INT_MAX, SEP, Filter, FloatFilter, IntFilter, TextPatternFilter
from pytesseract import pytesseract
from stdl.fs import readable_size_to_bytes

from imgtk.img import ImageItem


class Width(IntFilter):
    """Filter by image width"""

    priority = 5
    abbrev = "w"

    def process(self, img: ImageItem) -> bool:
        return img.data.width in range(self.low, self.high)


class Height(IntFilter):
    """Filter by image height"""

    priority = 5
    abbrev = "h"

    def process(self, img: ImageItem) -> bool:
        return img.data.height in range(self.low, self.high)


class AspectRatio(FloatFilter):
    """Filter by aspect ratio"""

    priority = 5
    abbrev = "ar"

    def process(self, img: ImageItem) -> bool:
        image = img.data
        r = image.width / image.height
        return r > self.low and r < self.high


class Size(IntFilter):
    """Filter by file size"""

    priority = 1
    abbrev = "sz"

    def __init__(self, low=0, high=INT_MAX, invert=False) -> None:
        if isinstance(low, str):
            low = readable_size_to_bytes(low)
        if isinstance(high, str):
            high = readable_size_to_bytes(high)
        super().__init__(low, high, invert)

    def process(self, img: ImageItem) -> bool:
        return os.path.getsize(img.path) in range(self.low, self.high)

    @classmethod
    def parse(cls, val: str | None = None):
        if val is None or val == "":
            return cls()
        args = val.split(SEP)
        args = [i.strip() for i in args]
        args = [readable_size_to_bytes(i) if i != "" else i for i in args]
        match args:
            case ["", ""]:
                return cls()
            case [x, ""]:
                return cls(low=cls.t(x))
            case ["", x]:
                return cls(high=cls.t(x))
            case [x, y]:
                return cls(cls.t(x), cls.t(y))
            case _:
                raise ValueError(args)


class Filename(TextPatternFilter):
    """Filter by filename using glob or regex pattern matching"""

    priority = 1
    abbrev = "fn"

    def process(self, img: ImageItem) -> bool:
        return super().process(img.path)


class Text(TextPatternFilter):
    """
    Filter by text content using OCR using glob or regex pattern matching

    Args:
        pattern (str) : Text pattern to match. See TextPatternFilter for more info.
        language (str) : Language to use for OCR. See pytesseract docs for more info.
        psm (int) : Page segmentation mode. Run tesseract --help-psm for more info.
        inverted (bool): Invert the result of the filter.
        pattern_type (str): Type of pattern to use.
            Possible options: 'glob', 'regex' or None.
            If None, it will be guessed from the pattern.
    """

    priority = 6
    abbrev = "txt"

    def __init__(
        self,
        pattern: str,
        language=None,
        psm=3,
        invert=False,
        pattern_type=None,
    ) -> None:
        super().__init__(pattern, invert, pattern_type)
        self.language = language
        if psm not in range(0, 14):
            raise ValueError(f"Invalid psm value: {psm}")
        self.psm = psm

    def process(self, img: ImageItem) -> bool:
        if text := img.extra.get("text_content", None):
            return super().process(text)
        _img = img.data.copy()
        _img = _img.convert("L")
        _img = _img.filter(ImageFilter.MedianFilter())
        _img = _img.point(lambda x: 0 if x < 140 else 255)
        text = pytesseract.image_to_string(_img, lang=self.language, config=f"--psm {self.psm}")
        img.extra["text_content"] = text
        return super().process(text)


FILTERS: dict[str, Filter] = {
    i.__name__: i
    for i in [
        Width,
        Height,
        Size,
        AspectRatio,
        Filename,
        Text,
    ]
}
