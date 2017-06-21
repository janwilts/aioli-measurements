

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
