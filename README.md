# FRC-PowerUp-VisionProcessing
This repo includes all the code related to vision processing, just for the 2018 POWER UP mission.

# OpenCV
This code is based on OpenCV (cv2)

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
- When merge is needed, please create a PR and add barak & leon as Reviewers.
