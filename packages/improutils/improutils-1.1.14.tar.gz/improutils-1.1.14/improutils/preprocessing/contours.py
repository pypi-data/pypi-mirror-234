import numpy as np
import cv2

def contour_to_image(contour, image, size=None):
    """
    Creates a new image from the contour.
    It's similar to contour cropping but it's not that fast.
    It does not suffer from the known error if the contour is irregulary shaped.

    Parameters
    ----------
    contour : ndarray
        Contour that represents the area from image to be cropped.
    img_bin : ndarray
        Input binary image.
    size : tuple
        Optional size of the created image.
        If it's not used, the image's size is the same as the
        size of bounding rectangle of the input contour.
    Returns
    -------
    Output cropped image.
    """

    if size is None:
        _, _, w, h = cv2.boundingRect(contour)
        size = (w, h)

    assert type(size) is tuple, 'Param size should be a tuple!'
    blank = np.zeros_like(image)
    half_x = int(size[0] * 0.5)
    half_y = int(size[1] * 0.5)

    c = get_center(contour)
    cv2.drawContours(blank, [contour], -1, (255, 255, 255), cv2.FILLED)

    return blank[c[1] - half_y:c[1] + half_y, c[0] - half_x:c[0] + half_x].copy()


def find_contours(img_bin, min_area=0, max_area=np.inf, fill=True, external=True):
    """
    Finds contours in binary image and filters them using their area. Then it draws binary image
    from filtered contours. It counts contours as well.

    Parameters
    ----------
    img_bin : ndarray
        Input binary image.
    min_area : int
        Size of contour that is used to filter all smaller contours out.
    max_area : int
        Size of contour that is used to filter all larger contours out.
    Returns
    -------
    contour_drawn : ndarray
        Output binary image with drawn filled filtered contours.
    count : int
        Number of found and filtered contours.
    contours : list
        Found contours.
    """
    mode = cv2.RETR_EXTERNAL
    if not external:
        mode = cv2.RETR_LIST
    contours, _ = cv2.findContours(img_bin, mode, cv2.CHAIN_APPROX_SIMPLE)
    contours = [c for c in contours if cv2.contourArea(c) > min_area and cv2.contourArea(c) < max_area]
    thick = cv2.FILLED
    if not fill: thick = 2
    contour_drawn = cv2.drawContours(np.zeros(img_bin.shape, dtype=np.uint8), contours, -1, color=(255, 255, 255),
                                     thickness=thick)
    return contour_drawn, len(contours), contours


def fill_holes(img_bin, close=False, size=5):
    """
    Fill the holes in found contours. It could merge the contour using close input with appropriate size.

    Parameters
    ----------
    img_bin : ndarray
        Input binary image.
    close : boolean
        If it should merge contours with missing points using close operation.
    size : int
        Size of the close operation element.
    Returns
    -------
    Output binary image.
    """
    if close:
        struct = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
        img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, struct)
    res, _, _ = find_contours(img_bin)
    return res


def get_center(contour):
    """
    Gets the center of a contour in pixels in tuple format.

    Parameters
    ----------
    contour : ndarray
        input contour.
    Returns
    -------
    _ : tuple
        Center in pixels in tuple format.
    """
    M = cv2.moments(contour)
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])

    return cX, cY
