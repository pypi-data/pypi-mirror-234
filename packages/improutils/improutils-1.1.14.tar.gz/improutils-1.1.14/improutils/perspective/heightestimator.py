from .coordconversion import _calc_alfa_metric_factor
from .coordconversion import *

"""
Allows to estimate real world object height based on two points (top and bottom) measured
on image plane.
"""
class HeightEstimator:

    def __init__(self, ref_measurements, vl, vz):
        self._vanish_line = vl
        self._vert_vanish_point = vz
        self._alfa_metric_factor = _calc_alfa_metric_factor(ref_measurements, self._vanish_line,
                                                            self._vert_vanish_point)

    def calc_height(self, top_point, bottom_point):
        """
        Calculates real world height based on top_point and bottom_point measured
        on image plane.

        :param top_point: ndarray
            Top point in reference direction of the object in inhomogeneous format.
        :param bottom_point: ndarray
            Ground plane point of the object in inhomogeneous format.
        :return: float
            Scalar value representing real world height.
        """
        top_point = convert_pt_to_homogenous(top_point)
        bottom_point = convert_pt_to_homogenous(bottom_point)
        # This formula comes from paper Single view metrology by A. Criminisi.
        height = - np.linalg.norm(np.cross(bottom_point, top_point)) / (
                self._alfa_metric_factor * (np.dot(self._vanish_line, bottom_point)) * np.linalg.norm(
            np.cross(self._vert_vanish_point, top_point)))
        return height
