import numpy as np
import cv2

def to_gray(img_bgr):
    """
    Converts image to monochrome

    Parameters
    ----------
    img : ndarray
        Input image.
    Returns
    -------
    Output image.
    """
    if len(img_bgr.shape) == 2:
        return img_bgr
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)


def to_hsv(img_bgr):
    """
    Converts image to HSV (hue, saturation, value) color space.

    Parameters
    ----------
    img : ndarray
        Input image.
    Returns
    -------
    Output image.
    """
    dst = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    return dst


def to_rgb(img_bgr):
    """
    Converts image to RGB (red, green, blue) color space from BGR.

    Parameters
    ----------
    img : ndarray
        Input image.
    Returns
    -------
    Output image.
    """
    dst = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return dst


def negative(img):
    """
    Converts image to its negative.

    Parameters
    ----------
    img : ndarray
        Input image.
    Returns
    -------
    Output image.
    """
    dst = 255 - img
    return dst


def normalize(img):
    """
    Normalizes image using min-max normalization from its values to values 0 - 255.

    Parameters
    ----------
    img : ndarray
        Input image.
    """
    return cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)


def normalize2BGR_image(img):
    """
    Normalizes image using min-max and converts it to BGR

    Parameters
    ----------
    img : ndarray
        Input image

    Returns
    -------
    _ : ndarray
        Normalized image in BGR
    """
    scaled = ((img - img.min()) * (1/(img.max() - img.min()) * 255)).astype('uint8')
    return cv2.cvtColor(scaled, cv2.COLOR_GRAY2BGR)


def crop(img, tl_x, tl_y, br_x, br_y):
    """
    Crops an image by added coordinates.

    Parameters
    ----------
    img : ndarray
        Input image.
    tl_x : int
        TOP-LEFT corner's x-coordinate
    tl_y : int
        TOP-LEFT corner's y-coordinate
    br_x : int
        BOTTOM-RIGHT corner's x-coordinate
    br_y : int
        BOTTOM-RIGHT corner's y-coordinate
    Returns
    -------
    Output image.
    """
    roi = img[tl_y:br_y, tl_x:br_x]
    return roi


def crop_by_bounding_rect(img_bin):
    """
    Crops binary image by ONE bounding rectangle corresponding to ALL objects in the binary image.

    Parameters
    ----------
    img_bin : ndarray
        Input binary image.
    Returns
    -------
    Output cropped image.
    """
    assert len(img_bin.shape) == 2, 'Input image is NOT binary!'

    contours, _ = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    tl_x, tl_y, w, h = cv2.boundingRect(contours[0])
    return crop(img_bin, tl_x, tl_y, tl_x + w, tl_y + h)


def crop_contour(contour, image):
    """ Crops contour in respect to its bounding rectangle.
    It's the fastest method, but could include other parts
    of image than just contour if the contour is irregulary shaped.

    Parameters
    ----------
    contour : ndarray
        Contour that represents the area from image to be cropped.
        The bounding rectangle of contour is used.
    img_bin : ndarray
        Input binary image.
    Returns
    -------
    Output cropped image.
    """
    x, y, w, h = cv2.boundingRect(contour)
    return image[y:y + h, x:x + w]


def resize(image, size, method=cv2.INTER_AREA):
    """
    Resizes the image to the preffered size.
    Method of resizing is well suited for making the images smaller rather than larger
    (cv2.INTER_AREA). For making images larger, use other cv2.INTER_### instead.

    Parameters
    ----------
    image : ndarray
        Contour that represents the area from image to be cropped.
    size : tuple
        New size of the resized image.
    method : int
        Optional argument. For more information see cv2.INTER_### parameters.
    Returns
    -------
    Output resized image.
    """
    assert type(size) is tuple, 'Variable size is NOT a tuple!'
    return cv2.resize(image, size, method)


def rotate(image, angle, image_center=None):
    """
    Rotates the input image by specified angle.

    Parameters
    ----------
    image : ndarray
        Image to be rotated.
    angle : float
        Rotation angle.
    image_center : Optional[tuple(int, int)]
        Center of rotation.
    Returns
    -------
    ndarray
        Returns the rotated input image by specified angle.
    """
    height, width = image.shape[:2]
    if image_center == None:
        image_center = (width / 2, height / 2)

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])

    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    rotation_mat[0, 2] += bound_w / 2 - image_center[0]
    rotation_mat[1, 2] += bound_h / 2 - image_center[1]

    dest = cv2.warpAffine(image, rotation_mat, (bound_w, bound_h))
    return dest

def polar_warp(img, full_radius=True, inverse=False):
    """
    Polar warp help function

    Parameters
    ----------
    img : TYPE
        Image to be rotated.
    full_radius : TYPE
    inverse : TYPE
    Returns
    -------
    TYPE
        DESCRIPTION.
    """
    center = (img.shape[0] / 2.0, img.shape[1] / 2.0)

    if full_radius:
        radius = np.sqrt(((img.shape[0] / 2.0) ** 2.0) + ((img.shape[1] / 2.0) ** 2.0))
    else:
        radius = center[0]

    method = cv2.WARP_FILL_OUTLIERS
    size = None
    if inverse:
        method += cv2.WARP_INVERSE_MAP
        size = img.shape[:2]
    dest = cv2.warpPolar(img, size, center, radius, method)
    return dest



def warp_to_cartesian(img, full_radius=True):
    return polar_warp(img, full_radius)


def warp_to_polar(img, full_radius=True):
    return polar_warp(img, full_radius, True)
