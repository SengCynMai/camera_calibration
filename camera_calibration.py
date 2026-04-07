import numpy as np
import cv2 as cv


def select_img_from_video(video_file, board_pattern, select_all=False, wait_msec=10):
    video = cv.VideoCapture(video_file)
    img_select = []

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        display_frame = frame.copy()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)

        if complete:
            cv.drawChessboardCorners(display_frame, board_pattern, pts, complete)

        cv.imshow('Select Images (Space to select, Enter to finish)', display_frame)
        
        key = cv.waitKey(wait_msec)
        if select_all or key == ord(' '):
            img_select.append(frame)
            print(f"Frame selected. Total: {len(img_select)}")
        elif key == 13:
            break

    video.release()
    cv.destroyAllWindows()
    return img_select


def calib_camera_from_chessboard(images, board_pattern, board_cellsize, K=None, dist_coeff=None, calib_flags=None):
    img_points = []
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            pts2 = cv.cornerSubPix(gray, pts, (11, 11), (-1, -1), criteria)
            img_points.append(pts2)

    assert len(img_points) > 0, 'There is no set of complete chessboard points!'

    obj_pts = [[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])]
    obj_points = [np.array(obj_pts, dtype=np.float32) * board_cellsize] * len(img_points)

    return cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], K, dist_coeff, flags=calib_flags)


if __name__ == '__main__':
    video_input = 'chessboard.mp4'
    pattern_size = (8, 6)
    cell_size = 0.025

    selected_images = select_img_from_video(video_input, pattern_size)

    if len(selected_images) > 0:
        rmse, K, dist_coeff, rvecs, tvecs = calib_camera_from_chessboard(
            selected_images, pattern_size, cell_size
        )

        print("\n" + "="*30)
        print(f"Calibration Result (RMSE): {rmse}")
        print("Camera Matrix (K):")
        print(K)
        print("\nDistortion Coefficients (dist):")
        print(dist_coeff)
        print("="*30)

        # ✅ FIXED HERE
        np.savez('calibration_result.npz', K=K, dist=dist_coeff)

        print("\nResults saved to 'calibration_result.npz'")