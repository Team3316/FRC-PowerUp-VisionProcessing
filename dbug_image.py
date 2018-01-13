from dbug_contour import DbugContour
import cv2
import numpy as np


class DBugAbstractImage(object):
    """
    The mother class of an image (e.g: frame taken from a camera), all types of images should inherit from
    this class.
    """

    def __init__(self, cv2_image):
        """
        :param cv2_image: The image (a CV2 image, which is a numpy array) this instance will represent
        """
        self.image = cv2_image

    def copy(self):
        """
        :return: a copy of self - a new image with the exact same pixels
        """
        return self.__class__(cv2_image=self.image.copy())

    def display_gui_window(self, window_title):
        """
        Opens a graphic window with the give title presenting self
        :param window_title: The title of the gui window
        :return: None
        """
        cv2.imshow(window_title, self.image)

    def save_to_path(self, path):
        """
        :param path: The relative path to save the image in self to
        :return: None
        """
        cv2.imwrite(path, self.image)


class DBugColorImage(DBugAbstractImage):
    """
    a DBugColorImage instance represents an image with colors.
    This class helps interact and extract data from the underling image represented as an OpenCV image.
    """

    def filter_with_colors(self, lower_thresh, upper_thresh):
        """
        Filters self.image with the given hsv thresh values
        :param lower_thresh: the lower hsv thresh value (as a np.array(hsv))
        :param upper_thresh: the upper hsv thresh value (as a np.array(hsv))
        :return: A DBugBinaryImage instance. Each pixel in the returned image is white iff:
                 lower_bound <= pixel <= upper_bound.

        """
        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image with the given thresh values
        return DBugBinaryImage(cv2.inRange(hsv_image, lower_thresh, upper_thresh))

    def draw_contours(self, contours, line_color=(0,0,0), line_thickness=1):
        """
        Draws the given DBugContours (list) on self
        :param contours: The contours to draw (list)
        :param line_color: (r,g,b)
        :return: None
        """
        cv2_contours = [c.contour for c in contours]
        cv2.drawContours(self.image, cv2_contours, -1, line_color, line_thickness)  # -1 draw all contours in cv2_contours

    def draw_rotated_enclosing_rectangle(self, contour, line_color=(0,0,0), line_thickness=1):
        """
        Draws the rotated enclosing rectangle of the given contour on self
        :param line_color: (r,g,b)
        :return: None
        """
        rect = contour.rotated_enclosing_rectangle()
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        self.draw_contours([DbugContour(cv_contour=box)], line_color=line_color, line_thickness=line_thickness)

    def draw_text(self, text, origin, font=cv2.FONT_HERSHEY_SIMPLEX, text_scale=0.7, text_color=(255,0,0), thickness=2):
        """
        Draws the given text on self
        :param text: The text to draw
        :param origin: The top-left (x,y) coords to start the drawing from
        :param font: a cv2 font
        :param text_scale: The text scale (size)
        :param text_color: The (r,g,b) text color
        :param thickness: The line thickness
        :return:
        """
        cv2.putText(self.image, text, origin, font, text_scale, text_color, thickness)


class DBugBinaryImage(DBugAbstractImage):
    """
    a DBugBinaryImage instance represents an image with white or black pixels only.
    This class helps interact and extract data from the underling image represented as an OpenCV image.
    """

    def detect_contours(self):
        """
        Detects the contours in self. A contour is a set of white pixels connected to each other.
        :return: the contours that were found as cv2 contours.
        """
        (_,contours, _) = cv2.findContours(self.image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return [DbugContour(cv_contour=contour) for contour in contours]