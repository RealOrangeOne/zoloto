import argparse
import logging
from pathlib import Path

import cv2

from zoloto import assert_has_gui_components
from zoloto.calibration import CalibrationParameters, save_calibrations
from zoloto.cameras.camera import Camera
from zoloto.marker_dict import MarkerDict

FEED_WINDOW_NAME = "Feed"

assert_has_gui_components()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, default=0)
    parser.add_argument("--frames", type=int, default=250)
    parser.add_argument("-v", "--verbose", help="Run verbosely", action="store_true")
    return parser.parse_args()


def wait_for_markers(camera):
    while True:
        frame = camera.capture_frame()
        cv2.imshow(FEED_WINDOW_NAME, frame)
        cv2.waitKey(1)
        visible_markers = camera.get_visible_markers(frame=frame)
        if visible_markers != []:
            return


def create_board(camera, board_size=6):
    board = cv2.aruco.CharucoBoard_create(
        board_size, board_size, 0.025, 0.0125, camera.marker_dictionary
    )
    return board.draw((150 * board_size, 150 * board_size)), board


def capture_frames(frames, camera, board):
    decimator = 0
    all_corners = []
    all_ids = []

    for i in range(frames):
        frame = camera.capture_frame()
        ids, corners = camera._get_raw_ids_and_corners(frame)
        if not len(corners):
            continue
        _, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(
            corners, ids, frame, board
        )
        if (
            charuco_corners is not None
            and charuco_ids is not None
            and len(charuco_corners) > 3
            and decimator % 3 == 0
        ):
            all_corners.append(charuco_corners)
            all_ids.append(charuco_ids)
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        cv2.imshow(FEED_WINDOW_NAME, frame)
        cv2.waitKey(1)
        logging.debug("Frames captured: {}/{}".format(i + 1, frames))
        decimator += 1

    return all_ids, all_corners


def process_frames(all_ids, all_corners, image_size, board):
    ret, mtx, dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
        all_corners, all_ids, board, image_size, None, None
    )
    return mtx, dist


def main():
    args = parse_args()
    logging.basicConfig(
        level=logging.NOTSET if args.verbose else logging.INFO,
        format="[%(levelname)s]: %(message)s",
    )
    logging.info("Creating calibration image...")
    camera = Camera(args.id, marker_dict=MarkerDict.DICT_6X6_250)

    board_image, board = create_board(camera, board_size=5)
    cv2.imshow("Calibration Board", board_image)
    cv2.waitKey(1)

    logging.info("Waiting until markers in view...")
    wait_for_markers(camera)

    logging.info("Capturing frames...")
    all_ids, all_corners = capture_frames(args.frames, camera, board)

    cv2.destroyAllWindows()
    image_size = cv2.cvtColor(camera.capture_frame(), cv2.COLOR_BGR2GRAY).shape
    del camera  # Explicitly close the camera so the light turns off

    logging.info("Processing frames...")
    camera_matrix, distance_coefficients = process_frames(
        all_ids, all_corners, image_size, board
    )

    logging.info("Saving calibration...")
    calibration_params = CalibrationParameters(camera_matrix, distance_coefficients)

    save_calibrations(calibration_params, Path("calibrations.xml"))
    logging.info("Calibrations saved to 'calibrations.xml'")


if __name__ == "__main__":
    main()
