import cv2

from zoloto import assert_has_gui_components
from zoloto.calibration import CalibrationParameters, save_calibrations
from zoloto.cameras.camera import Camera

FRAMES = 250
FEED_WINDOW_NAME = "Feed"

assert_has_gui_components()


def wait_for_markers(camera):
    while True:
        frame = camera.capture_frame()
        print(frame)
        cv2.imshow(FEED_WINDOW_NAME, frame)
        cv2.waitKey(1)
        visible_markers = camera.get_visible_markers(frame)
        if visible_markers != []:
            return


def capture_frames(camera, board):
    decimator = 0
    all_corners = []
    all_ids = []

    for i in range(FRAMES):
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
        cv2.imshow("Feed", frame)
        cv2.waitKey(1)
        print("Frames captured: {}/{}".format(i + 1, FRAMES), end="\r")  # noqa: T001
        decimator += 1

    return all_ids, all_corners


def process_frames(all_ids, all_corners, camera, board):
    image_size = cv2.cvtColor(camera.capture_frame(), cv2.COLOR_BGR2GRAY).shape
    ret, mtx, dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
        all_corners, all_ids, board, image_size, None, None
    )
    return mtx, dist


def main():
    camera = Camera(0, marker_dict=cv2.aruco.DICT_6X6_250)

    board = cv2.aruco.CharucoBoard_create(6, 6, 0.025, 0.0125, camera.marker_dictionary)

    cv2.imshow("Calibration image", board.draw((200 * 6, 200 * 6)))
    cv2.waitKey(1)

    print("Waiting until markers in view...")  # noqa: T001
    wait_for_markers(camera)

    print("Capturing frames...")  # noqa: T001
    all_ids, all_corners = capture_frames(camera, board)

    cv2.destroyAllWindows()

    print()  # noqa: T001
    print("Processing frames...")  # noqa: T001
    camera_matrix, distance_coefficients = process_frames(
        all_ids, all_corners, camera, board
    )

    print("Saving calibration...")  # noqa: T001
    calibration_params = CalibrationParameters(camera_matrix, distance_coefficients)

    save_calibrations(calibration_params, "calibrations.xml")
    print("Calibrations saved to 'calibrations.xml'")  # noqa: T001


if __name__ == "__main__":
    main()
