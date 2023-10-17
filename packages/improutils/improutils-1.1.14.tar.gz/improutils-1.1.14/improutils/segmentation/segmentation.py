import numpy as np
import cv2

def apply_mask(img, mask_bin):
    """
    Masks colored image with binary mask. Output image is just logical AND between two images.
    """
    return cv2.bitwise_and(img, img, mask=mask_bin)


def logical_and(bin_im, bin_mask):
    return cv2.bitwise_and(bin_im, bin_mask)


def to_intensity(hue_angle):
    """
    Converts color angle in HUE definition into intensity value of brightness image in opencv.
    https://www.docs.opencv.org/trunk/df/d9d/tutorial_py_colorspaces.html

    Parameters
    ----------
    hue_angle : int
        Angle in HUE definition (0-359).
    Returns
    -------
    Integer value that represents the same HUE value but in opencv brightness image (0-179).
    """
    return int(hue_angle * 0.5)


def to_angle(hue_intensity):
    """
    Converts hue intensity value of brightness image in opencv into hue angle in HUE definition.
    https://www.docs.opencv.org/trunk/df/d9d/tutorial_py_colorspaces.html

    Parameters
    ----------
    hue_intensity : int
        Intensity value of brightness image (0-179).
    Returns
    -------
    Integer value that represents the HUE angle (0-359).
    """
    return hue_intensity * 2


def to_3_channels(image):
    """
    Converts 1 channel image to 3 channels.
    """
    if len(image.shape) == 3:
        raise Exception('Image already has 3 channels! Use it on binary or grayscale image only.')
    return cv2.merge([image, image, image])


def segmentation_one_threshold(img, threshold):
    """
    Segments image into black & white using one threshold

    Parameters
    ----------
    img : ndarray
        Input image.
    threshold : int
        Pixels with value lower than threshold are considered black, the others white.
    Returns
    -------
    Output image.
    """
    _, dst = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    return dst


def segmentation_auto_threshold(img):
    """
    Segments image into black & white using automatic threshold

    Parameters
    ----------
    img : ndarray
        Input image.
    Returns
    -------
    Output image.
    """
    _, dst = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return dst


def segmentation_two_thresholds(img, lower, higher):
    """
    Segments image into black & white using two thresholds

    Parameters
    ----------
    img : ndarray
        Input image.
    lower : int
        Pixels with value lower than threshold are considered black, the others white.
    higher : int
        Pixels with value higher than threshold are considered black, the others white.
    Returns
    -------
    Output image.
    """
    return cv2.inRange(img, min(lower, higher), max(lower, higher))


def segmentation_adaptive_threshold(img, size, constant=0):
    """
    Segments image into black & white using calculated adaptive
    threshold using Gaussian function in pixel neighbourhood.

    Parameters
    ----------
    img : ndarray
        Input image.
    size : int
        Size of used gaussian. Lowest value is 3. Algorithm uses only odd numbers.
    constant : int
        Value that is added to calculated threshlod. It could be negative as well as zero as well as positive number.
    Returns
    -------
    img : ndarray
        Output binary image.
    """
    if size < 3:
        size = 3
    elif size % 2 == 0:
        size -= 1
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, size, int(constant))
