from constants import *
from dbug_contour import DbugContour


class DBugResult(object):
    """
    This class represents the result of the image processing - the data that was extracted from the camera.
    This result can be later sent to the robot.
    """
    def __init__(self, result_object=None):

        if result_object is None:
            self.azimuth_angle = UNABLE_TO_PROC_DEFAULT_VAL

        else:
            self.result_object = result_object

            (x_cord, y_cord) = self.result_object.rotated_enclosing_rectangle()[0]
            self.azimuth_angle = DBugResult._get_azimuth_angle(object_x_center=x_cord,
                                                               frame_width=RESIZE_IMAGE_WIDTH,
                                                               viewing_angle=CAMERA_VIEW_ANGLE_X)

    @staticmethod
    def _get_azimuth_angle(object_x_center,
                           frame_width,
                           viewing_angle):
        """
        :param object_x_center: The center of the object in the x coord (top-left)
        :param frame_width: The frame width in pixels
        :param viewing_angle: The frame viewing angle - used to calculate the result in angles(degrees)
        :return: The azimuthal angle of center of frame to center of object
        """
        return ((object_x_center - frame_width/2.0)/frame_width)*viewing_angle

    @staticmethod
    def _get_approxiamte_distance(object_area, area_1m_far):
        """

        :param object_area:
        :param area_1m_far:
        :return:
        """
