"""
Unzip zipped photos from Google Album to specified directory.
"""
import os
import sys
from zipfile import ZipFile

SRC_DIR = os.path.join(input(('Source directory which only contains '
                              'zipped photos: ')).strip(), '')
if not os.path.exists(SRC_DIR):
    print('Error: source directory does not exist')
    sys.exit(1)
DEST_DIR = os.path.join(input(('Destination directory which only '
                               'contains zipped photo: ')).strip(), '')
if not os.path.exists(SRC_DIR):
    print('Error: destination directory does not exist')
    sys.exit(1)

ZIPPED_FILES = [f for f in os.listdir(SRC_DIR) if f.endswith('.zip')]
for filename in ZIPPED_FILES:
    with ZipFile(f'{SRC_DIR}{filename}', 'r') as zip_obj:
        # Extract all the contents of zip file in different directory
        zip_obj.extractall(DEST_DIR)
