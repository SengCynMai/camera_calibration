# Lens Distortion Correction using OpenCV

## Description
This project focuses on understanding and correcting lens distortion using OpenCV. Cameras, especially those with wide-angle lenses, often produce images where straight lines appear slightly curved. This project demonstrates how to remove that distortion through camera calibration and image rectification.

A chessboard pattern is used because it provides a clear and structured set of corner points, which makes it suitable for estimating camera parameters. Once the camera is calibrated, the computed parameters are applied to correct distortion in a video.

---

## Main Idea
The workflow of this project is divided into two main steps:

1. Estimate the camera parameters using a known pattern (chessboard)  
2. Use those parameters to correct distortion in a video  

---

## Features
- Interactive frame selection from a video  
- Automatic chessboard corner detection  
- Camera calibration using multiple images  
- Real-time distortion correction  
- Toggle between original and corrected video  
- Save corrected output as an MP4 file  

---

## Project Structure
.
├── camera_calibration.py # Computes camera parameters from chessboard images
├── distortion_correction.py # Applies distortion correction to video
├── calibration_result.npz # Saved camera matrix and distortion coefficients
├── chessboard.mp4 # Input video
└── rectified_output.mp4 # Output video (generated)

---

## Detailed Explanation

### 1. Camera Calibration (camera_calibration.py)
This step estimates the intrinsic parameters of the camera.

- The program reads frames from a video containing a chessboard pattern  
- The user manually selects useful frames:  
  - Press `Space` to select a frame  
  - Press `Enter` to finish  
- For each selected frame:  
  - Chessboard corners are detected  
  - Corner positions are refined for higher accuracy  
- 3D points (real-world coordinates) and 2D points (image coordinates) are created  
- OpenCV’s `calibrateCamera()` computes:  
  - Camera matrix (K)  
  - Distortion coefficients (dist)  

The results are saved in:
calibration_result.npz

---

### 2. Distortion Correction (distortion_correction.py)
This step uses the calibration results to correct distortion in a video.

- The program loads the saved camera parameters  
- Each frame of the video is processed  
- Distortion is corrected using:  
  - `cv.initUndistortRectifyMap()`  
  - `cv.remap()`  
- The corrected frame is displayed in real time  

The correction keeps the same frame size as the original video.

---

## Controls

### During Calibration
- `Space` : Select frame  
- `Enter` : Finish selection  

### During Distortion Correction
- `R` : Toggle Original ↔ Rectified  
- `Q` : Quit  

---

## Results
- Original video: straight lines may appear curved due to lens distortion  
- Rectified video: lines become straight after correction  
- The effect is more visible near the edges of the image  

---

## Demo
Add your screenshot or video here (required).

Example:

---

## Requirements
- Python 3  
- OpenCV (`cv2`)  
- NumPy  

Install dependencies:

pip install opencv-python numpy

