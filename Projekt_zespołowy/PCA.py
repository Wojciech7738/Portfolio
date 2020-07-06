import sys
import math, copy, time
import cv2
import numpy as np
import matplotlib.pyplot as plt


def main(argv):
    file = cv2.imread('keys/giza-pyramid.jpg', cv2.IMREAD_GRAYSCALE) # Wczytanie obrazu w skali szarości

    dst = cv2.Canny(file, 50, 200, None, 3)
    # Copy edges to the images that will display the results in BGR
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    # lines = cv2.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
    # if lines is not None:
    #     for i in range(0, len(lines)):
    #         rho = lines[i][0][0]
    #         theta = lines[i][0][1]
    #         a = math.cos(theta)
    #         b = math.sin(theta)
    #         x0 = a * rho
    #         y0 = b * rho
    #         pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
    #         pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
    #         cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)

    begin = time.time()
    linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)
    cimg = copy.deepcopy(file)
    end = time.time()
    print(f"HoughLinesP\'s execution time: {end-begin}s")

    # begin = time.time()
    # circles = cv2.HoughCircles(file, cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, param2 = 30, minRadius = 0, maxRadius = 0)
    # circles = np.uint16(np.around(circles))
    # for i in circles[0, :]:
    #     # Outer circles
    #     cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2, cv2.LINE_4)
    #     # Centers of the circles
    #     cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
    # end = time.time()
    # print(f"HoughCircles\'s execution time: {end - begin}s")

    cv2.imshow("Source", file)
    # cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
    cv2.imshow("Detected Circles (in black) - Circle Transform", cimg)

    cv2.waitKey()
    return 0

if __name__ == '__main__':
    main(sys.argv[1:])
