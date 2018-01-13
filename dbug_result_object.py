from constants import *
from dbug_contour import DbugContour
from enum import Enum
from math import sqrt

class DBugResult(object):
    """
    This class represents the result of the image processing - the data that was extracted from the camera.
    This result can be later sent to the robot.
    """
    def __init__(self, result_object=None):

        self.result_object = result_object
        if result_object is None:
            self.azimuth_angle = UNABLE_TO_PROC_DEFAULT_VAL

        else:

            (x_cord, y_cord),(width, height), rotation_angle = self.result_object.rotated_enclosing_rectangle()

            self.result_type = self._get_result_type(width, height, rotation_angle)

            self.azimuth_angle = self._get_azimuth_angle(object_x_center=x_cord,
                                                               frame_width=RESIZE_IMAGE_WIDTH,
                                                               viewing_angle=CAMERA_VIEW_ANGLE_X)
            self.distance_from_camera = self._get_approximate_distance(width,
                                                                       height,
                                                                       BASE_1M_POWER_CUBE_BOUNDING_ROTATED_RECTANGLE_AREA)
            if self.distance_from_camera is None:
                self.distance_from_camera = UNABLE_TO_PROC_DEFAULT_VAL

            if self.azimuth_angle is None:
                self.azimuth_angle = UNABLE_TO_PROC_DEFAULT_VAL

    class ResultType(Enum):
        """
        Specifies the possible types of a DBugResult instance
        """
        unable_to_proc = "-"  # The vision was unable to process useful data
        single_power_cube = "S"  # The vision detected a single PowerCube in frame
        double_power_cube = "D"  # The vision detected 2 touching(!) PowerCubes in frame
        multiple_power_cubes = "M"  # The vision detected more than 2 touching(!) PowerCubes in frame

    def _get_result_type(self, object_width, object_height, rotation_angle):
        """
        :param object_width: object width in pixels
        :param object_height: object height in pixels
        :param rotation_angle: the rotation angle of the minimum enclosing rectangle.
        :return: The type of result object that self is, please refer to DBugResult.ResultType for type list and description
        """
        if self.result_object is None:
            return DBugResult.ResultType.unable_to_proc
        if rotation_angle < -45:  # When angle is less then -45 opencv switches between width and height
            ratio = float(object_height)/float(object_width)
        else:
            ratio = float(object_width)/float(object_height)

        if ratio <= SINGLE_POWER_CUBE_MAX_RATIO:
            return DBugResult.ResultType.single_power_cube
        elif ratio <= DOUBLE_POWER_CUBE_MAX_RATIO:
            return DBugResult.ResultType.double_power_cube
        else:
            return DBugResult.ResultType.multiple_power_cubes

    # MARK: Static methods

    def _get_azimuth_angle(self, object_x_center, frame_width, viewing_angle):
        """
        :param object_x_center: The center of the object in the x coord (top-left)
        :param frame_width: The frame width in pixels
        :param viewing_angle: The frame viewing angle - used to calculate the result in angles(degrees)
        :return: The azimuthal angle of center of frame to center of object
        """
        # if we have 2 power cubes we want to get the center of the first one, and not the center of both
        if self.result_type == DBugResult.ResultType.single_power_cube:
            ratio = 2.0
        elif self.result_type == DBugResult.ResultType.double_power_cube:
            ratio = 4.0
        else:
            return None
        return ((object_x_center - frame_width/ratio)/frame_width)*viewing_angle

    def _get_approximate_distance(self, object_width, object_height, area_1m_far):
        """
        :param object_width: The object width (in pixels) to calculate the area.
        :param object_height: The object height (in pixels) to calculate the area.
        :param area_1m_far: The area in pixels of the same object in a frame taken when the object is 1m from camera.
        :return: The approximate distance of the given object from the camera
        """
        if self.result_type == DBugResult.ResultType.single_power_cube:
            object_area = object_width * object_height
        elif self.result_type == DBugResult.ResultType.double_power_cube:
            object_area = (float(object_width)/2.0) * float(object_height)
        else:
            return None
        return sqrt(area_1m_far/object_area)  # sqrt because the ration is double the distance because the area is w*h

