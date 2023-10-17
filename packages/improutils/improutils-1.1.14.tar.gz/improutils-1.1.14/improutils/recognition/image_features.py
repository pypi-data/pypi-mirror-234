import numpy as np
import cv2

# Dimensionless descriptors
from improutils import find_contours


class ShapeDescriptors:
    """
    An internal class for shape descriptors.
    If you are an user, you shall not call not nor work with the class directly
    """
    def form_factor(area, perimeter):
        return (4 * np.pi * area) / (perimeter * perimeter)

    def roundness(area, max_diameter):
        return (4 * area) / (np.pi * max_diameter * max_diameter)

    def aspect_ratio(min_diameter, max_diameter):
        return min_diameter / max_diameter;

    def convexity(perimeter, convex_perimeter):
        return convex_perimeter / perimeter

    def solidity(area, convex_area):
        return area / convex_area

    def compactness(area, max_diameter):
        return np.sqrt(4 / np.pi * area) / max_diameter;

    def extent(area, bounding_rectangle_area):
        return area / bounding_rectangle_area;

"""
An internal, helper function.
Shall not be called directly by the user.
This can perform a check for contour validity.

Right now, there is no check for validity, and the function does nothing.

If the contour would be invalid, a ValueError shall be risen

Parameters
----------
contour : ndarray
    One contour.

Returns
-------

Throws
-------
_ : a ValueError exception if ???
"""
def _validateContourGiven(contour):
    return;

"""
Aka Špičatost.
Allows to determine the form factor of the contour given
Parameters
----------
contour : ndarray
    The contour. You can get it by calling
    _, _, contours = improutils.find_contours()
    Then that one contours is contours[i] where i is index of your choice.

Returns
-------
_ : number
    The number, describing the contour property

"""
def form_factor(contour):
    _validateContourGiven(contour)
    return ShapeDescriptors.form_factor(cv2.contourArea(contour), cv2.arcLength(contour, True))

"""
Allows to determine the roundness of the contour given
Parameters
----------
contour : ndarray
    The contour. You can get it by calling
    _, _, contours = improutils.find_contours()
    Then that one contours is contours[i] where i is index of your choice.

Returns
-------
_ : number
    The number, describing the contour property

"""
def roundness(contour):
    _validateContourGiven(contour)
    area = cv2.contourArea(contour)
    _, radius = cv2.minEnclosingCircle(contour)
    r = ShapeDescriptors.roundness(area, 2 * radius)
    if r > 1:
        r = 1
    return r

"""
Allows to determine the aspect ratio of the contour given
Parameters
----------
contour : ndarray
    The contour. You can get it by calling
    _, _, contours = improutils.find_contours()
    Then that one contours is contours[i] where i is index of your choice.

Returns
-------
_ : number
    The number, describing the contour property

"""
def aspect_ratio(contour):
    _validateContourGiven(contour)
    dims = cv2.minAreaRect(contour)[1]
    min_diameter = min(dims)
    max_diameter = max(dims)
    return ShapeDescriptors.aspect_ratio(min_diameter, max_diameter)


"""
Allows to determine the convexity of the contour given
Parameters
----------
contour : ndarray
    The contour. You can get it by calling
    _, _, contours = improutils.find_contours()
    Then that one contours is contours[i] where i is index of your choice.

Returns
-------
_ : number
    The number, describing the contour property

"""
def convexity(contour):
    _validateContourGiven(contour)
    hull = cv2.convexHull(contour, None, True, True)
    per = cv2.arcLength(contour, True)
    conv_per = cv2.arcLength(hull, True)
    r = ShapeDescriptors.convexity(per, conv_per)
    if r > 1:
        r = 1
    return r


"""
Allows to determine the solidity of the contour given
Parameters
----------
contour : ndarray
    The contour. You can get it by calling
    _, _, contours = improutils.find_contours()
    Then that one contours is contours[i] where i is index of your choice.

Returns
-------
_ : number
    The number, describing the contour property

"""
def solidity(contour):
    _validateContourGiven(contour)
    hull = cv2.convexHull(contour, None, True, True)
    area = cv2.contourArea(contour)
    conv_area = cv2.contourArea(hull)
    r = ShapeDescriptors.solidity(area, conv_area)
    if r > 1: r = 1
    return r


"""
Allows to determine the compactness of the contour given
Parameters
----------
contour : ndarray
    The contour. You can get it by calling
    _, _, contours = improutils.find_contours()
    Then that one contours is contours[i] where i is index of your choice.

Returns
-------
_ : number
    The number, describing the contour property

"""
def compactness(contour):
    _validateContourGiven(contour)
    area = cv2.contourArea(contour)
    max_diameter = max(cv2.minAreaRect(contour)[1])
    r = ShapeDescriptors.compactness(area, max_diameter)
    if r > 1: r = 1
    return r


"""
Allows to determine the extent of the contour given
Parameters
----------
contour : ndarray
    binary image. This image contains only black and white values.
    Traditionally, you get it from the segmentation process.

Returns
-------
_ : number
    The number, describing the contour property

"""
def extent(contour):
    _validateContourGiven(contour)
    area = cv2.contourArea(contour)
    w, h = cv2.minAreaRect(contour)[1]
    return ShapeDescriptors.extent(area, w * h)
