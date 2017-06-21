from camera import Camera
from shapedetector import *

# Statics
CROP_SIZE = 25

# Global variables
cameras = [Camera('USB Cam', 1)]
cameras_status = False


def main():
    """ Main, function, entry point """
    for cam in cameras:
        if cam.cap.isOpened():
            reference, crop_height, crop_width = cam.snap_rotation_reference(CROP_SIZE)

            frame = cam.snap()
            rotation_degrees = frame.get_rotation()
            rotated_frame = frame.rotate_frame(rotation_degrees)
            rotated_frame_crop = rotated_frame.frame[CROP_SIZE:crop_height, CROP_SIZE:crop_width]

            matched_result = cv2.matchTemplate(rotated_frame_crop, reference.frame, cv2.TM_CCOEFF)
            _, _, _, max_loc = cv2.minMaxLoc(matched_result)
            top_left = max_loc
            bottom_right = (top_left[0] + crop_width - CROP_SIZE, top_left[1] + crop_height - CROP_SIZE)

            reference_crop = reference.frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

            frame_edges = cam.snap_canny(snap=True)

            subtracted_edges = frame_edges.subtract(cam.reference)
            contours = subtracted_edges.thresh_contours()

            for contour in contours:
                contour_area = cv2.contourArea(contour)
                if contour_area > 5:
                    print contour_area

            cv2.imshow('edges', frame_edges.frame)
            cv2.imshow('subtracted', subtracted_edges.frame)
            cv2.imshow('reference', cam.reference.frame)
            cv2.imshow('reference-crop', reference_crop)


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
        cv2.namedWindow(cam.name)
        if cam.status():
            cam.calibrate(5)

    while camera_status():
        main()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    for cam in cameras:
        cam.cap.release()
        cv2.destroyAllWindows()
