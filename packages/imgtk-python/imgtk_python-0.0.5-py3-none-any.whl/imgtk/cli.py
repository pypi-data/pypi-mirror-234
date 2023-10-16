from glob import glob

from pypipeline import PyPipelineCLI
from stdl.fs import IMAGE_EXT, os, read_stdin, yield_files_in

from imgtk.filters import FILTERS
from imgtk.img import ImageItem
from imgtk.modifiers import MODIFIERS


def collect_files(items: list[str], ext=None, stdin=False):
    # if stdin:
    #    items.extend(read_stdin())

    for filepath in items:
        if os.path.isdir(filepath):
            for i in yield_files_in(filepath, ext):
                yield i
        elif os.path.isfile(filepath):
            if ext is None or filepath.endswith(ext):
                yield filepath
        elif "*" in filepath:
            for i in glob(filepath, recursive=True):
                if ext is None or i.endswith(ext):
                    yield i
        else:
            raise ValueError(f"invalid path: {filepath}")


class imgtkCLI(PyPipelineCLI):
    name = "imgtk"

    def collect_items(self, items: list[str]) -> list[ImageItem]:
        images = [ImageItem(i) for i in collect_files(items, IMAGE_EXT)]
        self.log_info(f"found {len(images)} images")
        return images


def cli():
    actions = [
        *[i for i in FILTERS.values() if i.is_parsable() or i.allow_autoparse],
        *[i for i in MODIFIERS.values() if i.is_parsable() or i.allow_autoparse],
    ]

    imgtkCLI(actions=actions)


if __name__ == "__main__":
    cli()

__all__ = ["cli", "imgtkCLI"]
