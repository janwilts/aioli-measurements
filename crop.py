import cv2

# Global variables
current_crop = None
highest_line = None
lowest_line = None


def crop(image, lines, tray_size):
    """ Takes in an image, hough lines, and the width of the tray and returns a cropped image """
    global current_crop
    global highest_line
    global lowest_line

    height, width, _ = image.frame.shape

    if current_crop is None:
        current_crop = image.frame

    if highest_line is None and lowest_line is None:
        highest_line = [0, height / 2, width, height / 2]
        lowest_line = highest_line

    for x1, y1, x2, y2 in lines[0]:
        line = [0, y1, width, y2]

        if lowest_line[1] > y1 and lowest_line[3] > y2:
            lowest_line = line
        elif highest_line[1] < y1 and highest_line[3] < y2:
            highest_line = line

        cv2.line(image.frame, (0, y1), (width, y2), (0, 0, 255), 2)

    top_crop = (highest_line[1] + highest_line[3]) / 2 - tray_size
    bottom_crop = (lowest_line[1] + lowest_line[3]) / 2 + tray_size

    current = image.frame[bottom_crop:top_crop, 0:]

    return current