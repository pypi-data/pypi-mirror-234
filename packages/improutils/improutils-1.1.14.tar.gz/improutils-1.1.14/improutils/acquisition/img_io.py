import os

import numpy as np
import cv2

import re
from natsort import natsorted
import shutil


def load_image(file_path):
    """
    Loads an image from a file.

    The function calls cv2.imread() to load image from the specified file
    and then return it. If the image cannot be read, the AssertError exception is thrown.

    For more info about formats, see cv2.imread() documentation

    Parameters
    ----------
    file_path : string
        A path to an image file
    Returns
    -------
    Loaded image in numpy.ndarray
    """
    assert os.path.exists(file_path), 'File does NOT exist! (' + file_path + ')'
    return cv2.imread(file_path)


def save_image(image, file_path):
    """
    Save an image to a file.

    The function calls cv2.imwrite() to save an image to the specified file. The image format is chosen based on the
    filename extension.

    Parameters
    ----------
    image : numpy.ndarray
        Pixel values
    file_path : string
        A path to an image file
    Returns
    -------
    True if image is saved successfully
    """
    return cv2.imwrite(file_path, image)


def copy_to(src, dst, mask):
    """
    Copies source image pixel to destination image using mask matrix.

    This function is Python alternative to C++/Java OpenCV's Mat.copyTo().
    More: https://docs.opencv.org/trunk/d3/d63/classcv_1_1Mat.html#a626fe5f96d02525e2604d2ad46dd574f

    Parameters
    ----------
    src : numpy.ndarray
        Source image
    dst : numpy.ndarray
        Destination image
    mask : numpy.ndarray
        Binary image that specifies which pixels are copied. Value 1 means true
    Returns
    -------
    Destination image with copied pixels from source image
    """
    locs = np.where(mask != 0)  # Get the non-zero mask locations
    dst[locs[0], locs[1]] = src[locs[0], locs[1]]
    return dst

def reindex_image_files(source_dir, output_dir=None):
    """ Reads all images in source_dir and based on they original order,
    change their filename to be continuous integer (starting from 0).
    Then, they can be easily read by cv2.VideoCapture. Image format is kept.

    Parameters
    ----------
    source_dir : string
        Input images directory that have to be renamed.
    output_dir : Optional[string]
        Output directory for renamed files. If not specified, renaming is done inplace in source_dir.
    Returns
    -------
    None
    """
    input_files = []

    for file in os.listdir(source_dir):
        if re.match(r'.*(\.bmp|\.jpg|\.png|\.gif)$', file, re.I):
            input_files.append(os.path.join(source_dir, file))

    if not input_files:
        print('No files were found.')
        return

    extension = '.' + input_files[0].split(".")[-1]
    if output_dir is None:
        for i, filename in enumerate(natsorted(input_files)):
            os.rename(filename, os.path.join(source_dir, str(i) + extension))
        print(f'Files within {source_dir} were renamed, starting from 0{extension} to {i}{extension}.')
    else:
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        for i, filename in enumerate(natsorted(input_files)):
            shutil.copy(filename, os.path.join(output_dir, str(i) + extension))

        print(
            f'Files from {source_dir} were renamed and saved to {output_dir}, starting from 0{extension} to {i}{extension}.')
