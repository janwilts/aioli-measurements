import math


def crop_image(lines, height, width):
    """ Crops an image to specified height and using supplied lines """
    if lines is not None:
        top_left = [0, height]
        top_right = [width - 1, height]

        for line in lines:
            for x1, y1, x2, y2 in line:
                if x1 == top_left[0] and y1 < top_left[1]:
                    top_left[1] = y1
                if x2 == top_right[0] and y2 < top_right[1]:
                    top_right[1] = y2

        return top_left, top_right

    else:
        return False, False


def crop_rotated_image(angle, height, width):
    """ Calculates the crop to be used to eliminate black lines around a rotation """
    if width <= 0 or height <= 0:
        return 0, 0

    width_is_longer = width >= height
    side_long, side_short = (width, height) if width_is_longer else (height, width)

    # Since the solutions for angle, -angle and 180-angle are all the same,
    # If suffices to look at the first quadrant and the absolute values of sin,cos:
    sin_a, cos_a = abs(math.sin(angle)), abs(math.cos(angle))
    if side_short <= 2. * sin_a * cos_a * side_long:
        # Half constrained case: two crop corners touch the longer side,
        # The other two corners are on the mid-line parallel to the longer line
        x = 0.5 * side_short
        max_width, max_height = (x / sin_a, x / cos_a) if width_is_longer else (x / cos_a, x / sin_a)
    else:
        # Fully constrained case: crop touches all 4 sides
        cos_2a = cos_a * cos_a - sin_a * sin_a
        max_width, max_height = (width * cos_a - height * sin_a) / cos_2a, (height * cos_a - width * sin_a) / cos_2a

    return int(max_height), int(max_width)
