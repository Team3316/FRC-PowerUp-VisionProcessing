# FRC-PowerUp-VisionProcessing
This repo includes all the code related to vision processing, just for the 2018 POWER UP mission.

# OpenCV
This code is based on OpenCV (cv2).
This code was tested on Windows and MacOS using OpenCV 2.4.12.

# Running
- Please use sudo when running main (i.e sudo python main.py) to allow logging.
- This code was tested on python2.7.9

# Arguments
The possible command line arguments are as following:
- --host Roborio host address
- --port Roborio port address
- --dump_image should the processed image be saved to DUMP_IMAGE_PATH every DUMP_IMAGE_EVERY_FRAMES frames. Default to False
- --enable_network should data be sent to the given port and host. Default to False
- --display_gui should a gui window with the processed image be displayed. Default to False

*(NOTE: All CAPITAL names are constants in constants.py)*

# Pushing/Commiting/PRs
- Branches are mandatory!
- When merge is needed, please create a PR and add Barak & Leon & Jonathan as Reviewers.

# Constants to Update Per Lightning Conditions or Camera
- BASE_1M_POWER_CUBE_BOUNDING_ROTATED_RECTANGLE_AREA
- MIN_BOUND_RECT_AREA, MAX_BOUND_RECT_AREA
- CAMERA_VIEW_ANGLE_Y, CAMERA_VIEW_ANGLE_X
- LOWER_BOUND, UPPER_BOUND

*(NOTE: Description of the above constants can be found in constans.py)*
