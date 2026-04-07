import numpy as np
import cv2 as cv
import os


def main():
    os.chdir(os.path.dirname(__file__))
    print("Current directory:", os.getcwd())

    try:
        data = np.load('calibration_result.npz')
        print("Loaded keys:", data.files)

        K = data['K']
        dist_coeff = data['dist']

    except Exception as e:
        print("Error loading calibration data:", e)
        print("Run camera_calibration.py first.")
        return

    video_file = 'chessboard.mp4'
    video = cv.VideoCapture(video_file)

    if not video.isOpened():
        print("Error: Cannot open video file")
        return

    # ✅ MP4 Video Writer (fixed)
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    fps = int(video.get(cv.CAP_PROP_FPS))
    w = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    out = cv.VideoWriter('rectified_output.mp4', fourcc, fps, (w, h))

    print("Press 'R' to toggle correction")
    print("Press 'Q' to quit")

    show_rectify = True
    map1, map2 = None, None

    while True:
        valid, img = video.read()
        if not valid:
            break

        info = "Original"

        if show_rectify:
            if map1 is None or map2 is None:
                h, w = img.shape[:2]

                # Keep same frame (no zoom/shift)
                map1, map2 = cv.initUndistortRectifyMap(
                    K, dist_coeff, None, K, (w, h), cv.CV_32FC1
                )

            img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR)
            info = "Rectified"

        cv.putText(img, info, (10, 25),
                   cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

        cv.imshow("Geometric Distortion Correction", img)

        # ✅ Save frame to MP4
        out.write(img)

        key = cv.waitKey(10)

        if key == ord('q'):
            break
        elif key == ord('r'):
            show_rectify = not show_rectify

    video.release()
    out.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()