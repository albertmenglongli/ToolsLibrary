#!/usr/bin/env python3
import os
import shutil
from pathlib import Path
import subprocess
from typing import Optional, Set
import argparse
import sys

import imageio
import rawpy  # "brew install libraw" required in MacOS


def convert_cr2_to_jpg(file_paths: Optional[Set[Path]]):
    file_paths_converted = set()
    for file_path in file_paths:
        new_file_path = file_path.parent / (file_path.stem + '.JPG')

        with rawpy.imread(str(file_path)) as raw:
            try:
                thumb = raw.extract_thumb()
            except rawpy.LibRawNoThumbnailError:
                print('no thumbnail found')
                continue
            except rawpy.LibRawUnsupportedThumbnailError:
                print('unsupported thumbnail')
                continue
            else:
                if thumb.format == rawpy.ThumbFormat.JPEG:
                    # thumb.data is already in JPEG format, save as-is
                    with open(str(new_file_path), 'wb') as f:
                        f.write(thumb.data)
                elif thumb.format == rawpy.ThumbFormat.BITMAP:
                    # thumb.data is an RGB numpy array, convert with imageio
                    imageio.imsave(str(new_file_path), thumb.data)
                file_paths_converted.add(file_path)
    return file_paths_converted


def remove(path: Path):
    path = Path(path)
    path = str(path)
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))


def analyze_files_to_delete(file_paths: Optional[Set[Path]]):
    files_to_delete = set()
    all_file_names = set()

    for fp in file_paths:
        file_name = fp.name
        all_file_names.add(file_name)

    for fp in file_paths:
        if fp.name.endswith('CR2') and fp.stem + '.JPG' in all_file_names:
            files_to_delete.add(fp)

    return files_to_delete


def cmd_nouchg(file_path: Path):
    subprocess.run(f'chflags nouchg {str(file_path)}', shell=True, universal_newlines=True,
                   stdout=subprocess.PIPE, check=True)


def delete_file_paths(file_paths: Optional[Set[Path]]):
    for file_path in file_paths:
        try:
            remove(file_path)
        except PermissionError as e:
            cmd_nouchg(file_path)
            remove(file_path)


def parse_args():
    description = ("keep only preview file JPGs:"
                   "\t1. remove CR2 if JPG exists;"
                   "\t2. convert CR2 to JPG then remove CR2;")

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-d', '--dir', dest='dir_path', type=str, help='dir')

    args = parser.parse_args()
    return args


def entry(dir_path: Path):
    for root, sub_dirs, file_names in os.walk(dir_path):
        file_paths = set([Path(root) / file for file in file_names])
        file_paths_to_delete = analyze_files_to_delete(file_paths)
        file_paths_to_convert = set(filter(lambda __: __.name.endswith('CR2'),
                                           file_paths.difference(file_paths_to_delete)))
        file_paths_converted = convert_cr2_to_jpg(file_paths_to_convert)
        print(f'{len(file_paths_to_convert)} CR2 files converted!')
        file_paths_to_delete |= file_paths_converted
        delete_file_paths(file_paths_to_delete)
        print(f'{len(file_paths_to_delete)} CR2 files deleted!')


if __name__ == '__main__':
    args = parse_args()
    dir_path = args.dir_path
    dir_path = Path(dir_path)
    if not dir_path.exists():
        print(f'Invalid dir_path {dir_path}')
        sys.exit(1)
    if not dir_path.is_dir():
        print(f'Invalid dir_path {dir_path}')
        sys.exit(1)
    entry(dir_path=dir_path)
