import os
import sys
import shutil
import argparse
from typing import Iterable
import logging
import datetime as dt
from PIL import Image


def _set_logger():
    """Set logger to utput to stdout."""
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


def _parse_args():
    """ "Parse cli arguments"""
    parser = argparse.ArgumentParser(
        prog="ProgramName",
        description="What the program does",
        epilog="Text at the bottom of help",
    )
    parser.add_argument(
        "-d", "--directory", type=str, required=False, default="~/Pictures"
    )
    parser.add_argument("-f", "--format", type=str, required=False, default="%Y%m%d")
    parser.add_argument("-z", "--zeros", type=int, required=False, default=2)
    args = parser.parse_args()
    return args


def _get_timestamp(file: str) -> dt.datetime:
    """Get timestamp for image."""
    image = Image.open(file)
    exifdata = image.getexif()
    timestamp = exifdata.get(36867)
    return dt.datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S")


def _get_image_names(path: str):
    """Get all image filenames in a directory."""
    return [f"{path}/{file}" for file in os.listdir(path) if file.endswith(".jpg")]


def _sort_images(
    names: Iterable[str], timestamps: Iterable[dt.datetime]
) -> dict[str, dt.datetime]:
    """Sort image filenames based on timestamps."""
    tuples = sorted(zip(timestamps, names))
    return {content[1]: content[0] for content in tuples}


def _get_timestamps(files: Iterable[str]):
    """Get timestamp for all images."""
    timestamps = []
    for file in files:
        timestamps.append(_get_timestamp(file))
    return timestamps


def _get_new_names(files: dict[str, dt.datetime], format: str, leading_zeros: int):
    """Get new image names based on format."""
    j = 1
    previous_timestamp = None
    renaming = {}
    for old_name, timestamp in files.items():
        path = "/".join(old_name.split("/")[:-1])
        if previous_timestamp:
            if timestamp.day != previous_timestamp.day:
                j = 1
        new_name = timestamp.strftime(
            f"{format}{j:0>{leading_zeros}}.{old_name.split('.')[-1]}"
        )
        new_name = f"{path}/{new_name}"
        j += 1
        renaming[old_name] = new_name
        previous_timestamp = timestamp
    return renaming


def _rename_files(name_mapping: dict[str, str]) -> None:
    """Rename files."""
    for old_name, new_name in name_mapping.items():
        shutil.move(old_name, new_name)


def rename_images() -> None:
    """Rename all images in a directory according to given input."""
    args = _parse_args()
    directory = args.directory
    format = args.format
    leading_zeros = args.zeros
    log = _set_logger()
    directory_py = directory.replace("~", os.environ["HOME"])
    image_names = _get_image_names(directory_py)
    timestamps = _get_timestamps(image_names)
    timestamp_mapping = _sort_images(image_names, timestamps)
    name_mapping = _get_new_names(
        timestamp_mapping, format=format, leading_zeros=leading_zeros
    )
    _rename_files(name_mapping)
    images = len(name_mapping)
    log.info(f"Finished renaming images: ({directory=}) - ({images=})")
