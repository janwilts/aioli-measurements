from frame import Frame
from camera import Camera
from shapedetector import *

# Constants
CROP_SIZE = 25
ANGLE_SMOOTHING_LENGTH = 5

# Global variables
cameras = [Camera('USB Cam', 0, ANGLE_SMOOTHING_LENGTH)]
cameras_status = False


def main():
    """ Main, function, entry point """
    for cam in cameras:
        if cam.cap.isOpened():
            rotated_frame_crop, _ = cam.snap_rotation(CROP_SIZE)
            reference = cam.reference
            height, width = reference.shape

            matched_result = cv2.matchTemplate(rotated_frame_crop.frame, reference.frame, cv2.TM_CCOEFF)
            _, _, _, top_left = cv2.minMaxLoc(matched_result)
            bottom_right = (top_left[0] + width - 2 * CROP_SIZE, top_left[1] + height - 2 * CROP_SIZE)

            reference_crop = cam.reference_canny.frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

            frame_edges = cam.snap_canny(rotated_frame_crop.frame)

            subtracted_edges = frame_edges.subtract(reference_crop)

            zero = cv2.countNonZero(subtracted_edges.frame)
            #print zero
            size = subtracted_edges.frame.size
            #print (cv2.countNonZero(subtracted_edges.frame) / subtracted_edges.frame.size) * 100
            contours = subtracted_edges.thresh_contours()

            for contour in contours:
                contour_area = cv2.contourArea(contour)
                if contour_area > 5:
                    break

            cv2.imshow('edges', frame_edges.frame)
            cv2.imshow('subtracted', subtracted_edges.frame)
            cv2.imshow('rotated-frame-crop', rotated_frame_crop.frame)
            cv2.imshow('reference', reference.frame)
            cv2.imshow('reference-crop', reference_crop)
            cv2.imshow('reference-canny', cam.reference_canny.frame)


def camera_status():
    """ Checks the status of the camera's """
    global cameras
    global cameras_status

    if cameras_status:
        return cameras_status

    temp_status = False

    for cam in cameras:
        if cam.status():
            temp_status = True

    return temp_status

if __name__ == '__main__':
    # Entry point
    for cam in cameras:
        #cv2.namedWindow(cam.name)
        if cam.status():
            calibration_completed = False
            while not calibration_completed:
                calibration_completed = cam.calibrate(5)

    while camera_status():
        main()
        k = cv2.waitKey(1) & 0xFF
        if k == 27 or k == ord('q') or k == ord('c'):
            if k == 27 or k == ord('q'):
                break
            else:
                calibration_completed = False
                while not calibration_completed:
                    calibration_completed = cam.calibrate(5)

    for cam in cameras:
        cam.cap.release()
        cv2.destroyAllWindows()
