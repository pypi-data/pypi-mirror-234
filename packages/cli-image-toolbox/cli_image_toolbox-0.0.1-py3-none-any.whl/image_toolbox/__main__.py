import os
import logging
from typing import Iterable
import shutil
import datetime as dt
from PIL import Image
import typer


DEFAULT_DIR = "~/Pictures"
DEFAULT_FORMAT = "%Y%m%d"
DEFAULT_LEADING_ZEROS = 2


app = typer.Typer()


def get_timestamp(file: str) -> dt.datetime:
    image = Image.open(file)
    exifdata = image.getexif()
    timestamp = exifdata.get(36867)
    return dt.datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S")


def get_image_names(path: str = DEFAULT_DIR):
    return [f"{path}/{file}" for file in os.listdir(path) if file.endswith(".jpg")]


def sort_images(names: Iterable[str], timestamps: Iterable[dt.datetime]) -> dict[str, dt.datetime]:
    tuples = sorted(zip(timestamps, names))
    return {content[1]: content[0] for content in tuples}


def get_timestamps(files: Iterable[str]):
    timestamps = []
    for file in files:
        timestamps.append(get_timestamp(file))
    return timestamps


def get_new_names(files: dict[str, dt.datetime], format: str = DEFAULT_FORMAT, leading_zeros: int = DEFAULT_LEADING_ZEROS):
    j = 1
    previous_timestamp = None
    renaming = {}
    for old_name, timestamp in files.items():
        path = "/".join(old_name.split("/")[:-1])
        if previous_timestamp:
            if timestamp.day != previous_timestamp.day:
                j = 1
        new_name = timestamp.strftime(f"{format}{j:0>{leading_zeros}}.{old_name.split('.')[-1]}")
        new_name = f"{path}/{new_name}"
        j += 1
        renaming[old_name] = new_name
        previous_timestamp = timestamp
    return renaming


def rename_files(name_mapping: dict[str, str]) -> None:
    for old_name, new_name in name_mapping.items():
        shutil.move(old_name, new_name)


@app.command()
def rename_images(directory: str = DEFAULT_DIR, format: str = DEFAULT_FORMAT, leading_zeros: int = DEFAULT_LEADING_ZEROS) -> None:
    """
    Rename all images in a directory according to given input.

    Parameters
        directory {str} -- The directory where imsge nsmes are changed.
        format {str}
    """
    directory = directory.replace("~", os.environ["HOME"])
    image_names = get_image_names(directory)
    timestamps = get_timestamps(image_names)
    timestamp_mapping = sort_images(image_names, timestamps)
    name_mapping = get_new_names(timestamp_mapping, format=format, leading_zeros=leading_zeros)
    rename_files(name_mapping)
    print(f"renamed {len(name_mapping)} files")


if __name__ == "__main__":
    app()
