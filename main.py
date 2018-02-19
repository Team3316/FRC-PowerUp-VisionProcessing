# Imports:
import argparse
import traceback

from cv2 import destroyAllWindows, waitKey
from constants import *
from dbug_networking import DBugNetworking
from dbug_video_stream import DBugVideoStream
from dbug_result_object import DBugResult
from logger import get_logger
from dbug_contour import DbugContour

logger = get_logger()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default=ROBORIO_MDNS,
                        help="Roborio host address")
    parser.add_argument("--port", type=int, default=ROBORIO_PORT,
                        help="Roborio host port")
    parser.add_argument("--dump_image", action="store_true", default=False,
                        help="Dump images to current working directory")
    parser.add_argument("--enable_network", action="store_true", default=False,
                        help="Enable network communications")
    parser.add_argument("--display_gui", action="store_true", default=False,
                        help="Should display image on gui frame")
    return parser.parse_args()


def filter_sort_contours(contours):
    """
    Filters the given list of contours and sorting them according to the probability of being a PowerCube
    :param contours: The list of DbugContours to filter and sort
    :return: A new list of DbugContours that are sorted according to the probability of being a PowerCube
             This list may not contain all the original DbugContours in contours, since we filter the given list for
             Better performance.
    """
    potential_power_cubes = []
    for contour in contours:
        (x_offset, y_offset, width, height) = contour.straight_enclosing_rectangle()
        if not (MIN_BOUND_RECT_AREA < contour.contour_area() < MAX_BOUND_RECT_AREA):
            # logger.debug("Rect denied, contour min-max area, contour area is: " + str(width*height))
            continue

        ratio = float(height) / float(width)
        if (MIN_HEIGHT_WIDTH_RATIO > ratio) or (MAX_HEIGHT_WIDTH_RATIO < ratio):
            # logger.debug("Rect denied, height/width ratio")
            continue

        potential_power_cubes.append(contour)

    potential_power_cubes.sort(key=lambda cnt: cnt.contour_area(), reverse=True)

    logger.info("Found " + str(len(potential_power_cubes)) + " potential PowerCubes")

    return potential_power_cubes


def init_vision_command(args):

    # The communication channel to the robot
    robot_com = DBugNetworking(host=args.host, port=args.port)

    # Video stream to get the images from
    camera_device_index = DBugVideoStream.get_camera_usb_device_index()

    logger.debug("Found camera index: " + str(camera_device_index))

    if camera_device_index is not None:
        cam = DBugVideoStream(camera_device_index=camera_device_index)
    else:
        cam = DBugVideoStream()

    return cam, robot_com

def handle_image(args, frames_processed, frame, contours, powercube, result):
    """
    Handles the GUI / image dumping.
    """
    if ((args.dump_image and frames_processed % DUMP_IMAGE_EVERY_FRAMES == 0) or args.display_gui) and len(contours) >= 1:

        # Filtered contours:
        copy_image = frame.copy()
        copy_image.draw_contours(contours, line_color=(255,255,0))

        # Rotated enclosing rectangles on PowerCube:

        copy_image.draw_rotated_enclosing_rectangle(contour=powercube, line_color=(0,0,255))
        copy_image.draw_contours([powercube], line_color=(255,0,0))

        # Angle text:

        copy_image.draw_text('AA: ' + str(result.azimuth_angle), origin=(30,10), text_scale=0.5)
        copy_image.draw_text('Dis: ' + str(result.distance_from_camera), origin=(30,30), text_scale=0.5)
        copy_image.draw_text('Height: ' + str(result.height), origin=(30,50), text_scale=0.5)
        copy_image.draw_text('T: ' + str(result.result_type), origin=(30,70), text_scale=0.5)

        if args.dump_image:
            # Finally save the frames:
            logger.debug("Writing frame to path: %s", DUMP_IMAGE_PATH)
            copy_image.save_to_path(path=DUMP_IMAGE_PATH)
        elif args.display_gui:
            copy_image.display_gui_window("Result Image")

def send_to_roborio(args, robot_com, result_obj):
    if args.enable_network:
        if result_obj is None or result_obj.azimuth_angle == UNABLE_TO_PROC_DEFAULT_VAL:
            robot_com.send_no_data()
            logger.warning("Couldn't find PowerCubes... sending no data")
        else:
            robot_com.send_data(result_obj=result_obj)

def run_vision_command(cam, robot_com, args):

    frames_processed = 0
    # Making sure the vision process does not crash
    try:

        # Capture frames non-stop, process them and send the results to the robot
        while True:

            frame = cam.get_image()

            if frame is None:
                logger.error("Couldn't Read Image from self.cam!")
                if args.display_gui:
                    frame.display_gui_window("Result Image")
                    # OpenCV 3 GUI fix; needs to be here to be in the loop
                    if args.display_gui and (waitKey(1) & 0xFF == ord('q')):
                        break
                continue

            frames_processed += 1

            binary_image = frame.filter_with_colors(LOWER_BOUND, UPPER_BOUND)
            binary_image = binary_image.get_median_blur()
            unfiltered_contours = binary_image.detect_contours()

            filtered_contours = filter_sort_contours(unfiltered_contours)

            if len(filtered_contours) < 1:
                logger.error("Didn't find any PowerCubes")
                send_to_roborio(args, robot_com, None)

                if args.display_gui:
                    frame.display_gui_window("Result Image")
                    # OpenCV 3 GUI fix; needs to be here to be in the loop
                    if args.display_gui and (waitKey(1) & 0xFF == ord('q')):
                        break
                continue

            powercube_contour = filtered_contours[0]
            result_obj = None

            if len(filtered_contours) >= 1:
                result_obj = DBugResult(result_object=powercube_contour)

            send_to_roborio(args, robot_com, result_obj)

            handle_image(args, frames_processed, frame, filtered_contours, powercube_contour, result_obj)

            # OpenCV 3 GUI fix; needs to be here to be in the loop
            if args.display_gui and (waitKey(1) & 0xFF == ord('q')):
                break


    # except Exception as ex:
    #
    #     # MARK: Possible Exception and reasons:
    #     # 1. Example Exception - Reason For Exception
    #     logger.error("Unhandled Exception:\n" + traceback.format_exc())
    #     logger.debug("Skipping to the next frame!")

    finally:
        destroyAllWindows()
        cam.cam.release()
        logger.info("Finally was called, releasing camera and more")
        if robot_com.sock is not None:
            robot_com.sock.close()

if __name__ == "__main__":
    args = parse_arguments()

    cam, robot_com = init_vision_command(args)

    run_vision_command(cam, robot_com, args)

