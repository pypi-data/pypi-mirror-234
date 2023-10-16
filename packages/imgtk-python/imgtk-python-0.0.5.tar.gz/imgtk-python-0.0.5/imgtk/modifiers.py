from typing import Type

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from pypipeline.constants import SEP
from pypipeline.item import Item
from pypipeline.modifier import Modifier
from stdl import fs

from imgtk.img import ImageItem


class ImageModifier(Modifier):
    description = ""


class Crop(ImageModifier):
    """
    Crop the image to the given box

    Args:
        x1 (int): The left edge of the box.
        y1 (int): The upper edge of the box.
        x2 (int): The right edge of the box.
        y2 (int): The lower edge of the box.

    """

    abbrev = "cr"

    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        super().__init__()
        self.box = (int(x1), int(y1), int(x2), int(y2))

    def process(self, img: ImageItem) -> Item:
        img._data = img.data.crop(self.box)
        return img

    @classmethod
    def parse(cls, val: str):
        p1, p2 = val.split(SEP)
        x1, y1 = p1.split(",")
        x2, y2 = p2.split(",")
        return cls(int(x1), int(y1), int(x2), int(y2))


class Convert(ImageModifier):
    """
    Convert the image to the given mode. Modes: [L, RGB, CMYK, GRAYSACLE]
    """

    abbrev = "cnv"

    MODES = ["L", "RGB", "CMYK", "GRAYSACLE"]

    def __init__(self, mode: str, colors=256) -> None:
        super().__init__()
        self.colors = colors
        mode = mode.upper()
        if mode == "GRAYSCALE":
            mode = "L"
        if not mode in self.MODES:
            raise ValueError(f"Invalid mode: {mode}. Valid modes: {', '.join(self.MODES)}")
        self.mode = mode

    def process(self, img: ImageItem) -> Item:
        img._data = img.data.convert(self.mode, colors=self.colors)
        return img

    @classmethod
    def parse(cls, val: str):
        return cls(val)


class Resize(ImageModifier):

    """
    Resize the image to the given size

    Args:
        width (int): The width of the image.
        height (int): The height of the image.
    """

    abbrev = "rs"

    def __init__(self, width: int | None = None, height: int | None = None) -> None:
        super().__init__()
        self.width = int(width) if width is not None else None
        self.height = int(height) if height is not None else None

    def process(self, img: ImageItem) -> Item:
        match (self.width, self.height):
            case (None, None):
                box = (img.data.width, img.data.height)
            case (None, h):
                box = (img.data.width, h)
            case (w, None):
                box = (w, img.data.height)
            case (w, h):
                box = (w, h)
            case _:
                raise ValueError((self.width, self.height))
        img._data = img.data.resize(size=box)  # type: ignore
        return img

    @classmethod
    def parse(cls, val: str):
        args = [int(i) for i in val.split(SEP) if i != ""]
        match args:
            case ["", ""]:
                return cls(None, None)
            case [w, ""]:
                return cls(int(w), None)
            case ["", h]:
                return cls(None, int(h))
            case [x, y]:
                return cls(int(x), int(y))
            case _:
                raise ValueError(args)


class Save(ImageModifier):
    """
    Save the image to the given directory
    """

    abbrev = "s"

    def __init__(self, directory: str) -> None:
        super().__init__()
        self.directory = directory

    def process(self, img: ImageItem) -> Item:
        filename = fs.basename(img.path)
        filepath = fs.joinpath(self.directory, filename)
        img.data.save(filepath)
        return img

    def validate(self) -> None:
        fs.assert_paths_exist(self.directory)


class Move(ImageModifier):
    """
    Move the image to the given directory
    """

    abbrev = "m"

    def __init__(self, directory: str) -> None:
        self.directory = directory
        super().__init__()

    def process(self, img: ImageItem) -> Item:
        img_file = fs.File(img.path).move_to(self.directory)
        img.path = img_file.path
        return img

    def validate(self) -> None:
        fs.assert_paths_exist(self.directory)


class Filter(ImageModifier):
    """
    Apply the given filter to the image. Filters: [blur, contour, detail, edge_enhance, edge_enhance_more, emboss, find_edges, sharpen, smooth, smooth_more]
    """

    abbrev = "f"
    filters = {
        f.name.upper().replace(" ", "_"): f
        for f in [
            ImageFilter.BLUR,
            ImageFilter.CONTOUR,
            ImageFilter.DETAIL,
            ImageFilter.EDGE_ENHANCE,
            ImageFilter.EDGE_ENHANCE_MORE,
            ImageFilter.EMBOSS,
            ImageFilter.FIND_EDGES,
            ImageFilter.SHARPEN,
            ImageFilter.SMOOTH,
            ImageFilter.SMOOTH_MORE,
        ]
    }

    def __init__(self, name: str) -> None:
        super().__init__()
        name = name.upper().replace(" ", "_")
        if not name in self.filters:
            raise ValueError(
                f"Invalid filter: {name}. Valid filters: {', '.join(self.filters.keys())}"
            )
        self.filter = self.filters[name]

    def process(self, img: ImageItem) -> Item:
        img._data = img.data.filter(self.filter)
        return img


class Rotate(ImageModifier):
    """
    Rotate the image by the given angle
    """

    abbrev = "rot"

    def __init__(self, angle: float) -> None:
        super().__init__()
        self.angle = float(angle)

    def process(self, img: ImageItem) -> Item:
        img._data = img.data.rotate(self.angle, expand=True)
        return img


class Scale(ImageModifier):
    """
    Scale the image by the given factor
    """

    abbrev = "sc"

    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def process(self, img: ImageItem) -> Item:
        img._data = img.data.resize((int(img.data.width * self.x), int(img.data.height * self.y)))
        return img

    @classmethod
    def parse(cls, val: str):
        args = [int(i) for i in val.split(SEP) if i != ""]
        if len(args) == 1:
            return cls(float(args[0]), float(args[0]))
        match args:
            case ["", ""]:
                raise ValueError(val)
            case [w, ""]:
                return cls(float(w), float(w))
            case ["", h]:
                return cls(float(h), float(h))
            case [x, y]:
                return cls(float(x), float(y))
            case _:
                raise ValueError(args)


class Threshold(ImageModifier):
    """
    Threshold filter to binarize an image
    """

    abbrev = "thr"

    def __init__(self, threshold: float) -> None:
        super().__init__()
        self.threshold = float(threshold)

    def process(self, img: ImageItem) -> Item:
        img._data = ImageOps.autocontrast(
            img.data.convert("L").point(lambda x: 0 if x < self.threshold else 255)
        )
        return img


class MedianBlur(ImageModifier):
    """
    Median blur filter to reduce noise in an image
    """

    abbrev = "mb"

    def __init__(self, radius: int) -> None:
        super().__init__()
        self.radius = int(radius)

    def process(self, img: ImageItem) -> Item:
        img._data = img.data.filter(ImageFilter.MedianFilter(self.radius))
        return img


class GaussianBlur(ImageModifier):
    """
    Gaussian blur filter to reduce noise in an image
    """

    abbrev = "gb"

    def __init__(self, radius: float) -> None:
        super().__init__()
        self.radius = float(radius)

    def process(self, img: ImageItem) -> Item:
        img._data = img.data.filter(ImageFilter.GaussianBlur(radius=self.radius))
        return img


class Invert(ImageModifier):
    """
    Invert filter to invert the colors of an image
    """

    abbrev = "inv"

    def process(self, img: ImageItem) -> Item:
        img._data = ImageOps.invert(img.data)
        return img


class Flip(ImageModifier):
    """
    Flip an image. Directions: [horizontal, vertical]
    """

    abbrev = "fl"
    directions = {"horizontal": Image.FLIP_LEFT_RIGHT, "vertical": Image.FLIP_TOP_BOTTOM}

    def __init__(self, direction: str) -> None:
        super().__init__()
        self.direction = direction.lower()

    def process(self, img: ImageItem) -> Item:
        img._data = img.data.transpose(self.directions[self.direction])  # type: ignore
        return img


class Contrast(ImageModifier):
    """
    Adjust the image contrast. Factor 1.0 always returns a copy of the original image, lower factors mean less color (brightness, contrast, etc), and higher values more.
    There are no restrictions on this value.
    """

    abbrev = "cont"

    def __init__(self, factor: float) -> None:
        super().__init__()
        self.factor = float(factor)

    def process(self, img: ImageItem) -> Item:
        img._data = ImageEnhance.Contrast(img.data).enhance(self.factor)
        return img


class Brightness(ImageModifier):
    """
    Adjust the image brightness.
    An enhancement factor of 0.0 gives a black image. A factor of 1.0 gives the original image.
    """

    abbrev = "brgh"

    def __init__(self, factor: float) -> None:
        super().__init__()
        self.factor = float(factor)

    def process(self, img: ImageItem) -> Item:
        img._data = ImageEnhance.Brightness(img.data).enhance(self.factor)
        return img


class Saturation(ImageModifier):
    """
    Adjust the colour balance of an image, in a manner similar to the controls on a colour TV set.
    An enhancement factor of 0.0 gives a black and white image. A factor of 1.0 gives the original image.
    """

    abbrev = "sat"

    def __init__(self, factor: float) -> None:
        super().__init__()
        self.factor = float(factor)

    def process(self, img: ImageItem) -> Item:
        img._data = ImageEnhance.Color(img.data).enhance(self.factor)
        return img


class Sharpness(ImageModifier):
    """
    Adjust the sharpness of the image.
    An enhancement factor of 0.0 gives a blurred image, a factor of 1.0 gives the original image, and a factor of 2.0 gives a sharpened image.
    """

    abbrev = "shrp"

    def __init__(self, factor: float) -> None:
        super().__init__()
        self.factor = float(factor)

    def process(self, img: ImageItem) -> Item:
        img._data = ImageEnhance.Sharpness(img._data).enhance(self.factor)
        return img


MODIFIERS: dict[str, Type[ImageModifier]] = {
    i.name: i
    for i in [
        Resize,
        Crop,
        Rotate,
        Scale,
        Filter,
        Flip,
        Convert,
        Invert,
        Threshold,
        Contrast,
        Brightness,
        Sharpness,
        Saturation,
        MedianBlur,
        GaussianBlur,
        Move,
        Save,
    ]
}
