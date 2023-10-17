import numpy as np

# Functions for conversion within different types of coordinates
def convert_pt_to_homogenous(pt):
    """
    Converts the input point from inhomogeneous coordinates to homogeneous ones.

    Parameters
    ----------
    pt : ndarray
        Input point in inhomogeneous coordinates.

    Returns
    -------
    _ : ndarray
        Input point in homogeneous coordinates.
    """
    return np.append(pt, np.array(1))

def convert_pt_from_homogenous(pt):
    """
    Convert input point in homogeneous coordinates to inhomogeneous.

    Parameters
    ----------
    pt : ndarray
        Input point in homogeneous coordinates.

    Returns
    -------
    _ : tuple
        Input point in inhomogeneous coordinates.
    """
    return tuple([elem / pt[-1] for elem in pt[:-1]])

def convert_pts_to_homogenous(pts):
    """
    Convert input points in inhomogeneous coordinates to homogeneous.

    :param pt: ndarray
        Input points in inhomogeneous coordinates.
    :return: ndarray
        Input points in homogeneous coordinates.
    """
    return np.array([convert_pt_to_homogenous(pt) for pt in pts])

def convert_pts_from_homogenous(pts):
    """
    Convert input points in homogeneous coordinates to inhomogeneous.

    :param pt: ndarray
        Input points in homogeneous coordinates.
    :return: ndarray
        Input points in inhomogeneous coordinates.
    """
    return np.array([convert_pt_from_homogenous(pt) for pt in pts])

def _calc_alfa_metric_factor(ref_measurements, vanish_line, vert_vanish_point):
    """
    Calculates alfa metric factor using multiple reference measurements via minimization ||As|| = 0. This is done by SVD.
        In depth overview can be found in https://www.robots.ox.ac.uk/~vgg/publications/1999/Criminisi99b/criminisi99b.pdf - PDF page 104.

    :param ref_measurements: list
        Each measurement is in (t_ref, b_ref, height) format. ``Image coordinates are in inhomogeneous format.
    :param vanish_line: ndarray
        Homogenous coordinates of vanishing line.
    :param vert_vanish_point: ndarray
        Homogenous coordinates of vanishing point in reference direction.
    :return: float
        Scalar value of alfa metric factor calculated by SVD.
    """
    matrix_A = np.empty((len(ref_measurements), 2), dtype='float64')

    for i, (t_ref, b_ref, h_ref) in enumerate(ref_measurements):
        t_ref = convert_pt_to_homogenous(t_ref)
        b_ref = convert_pt_to_homogenous(b_ref)
        beta = np.linalg.norm(np.cross(b_ref, t_ref))
        ro = np.dot(vanish_line, b_ref)
        gamma = np.linalg.norm(np.cross(vert_vanish_point, t_ref))
        matrix_A[i] = (h_ref * ro * gamma, beta)
        # alfa_metric_factor = - np.linalg.norm(np.cross(b_ref, t_ref)) / \
        #                               (h_ref * (np.dot(vanish_line, b_ref)) * np.linalg.norm(np.cross(vert_vanish_point, t_ref)))
        # print(alfa_metric_factor)

    u, s, vh = np.linalg.svd(matrix_A)
    return vh[0, -1] / vh[1, -1]
