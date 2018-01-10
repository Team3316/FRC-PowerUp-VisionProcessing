from cv2 import boundingRect
from cv2 import contourArea
from cv2 import minAreaRect
from numpy import vstack


class DbugContour(object):
    """
    The Dbug rapper for a cv2 contour
    """
    def __init__(self, cv_contour):
        """
        :param cv_contour: The cv2 contour that self is wrapping
        """
        self.contour = cv_contour

    def straight_enclosing_rectangle(self):
        """
        Calculates and returns the (straight-no angle) bounding rectangle of the contour self is wrapping
        :return: (x,y,w,h), Let (x,y) be the top-left coordinate of the rectangle and (w,h) be its width and height.
        """
        return boundingRect(self.contour)

    def contour_area(self):
        """
        :return: The number of non-zero pixels in the contour self is wrapping
        """
        return contourArea(self.contour)

    def rotated_enclosing_rectangle(self):
        """
        :return: The minimum enclosing bounding rectangle of the contour self is wrapping.
                 Tuple of center (x,y), (width, height), angle of rotation.
        """
        return minAreaRect(self.contour)

    def min_rotated_enclosing_rectangle_angle(self):
        """
        :return: The rotation angle of the minimum enclosing bounding rectangle of the contour self is wrapping
        """
        return self.rotated_enclosing_rectangle()[2]

    def __add__(self, other):
        """
        :return: One contour which is the merger of self, other (holds both of their points)
        """
        cont = vstack([self.contour, other.contour])
        return DbugContour(cv_contour=cont)
