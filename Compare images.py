import cv2
import numpy as np
import math

def rotate_image(img, degrees):
    h, w, _ = img.shape
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, degrees, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))
    return rotated

def get_rotation_angle(img):
    h, w, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, 0)
    blurred_edges = cv2.GaussianBlur(edges, (5, 5), 0)
    lines = cv2.HoughLinesP(blurred_edges, 1, np.pi / 100, 150, 50, 10)
    if lines is not None:
        top_l = [0, h]
        top_r = [w-1, h]
        for line in lines:
            for x1, y1, x2, y2 in line:
                if x1 == top_l[0] and y1 < top_l[1]:
                    top_l[1] = y1
                if x2 == top_r[0] and y2 < top_r[1]:
                    top_r[1] = y2
    degrees = math.degrees(math.atan2(float(top_r[1] - top_l[1]), float(top_r[0] - top_l[0])))
    return degrees


cr_px = 25      # cr_px == the amount of Pixels that will be Cropped.
cap = cv2.VideoCapture(1)

_, reference_frame = cap.read()
degrees = get_rotation_angle(reference_frame)
reference_frame = rotate_image(reference_frame, degrees)
h, w, _ = reference_frame.shape
cr_h = h - cr_px
cr_w = w - cr_px

while True:
    _, curr_frame = cap.read()
    degrees = get_rotation_angle(curr_frame)
    curr_frame = rotate_image(curr_frame, degrees)
    curr_frame_crop = curr_frame[cr_px:cr_h, cr_px:cr_w]

    # Apply template Matching
    res = cv2.matchTemplate(curr_frame_crop, reference_frame, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + cr_w - cr_px, top_left[1] + cr_h - cr_px)

    reference_frame_crop = reference_frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    #Draw rectangle and show the original and cropped frames.
    cv2.imshow('crop-image', curr_frame_crop)
    cv2.imshow('crop-reference', reference_frame_crop)
    cv2.rectangle(curr_frame, top_left, bottom_right, 255, 2)
    cv2.imshow('sub-image', curr_frame)


    k = cv2.waitKey(5) & 0xFF
    if k == 27 or k == ord('c'):
        if k == 27:
            break
        reference_frame = rotate_image(cap.read()[1])



# def merge_edges(amount=5):
#     new_frame = None
#     x = 0
#     while x < amount:
#         _, frame = cap.read()
#         frame = cv2.GaussianBlur(frame, (5, 5), 0)
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         edges = cv2.Canny(gray, 50, 150, apertureSize=3)
#         if x > 0:
#             new_frame += edges
#         else:
#             new_frame = edges
#         x += 1
#         cv2.imshow('fram', gray)
#         cv2.imshow('cann', edges)
#     return new_frame
#
# prev_edges = merge_edges(5)
# while True:
#     curr_edges = merge_edges(1)
#     subst_edges = curr_edges - prev_edges
#
#     cv2.imshow('curr', curr_edges)
#     cv2.imshow('subs', subst_edges)
#
#     ret, thresh = cv2.threshold(subst_edges, 127, 255, 0)
#     im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
#     for cnt in contours:
#         area = cv2.contourArea(cnt)
#         if area > 5:
#             print area
#
#     l = cv2.waitKey(5) & 0xFF
#     if l == ord('c'):
#         prev_edges = merge_edges(5)
#
#     k = cv2.waitKey(5) & 0xFF
#     if k == 27:
#         break