#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a directory path, search all files in the path for a given text string
within the 'word/document.xml' section of a MSWord .dotm file.
"""
__author__ = "Christine Santos and Instructor(demo)"

import os
import sys
import zipfile
import argparse

DOC_FILENAME = 'word/document.xml'


def scan_zipfile(z, search_text, full_path):
    with z.open(DOC_FILENAME, 'r') as doc:
        xml_text = doc.read()
    xml_text = xml_text.decode('utf8')
    text_location = line.find(search_text)
    if text_location >= 0:
        # match_count += 1
        print("Match found in file {}".format(full_path))
        print(' ...' + line[text_location-40:text_location+40] + '...')
        return True
    return False


def create_parser():
    parser = argparse.ArgumentParser(description="Searches for text within all dotm files in a directory")
    parser.add_argument('--dir', help='directory to search for dotm files', default='.')
    parser.add_argument('test', help='text to search within each dotm file')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    search_text = args.text
    search_path = args.dir

    if not search_text:
        parser.print_usage()
        sys.exit(1)

    print("Searching directory {} for dotm files with text '{}' ...")

    file_list = os.listdir(search_path)
    match_count = 0
    search_count = 0

    for file in file_list:

        if not file.endswith('.dotm'):
            print('Disregarding file: ' + file)
            continue
        else:
            search_count += 1

        full_path = os.path.join(search_path, file)

        if zipfile.is_zipfile(full_path):
            with zipfile.ZipFile(full_path) as z:
                names = z.namelist()
                if DOC_FILENAME in names:
                    if scan_zipfile(z, search_text, full_path):
                        match_count += 1
        else:
            print("Not a zipfile" + full_path)

    print("Total dotn files searched: {}".format(search_count))
    print("Total dotm files matched: {}".format(match_count))


if __name__ == '__main__':
    main()
