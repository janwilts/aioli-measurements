import cv2

cap = cv2.VideoCapture(1)


def merge_edges(amount):
    new_frame = None
    x = 0
    while x < amount:
        _, frame = cap.read()
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        if x > 0:
            new_frame += edges
        else:
            new_frame = edges
        x += 1
        cv2.imshow('fram', gray)
        cv2.imshow('cann', edges)
    return new_frame

prev_edges = merge_edges(5)
while True:
    curr_edges = merge_edges(1)
    subst_edges = curr_edges - prev_edges

    cv2.imshow('curr', curr_edges)
    cv2.imshow('subs', subst_edges)

    ret, thresh = cv2.threshold(subst_edges, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5:
            print area

    l = cv2.waitKey(5) & 0xFF
    if l == ord('c'):
        prev_edges = merge_edges(5)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
