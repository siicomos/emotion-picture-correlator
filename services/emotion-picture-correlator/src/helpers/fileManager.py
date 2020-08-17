#!/bin/env python3

# Python version: 3.8.3
# Author: Liam Ling
# Contact: liam_ling@sfu.ca
# File name: fileManager.py
# Description:
"""This class implements useful functions of file manipulation and getting file information.
"""

import logging
import os
from pathlib import Path
from typing import Tuple, Union
import shutil
import sys
from urllib.parse import urlparse

import requests

logger = logging.getLogger(__name__)

# Type alias for paths or strings when either can be accepted
PathLike = Union[str, Path]


def cwd(_file: PathLike):
    return Path(_file).resolve()


def get_stem(path: PathLike):
    return Path(path).stem


def get_suffix(path: PathLike):
    return Path(path).suffix


def split_stem_and_suffix(path: PathLike) -> Tuple[str, str]:
    """Wrapper around getting the stem and the suffix that simply returns both items."""
    return get_stem(path), get_suffix(path)


def get_parent(path: PathLike):
    return Path(path).parent


def get_leaf_name(path: PathLike):
    return Path(path).name


def split_leaf_and_parent(path: PathLike) -> Tuple[Path, str]:
    """Wrapper around getting the parent and the leaf that simply returns both items."""
    return get_parent(path), get_leaf_name(path)


def join_path(path1: PathLike, *paths_to_join: PathLike):
    _path = Path(path1)
    return _path.joinpath(*paths_to_join).resolve()


def try_make_path(path: PathLike):
    _path = Path(path)
    _path.mkdir(mode=0o777, parents=True, exist_ok=True)
    os.chown(_path, os.getuid(), os.getgid())


def copy(origin_path: PathLike, target_path: PathLike):
    _path1 = Path(origin_path)
    _path2 = Path(target_path)
    shutil.copy(_path1.resolve(), _path2.resolve())


def rename(path: PathLike, target_name):
    _path = Path(path)
    if check_file(path) or check_path(path):
        target = _path.rename(target_name)
        if check_file(target) or check_path(target):
            return True
    return False


def check_file(path_to_file: PathLike):
    _file = Path(path_to_file)
    stat = True
    if not _file.exists():
        logger.debug(f"File doesn't exist: {path_to_file}")
        stat = False
    else:
        if _file.stat().st_size == 0:
            logger.debug(f"Given file is empty: {path_to_file}")
            stat = False
        if not _file.is_file():
            logger.debug(f"This is not a file: {path_to_file}")
            stat = False
    return stat


def check_path(path: PathLike):
    _path = Path(path)
    stat = True
    if path == "":
        stat = False
    elif not _path.exists():
        logger.debug(f"Path doesn't exist: {path}")
        stat = False
    else:
        if count_files(path) == 0:
            logger.debug(f"Given path is empty: {path}")
            stat = False
        if not _path.is_dir():
            logger.debug(f"This is not a path: {path}")
            stat = False
    return stat


def delete_file(path_to_file: PathLike):
    _file = Path(path_to_file)
    if check_file(path_to_file):
        _file.unlink()
        return not check_file(path_to_file)


def delete_path(path: PathLike):
    _path = Path(path)
    if check_path(path):
        shutil.rmtree(path)  # use shutil.rmtree to recursively remove directory
        if not check_path(path):
            return True
        else:
            return False


def download_file(url: str, save_path: PathLike, target_name: str = None):
    try_make_path(save_path)
    if target_name is None:
        try:
            path = Path(urlparse(url).path)
            target_name = path.name
        except Exception as e:
            logger.error(f"Exception caught: {e}")
    save_path_to_file = join_path(save_path, target_name)
    with open(save_path_to_file, "wb") as f:
        try:
            logger.info(f"Dowloading {save_path_to_file} ... ")
            response = requests.get(url, stream=True)
            total_length = response.headers.get("content-length")
            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ("=" * done, " " * (50 - done)))
                    sys.stdout.flush()
                sys.stdout.write("\n")
                sys.stdout.flush()
        except Exception as e:
            logger.error(f"Exception caught: {e}")

    return {
        "path": save_path_to_file,
        "request": {
            "status_code": response.status_code,
            "content_type": response.headers["content-type"],
            "encoding": response.encoding,
        },
    }


def walk_path(root: PathLike):
    _path = Path(root)
    objects = []
    empty_directories = []
    if _path.exists():
        if _path.is_dir():
            for path in _path.iterdir():
                if path.is_file():
                    objects.append(path)
                else:
                    sub_paths = [sub_path for sub_path in path.iterdir()]
                    if not sub_paths:
                        sub_objects, sub_empty_directories = walk_path(path)
                        objects.extend(sub_objects)
                        empty_directories.extend(sub_empty_directories)
                    else:
                        empty_directories.append(path)
        else:
            objects.append(_path)
    else:
        logger.error(f"{root} is not a valid path")
    return objects, empty_directories


def iterate_path(root: PathLike, recurse=False):
    _path = Path(root)
    # Use glob if recursive, otherwise use iterdir
    objects = _path.rglob("*") if recurse else _path.iterdir()
    for path in objects:
        yield path


def list_folders(root: PathLike, recurse=False):
    return [path for path in iterate_path(root, recurse=recurse) if path.is_dir()]


def list_files(root: PathLike, recurse=False):
    return [path for path in iterate_path(root, recurse=recurse) if path.is_file()]


def count_files(root: PathLike):
    return len([path for path in iterate_path(root)])
