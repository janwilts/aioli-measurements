import socket
import pickle
import struct
from frame import Frame
from frameprocessor import FrameProcessor
from shapedetector import *

# Constants
HOST = 'localhost'
PORT = 8082
CROP_SIZE = 25
ANGLE_SMOOTHING_LENGTH = 5

# Global variables
processor = FrameProcessor(ANGLE_SMOOTHING_LENGTH)
cameras_status = False
web_socket = None


def process_frame(web_frame):
    """ Main, function, entry point """
    rotated_frame_crop, _ = processor.frame_rotation(CROP_SIZE, Frame(web_frame))
    reference = processor.reference
    height, width = reference.shape

    matched_result = cv2.matchTemplate(rotated_frame_crop.frame, reference.frame, cv2.TM_CCOEFF)
    _, _, _, top_left = cv2.minMaxLoc(matched_result)
    bottom_right = (top_left[0] + width - 2 * CROP_SIZE, top_left[1] + height - 2 * CROP_SIZE)

    reference_canny_crop = processor.reference_canny.frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    frame_edges = processor.frame_canny(rotated_frame_crop.frame)

    subtracted_edges = frame_edges.subtract(reference_canny_crop)

    binary = subtracted_edges.binary
    print cv2.countNonZero(binary.frame)
    contours = subtracted_edges.thresh_contours()

    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if contour_area > 5:
            break

    cv2.imshow('edges', frame_edges.frame)
    cv2.imshow('rotated-frame-crop', rotated_frame_crop.frame)
    # cv2.imshow('reference', reference.frame)
    cv2.imshow('reference-crop', reference_canny_crop)
    cv2.imshow('reference-canny', processor.reference_canny.frame)
    cv2.imshow('subtracted', subtracted_edges.frame)
    cv2.imshow('binary', binary.frame)

    return frame_edges.frame, rotated_frame_crop.frame, reference.frame, processor.reference_canny.frame, \
           reference_canny_crop, subtracted_edges.frame, binary.frame


def calibration_handler():
    print 'Calibrating camera'

    calibration_frames = []
    calibration_count = 0

    connection, _ = web_socket.accept()

    for i in xrange(5):
        print 'Calibration frame ' + str(i)
        connection_data = ''
        payload_size = struct.calcsize('L')

        while True:
            while len(connection_data) < payload_size:
                connection_data += connection.recv(4096)
            packed_msg_size = connection_data[:payload_size]
            connection_data = connection_data[payload_size:]
            msg_size = struct.unpack('L', packed_msg_size)[0]
            while len(connection_data) < msg_size:
                connection_data += connection.recv(4096)
            frame_data = connection_data[:msg_size]
            connection_data = connection_data[msg_size:]

            frame = pickle.loads(frame_data)
            calibration_frames.append(frame)


def main():
    # Entry point, web server stuff
    global web_socket

    web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        web_socket.bind((HOST, PORT))
        print 'Aioli Server started on \'' + str(HOST) + ':' + str(PORT) + '\''
    except socket.error:
        print 'Could not set up an Aioli server'
    web_socket.listen(10)

    connection, _ = web_socket.accept()

    connection_data = ''
    payload_size = struct.calcsize('L')

    while True:
        while len(connection_data) < payload_size:
            connection_data += connection.recv(4096)
            if connection_data == 'calibrate':
                connection.send('calibrating')
                calibration_handler()
                break
        packed_msg_size = connection_data[:payload_size]
        connection_data = connection_data[payload_size:]
        msg_size = struct.unpack('L', packed_msg_size)[0]
        while len(connection_data) < msg_size:
            connection_data += connection.recv(4096)
        frame_data = connection_data[:msg_size]
        connection_data = connection_data[msg_size:]

        frame = pickle.loads(frame_data)
        cv2.imshow('frame', frame)

        k = cv2.waitKey(1) and 0xFF
        if k == 27 or k == ord('q') or k == ord('c'):
            if k == 27 or k == ord('q'):
                break

        # web_socket.sendto(pickle.dumps(process_frame(frame)), (HOST, PORT))

if __name__ == '__main__':
    main()
