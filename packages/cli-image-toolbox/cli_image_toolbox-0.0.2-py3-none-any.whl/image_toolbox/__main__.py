import os
import sys
import shutil
import argparse
from typing import Iterable
import logging
import datetime as dt
from PIL import Image


def set_logger():
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


def parse_args():
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help'
    )
    parser.add_argument("-d", "--directory", type=str, required=False, default="~/Pictures")
    parser.add_argument("-f", "--format", type=str, required=False, default="%Y%m%d")
    parser.add_argument("-z", "--zeros", type=int, required=False, default=2)
    args = parser.parse_args()
    return args


def get_timestamp(file: str) -> dt.datetime:
    image = Image.open(file)
    exifdata = image.getexif()
    timestamp = exifdata.get(36867)
    return dt.datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S")


def get_image_names(path: str):
    return [f"{path}/{file}" for file in os.listdir(path) if file.endswith(".jpg")]


def sort_images(names: Iterable[str], timestamps: Iterable[dt.datetime]) -> dict[str, dt.datetime]:
    tuples = sorted(zip(timestamps, names))
    return {content[1]: content[0] for content in tuples}


def get_timestamps(files: Iterable[str]):
    timestamps = []
    for file in files:
        timestamps.append(get_timestamp(file))
    return timestamps


def get_new_names(files: dict[str, dt.datetime], format: str, leading_zeros: int):
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


def rename_images() -> None:
    """
    Rename all images in a directory according to given input.
    """
    args = parse_args()
    directory = args.directory
    format = args.format
    leading_zeros = args.zeros
    log = set_logger()
    directory_py = directory.replace("~", os.environ["HOME"])
    image_names = get_image_names(directory_py)
    timestamps = get_timestamps(image_names)
    timestamp_mapping = sort_images(image_names, timestamps)
    name_mapping = get_new_names(timestamp_mapping, format=format, leading_zeros=leading_zeros)
    rename_files(name_mapping)
    images = len(name_mapping)
    log.info(f"Finished renaming files: ({directory=}) - ({images=})")
