import numpy as np
import cv2
import os

def midpoint(ptA, ptB):
    """
    Returns the midpoint between two input 2D points.

    Parameters
    ----------
    ptA : array | tuple | ndarray
        The first 2D point considered
    ptA : array | tuple | ndarray
        The second 2D point considered

    Returns
    -------
    _ : tuple
        The 2D midpoint

    Throws
    -------
    _ : a ValueError exception if
        [+] Any of the given input points are not 2D.
        That means, the length of the structure (array|tuple|ndarray)
        is not equal to 2
    """

    if(len(ptA) != 2 or len(ptB) != 2):
        raise ValueError("Ivalid input point format");
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def artificial_circle_image(size):
    """
    Creates an image with circles
    Parameters
    ----------
    size : int
        size of the image

    Returns
    -------
    _ : ndarray
        artificial image with circles
    Throws
    -------
    _ : a ValueError exception if any of the following contitions hold:
        [+] The input size is not an integer type
        [+] The input size is smaller than 1 (< 1)
    """
    if isinstance(size, int):
        raise ValueError("Ivalid input size. Integer required. got {}".format(type(size)));
    if size < 1:
        raise ValueError("Ivalid input size, must be >= 0. Got {}".format(size));

    img_art_circ = np.zeros((size, size), dtype=np.uint8)
    step = 10
    for i in range(step, size, step):
        cv2.circle(img_art_circ, (int(size / 2.0), int(size / 2.0)), i - step, np.random.randint(0, 255), thickness=4)
    return img_art_circ


def order_points(pts):
    """
    Sorts the points based on their coordinates,
    in top-left, top-right, bottom-right, and bottom-left order

    Parameters
    ----------
    pts : ndarray
        2D Points to be sorted.
        The points are expected to be in 2D cartesian plane coordinates.
        Must be type of ndarray.
        Must have length of 4 or more.

        Each element of the array is expected to be an ARRAY,
        containing exactly 2 elements, specifying the x and y, respectivelly

        If the content of the ndarray provided is not in the expected format,
        the behavior is not defined.

    Returns
    -------
    _ : ndarray
        sorted points, the coordinates in top-left, top-right, bottom-right, and bottom-left order
    Throws
    -------
    _ : a ValueError exception if any of the following contitions hold:
        [+] The input is not of an ndarray type
        [+] The input ndarray does have length below 4 (< 4)
        [+] The element (point) in the input ndarray does not have the dimension exactly of 2
    """

    if(not isinstance(pts, np.ndarray)):
        raise ValueError("Ivalid input point format. Numpy ndarray expected. Got {}".format(type(pts)));

    if(len(pts) < 4):
        raise ValueError("Ivalid amount of input points. Got {} elements".format(len(pts)));

    #understanding, that creating an NP array where not all elements have the same length
    #prints a warning thanks to python by itself,
    #we just check for the first element, and assume that they all have the same length
    if(len(pts[0]) != 2):
        raise ValueError("Ivalid input point format. For a point, dimension of 2 expected. got {}".format(len(pts[0])));


    xSorted = pts[np.argsort(pts[:, 0]), :]

    # grab the left-most and right-most points from the sorted
    # x-roodinate points
    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]

    # now, sort the left-most coordinates according to their
    # y-coordinates so we can grab the top-left and bottom-left
    # points, respectively
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (bl, tl) = leftMost

    # now that we have the top-left coordinate, use it as an
    # anchor to calculate the Euclidean distance between the
    # top-left and right-most points; by the Pythagorean
    # theorem, the point with the largest distance will be
    # our bottom-right point
    rightMost = rightMost[np.argsort(rightMost[:, 1]), :]
    (br, tr) = rightMost

    # return the coordinates in top-left, top-right,
    # bottom-right, and bottom-left order
    return np.array([tl, tr, br, bl], dtype="float32")


def pcd_to_depth(pcd, height, width):
    """
    Reduce point-cloud to coordinates, point cloud [x, y, z, rgb] -> depth[x, y, z]

    Parameters
    ----------
    pcd : array
        point cloud
    height : int
        height of captured img
    width : int
        width of a captured img
    Returns
    ----------
    _ : array
        coordinates
    """
    data = pcd
    data = [float(x.split(' ')[2]) for x in data]
    data = np.reshape(data, (height, width))
    return data

def create_file_path(folder, file_name):
    """
    Easier defined function to create path for filename inside a folder.
    Parameters
    ----------
    folder : string
        Base folder directory in string notation.
        If the directory does not exist, it is created.

    file_name : string
        File name that should be inside the base folder.
    Returns
    -------
    string
        Path to the file.
    """
    if not os.path.isdir(folder):
        os.mkdir(folder)

    return os.path.join(folder, file_name)
