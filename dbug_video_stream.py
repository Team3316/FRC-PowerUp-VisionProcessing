from dbug_image import DBugColorImage
from glob import glob
from constants import *
from cv2 import VideoCapture
from cv2 import cv
from logger import logger
from numpy import rot90


class DBugVideoStream(object):
    """
    A class to interact with a camera connected using a USB
    """

    def __init__(self, camera_device_index=DEFAULT_CAMERA_USB_INDEX, read_buffer_amount=DEFAULT_READ_BUFFER_AMOUNT):
        """
        :param camera_device_index: The USB device index of the camera to get the pictures from
        :param read_buffer_amount: The amount of frames to read from the camera in each update in order to clear the buffer
        """
        self.cam = VideoCapture(camera_device_index)
        self._set_cam_props()
        self.read_buffer_amount = read_buffer_amount

    def _set_cam_props(self):
        """
        Setting the props of self.cam such as picture height, width, saturation and more
        """
        if not self.cam.isOpened():
            raise ValueError("Camera Not Found")

        if not self.cam.set(3, RESIZE_IMAGE_WIDTH):
            logger.warning("Set width failed")

        if not self.cam.set(4, RESIZE_IMAGE_HEIGHT):
            logger.warning("Set height failed")

        if not self.cam.set(cv.CV_CAP_PROP_BRIGHTNESS, BRIGHTNESS):
            logger.warning("Set brightness failed")

        if not self.cam.set(cv.CV_CAP_PROP_SATURATION, SATURATION):
            logger.warning("Set saturation failed")

        if not self.cam.set(cv.CV_CAP_PROP_EXPOSURE, EXPOSURE):
            logger.warning("Set exposure failed")

        if not self.cam.set(cv.CV_CAP_PROP_CONTRAST, CONTRAST):
            logger.warning("Set contrast failed")

        return self.cam

    def get_image(self):
        """
        Clears the buffer of self.cam and grabs a frame.
        :return: The frame that was grabbed, as a DBugColorImage instance.
        """
        got_image, new_frame = self.cam.read()
        if not got_image:  # Can't even grab one frame - might be a problem
            return

        for _ in xrange(self.read_buffer_amount - 1):  # minus one, since we already grabbed one frame.
            frame = new_frame
            got_image, new_frame = self.cam.read()  # Grab another frame

            if not got_image:
                break  # Seems like the buffer is empty - lets use the last frame

        else:  # this occurs if the loop wasn't broken - lets use the new frame
            frame = new_frame

        if ROTATE_CLOCKWISE:
            frame = rot90(frame, 1)

        return DBugColorImage(cv2_image=frame)

    @staticmethod
    def get_camera_usb_device_index():
        """
        finds the camera usb device index from /dev
        return: Int, the usb device index of the camera that is currently connected. If no camera was found None.
        """
        video_devices_names = glob("/dev/video*")
        if video_devices_names:
            first_cam_name = video_devices_names[0]
            cam_index_start_index = first_cam_name.find("video")
            return int(first_cam_name[cam_index_start_index + len("video"):])
        else:
            return None
