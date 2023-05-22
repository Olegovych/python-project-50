#!/usr/bin/env python3
# import argparse
from gendiff.cli import get_args
from gendiff.differ import generate_diff


def main():
    file_path1, file_path2, formatter = get_args()
    difference = generate_diff(file_path1, file_path2, formatter)
    return difference


if __name__ == '__main__':
    main()
