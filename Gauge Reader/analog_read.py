'''  
Copyright (c) 2017 Intel Corporation.
Licensed under the MIT license. See LICENSE file in the project root for full license information.
'''
# modified version

import cv2
import numpy as np
import time
class Gauge_Reader:
    def completelyOverlaps(self, x1, x2, x3, x4):
        return (x1 <= x3 and x1 <= x4 and x2 >= x3 and x2 >= x4) or \
            (x2 <= x3 and x2 <= x4 and x1 >= x3 and x1 >= x4)

    def remove_overlapping_lines(self, lines):
        overlapped = []
        for i in range(int(len(lines)/2)+1, len(lines)):
            for j in range(len(lines)-1, 0, -1):
                [x1, y1, x2, y2] = lines[i]
                [x3, y3, x4, y4] = lines[j]
                # Checks whether the cross product between two different pairs of points
                # are both == 0, which means that the segments are both on the same line
                if np.cross(np.array([x1 - x2, y1 - y2]), np.array([x3 - x4, y3 - y4])) == 0 and \
                        np.cross(np.array([x1 - x2, y1 - y2]), np.array([x3 - x1, y3 - y1])) == 0:
                    # If lines are vertical, consider the y-coordinates
                    if x1 == x2:
                        # If 1st segment fully overlaps 2nd, add latter to the list
                        if self.completelyOverlaps(y1, y2, y3, y4):
                            overlapped.append(lines[j])
                        # If 2nd segment fully overlaps 1st, add latter to the list
                        elif self.completelyOverlaps(y3, y4, y1, y2):
                            overlapped.append(lines[i])
                    # In all other cases, consider the x-coordinates
                    else:
                        if self.completelyOverlaps(x1, x2, x3, x4):
                            overlapped.append(lines[j])
                        elif self.completelyOverlaps(x3, x4, x1, x2):
                            overlapped.append(lines[i])

        lines = [s for s in lines if s not in overlapped]
        return lines



    def dist_2_pts(self, x1, y1, x2, y2):
        #print np.sqrt((x2-x1)^2+(y2-y1)^2)
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def calibrate_gauge(self, img, gauge_number):
        '''
            This function should be run using a test image in order to calibrate the range available to the dial as well as the
            units.  It works by first finding the center point and radius of the gauge.  Then it draws lines at hard coded intervals
            (separation) in degrees.  It then prompts the user to enter position in degrees of the lowest possible value of the gauge,
            as well as the starting value (which is probably zero in most cases but it won't assume that).  It will then ask for the
            position in degrees of the largest possible value of the gauge. Finally, it will ask for the units.  This assumes that
            the gauge is linear (as most probably are).
            It will return the min value with angle in degrees (as a tuple), the max value with angle in degrees (as a tuple),
            and the units (as a string).
        '''

        height, width = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #convert to gray
        # gray = cv2.GaussianBlur(gray, (5, 5), 0)
        # gray = cv2.medianBlur(gray, 5)

        #for testing, output gray image
        #cv2.imwrite('gauge-%s-bw.%s' %(gauge_number, file_type),gray)

        #detect circles
        #restricting the search from 35-48% of the possible radii gives fairly good results across different samples.  Remember that
        #these are pixel values which correspond to the possible radii search range.
        big_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, np.array([]), 50, 30, int(height * 0.25),
                             int(height * 0.26))
        small_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, np.array([]), 50, 30, int(height * 0.15),
                             int(height * 0.18))

        circles = np.hstack((np.uint16(np.around(small_circles)), np.uint16(np.around(big_circles))))
        for i in circles[0,:]:
            # draw the outer circles
            cv2.circle(img, (i[0], i[1]), i[2], (0, 0, 255), 3, cv2.LINE_AA)
            # draw the centers of circles
            cv2.circle(img, (i[0], i[1]), 2, (0, 255, 0), 3, cv2.LINE_AA)

        #for testing, output circles on image
        # cv2.imwrite('gauge-%s-circles.%s' % (gauge_number, file_type), img)


        #for calibration, plot lines from center going out at every 10 degrees and add marker
        #for i from 0 to 36 (every 10 deg)

        '''
        goes through the motion of a circle and sets x and y values based on the set separation spacing.  Also adds text to each
        line.  These lines and text labels serve as the reference point for the user to enter
        NOTE: by default this approach sets 0/360 to be the +x axis (if the image has a cartesian grid in the middle), the addition
        (i+9) in the text offset rotates the labels by 90 degrees so 0/360 is at the bottom (-y in cartesian).  So this assumes the
        gauge is aligned in the image, but it can be adjusted by changing the value of 9 to something else.
        '''
        _, ncircles, R = circles.shape
        separation = 10.0 #in degrees
        interval = int(360 / separation)
        p1 = np.zeros((interval,2, ncircles))  #set empty arrays
        p2 = np.zeros((interval,2, ncircles))
        p_text = np.zeros((interval,2, ncircles))
        for i in range(0,interval):
            for j in range(0,2):
                for k_idx, k in enumerate(circles[0,:]):
                    if (j%2==0):
                        p1[i][j][k_idx] = k[0] + 0.9 * k[2] * np.cos(separation * i * 3.14 / 180) #point for lines
                    else:
                        p1[i][j][k_idx] = k[1] + 0.9 * k[2] * np.sin(separation * i * 3.14 / 180)
        text_offset_x = 10
        text_offset_y = 5
        for i in range(0, interval):
            for j in range(0, 2):
                for k_idx, k in enumerate(circles[0,:]):
                    if (j % 2 == 0):
                        p2[i][j][k_idx] = k[0] + k[2] * np.cos(separation * i * 3.14 / 180)
                        p_text[i][j][k_idx] = k[0] - text_offset_x + 1.2 * k[2] * np.cos((separation) * (i+9) * 3.14 / 180) #point for text labels, i+9 rotates the labels by 90 degrees
                    else:
                        p2[i][j][k_idx] = k[1] + k[2] * np.sin(separation * i * 3.14 / 180)
                        p_text[i][j][k_idx] = k[1] + text_offset_y + 1.2 * k[2] * np.sin((separation) * (i+9) * 3.14 / 180)  # point for text labels, i+9 rotates the labels by 90 degrees

        #add the lines and labels to the image
        for i in range(0,interval):
            for k_idx in range(ncircles):
                cv2.line(img, (int(p1[i][0][k_idx]), int(p1[i][1][k_idx])), (int(p2[i][0][k_idx]), int(p2[i][1][k_idx])),(0, 255, 0), 2)
                cv2.putText(img, '%s' %(int(i*separation)), (int(p_text[i][0][k_idx]), int(p_text[i][1][k_idx])), cv2.FONT_HERSHEY_SIMPLEX, 0.3,(0,0,0),1,cv2.LINE_AA)

        # cv2.imwrite('gauge-%s-calibration.%s' % (gauge_number, file_type), img)

        #get user input on min, max, values, and units
        # print ('gauge number: %s' %gauge_number)

        #min_angle = raw_input('Min angle (lowest possible angle of dial) - in degrees: ') #the lowest possible angle
        #max_angle = raw_input('Max angle (highest possible angle) - in degrees: ') #highest possible angle
        #min_value = raw_input('Min value: ') #usually zero
        #max_value = raw_input('Max value: ') #maximum reading of the gauge
        #units = raw_input('Enter units: ')

        #for testing purposes: hardcode and comment out raw_inputs above
        min_angle = 40
        max_angle = 320
        min_value = 0
        max_value = 30
        units = "PSI"

        # Get x, y and r values of the circles
        # x,y,r = get_xyr(circles, ncircles, R)

        return min_angle, max_angle, min_value, max_value, units, circles

    def get_current_value(self, img, circles, min_angle, max_angle, min_value, max_value, gauge_number):
        #for testing purposes
        #img = cv2.imread('gauge-%s.%s' % (gauge_number, file_type))

        gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Set threshold and maxValue
        thresh = 85
        maxValue = 255

        # for testing purposes, found cv2.THRESH_BINARY_INV to perform the best
        # th, dst1 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_BINARY);
        # th, dst2 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_BINARY_INV);
        # th, dst3 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_TRUNC);
        # th, dst4 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_TOZERO);
        # th, dst5 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_TOZERO_INV);
        # cv2.imwrite('gauge-%s-dst1.%s' % (gauge_number, file_type), dst1)
        # cv2.imwrite('gauge-%s-dst2.%s' % (gauge_number, file_type), dst2)
        # cv2.imwrite('gauge-%s-dst3.%s' % (gauge_number, file_type), dst3)
        # cv2.imwrite('gauge-%s-dst4.%s' % (gauge_number, file_type), dst4)
        # cv2.imwrite('gauge-%s-dst5.%s' % (gauge_number, file_type), dst5)

        # apply thresholding which helps for finding lines
        th, dst2 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_BINARY_INV)

        # found Hough Lines generally performs better without Canny / blurring, though there were a couple exceptions where it would only work with Canny / blurring
        #dst2 = cv2.medianBlur(dst2, 5)
        #dst2 = cv2.Canny(dst2, 50, 150)
        #dst2 = cv2.GaussianBlur(dst2, (5, 5), 0)

        # for testing, show image after thresholding
        # cv2.imwrite('gauge-%s-tempdst2.%s' % (gauge_number, file_type), dst2)

        # find lines
        # rho is set to 3 to detect more lines, easier to get more then filter them out later
        lines1 = cv2.HoughLinesP(image=dst2, rho=3, theta=np.pi / 180, threshold=100,minLineLength=10, maxLineGap=0)
        thresh = 80
        th, dst2 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_BINARY_INV)
        lines2 = cv2.HoughLinesP(image=dst2, rho=3, theta=np.pi / 180, threshold=100, minLineLength=10, maxLineGap=0)
        lines = np.vstack((lines1, lines2))
        del lines2
        del lines1


        # for i in range(0, len(lines)):
        #   for x1, y1, x2, y2 in lines[i]:
        #      cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #      cv2.imwrite('lines/gauge-%s-lines-test.%s' %(gauge_number, file_type), img)

        # remove all lines outside a given radius
        final_line_list = []

        diff1LowerBound = 0.15 #diff1LowerBound and diff1UpperBound determine how close the line should be from the center
        diff1UpperBound = 0.35
        diff2LowerBound = 0.5 #diff2LowerBound and diff2UpperBound determine how close the other point of the line should be to the outside of the gauge
        diff2UpperBound = 1.0

        for i in range(0, len(lines)):
            for x1, y1, x2, y2 in lines[i]:
                for j in circles[0, :]:
                    diff1 = self.dist_2_pts(j[0], j[1], x1, y1)  # j[0], j[1] is center of circle
                    diff2 = self.dist_2_pts(j[0], j[1], x2, y2)
                    #set diff1 to be the smaller (closest to the center) of the two), makes the math easier
                    if (diff1 > diff2):
                        temp = diff1
                        diff1 = diff2
                        diff2 = temp
                    # check if line is within an acceptable range
                    if (((diff1<diff1UpperBound*j[2]) and (diff1>diff1LowerBound*j[2]) and (diff2<diff2UpperBound*j[2])) and (diff2>diff2LowerBound*j[2])):
                        line_length = self.dist_2_pts(x1, y1, x2, y2)
                        # add to final list
                        final_line_list.append([x1, y1, x2, y2])

        #testing only, show all lines after filtering
        # for i in range(0,len(final_line_list)):
        #     x1 = final_line_list[i][0]
        #     y1 = final_line_list[i][1]
        #     x2 = final_line_list[i][2]
        #     y2 = final_line_list[i][3]
        #     cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # remove the overlapping lines
        final_line_list = self.remove_overlapping_lines(final_line_list)
        # final_line_list.pop(-2)

        # for testing purposes: draw blue lines on the image
        # idx = 1
        # for i in final_line_list:
        #     x1 = i[0]
        #     y1 = i[1]
        #     x2 = i[2]
        #     y2 = i[3]
        #     cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        #     cv2.imwrite('test/gauge-1-test%s.jpg' %(idx), img)
        #     idx = idx + 1

        #find the farthest point from the center to be what is used to determine the angle
        # x_angle = []
        # y_angle = []
        res = []
        x_angle = []
        y_angle = []
        idx = 0
        for i, j in zip(final_line_list, circles[0, :]):
            dist_pt_0 = self.dist_2_pts(j[0], j[1], i[0], i[1])
            dist_pt_1 = self.dist_2_pts(j[0], j[1], i[2], i[3])
            if (dist_pt_0 > dist_pt_1):
                x_angle.append(i[0] - j[0])
                y_angle.append(j[1] - i[1])
            else:
                x_angle.append(i[2] - j[0])
                y_angle.append(j[1] - i[3])
            # take the arc tan of y/x to find the angle
            res.append(np.arctan(np.divide(float(y_angle[idx]), float(x_angle[idx]))))
            idx = idx + 1
        #np.rad2deg(res) #coverts to degrees

        # print x_angle
        # print y_angle
        # print res
        # print np.rad2deg(res)

        #these were determined by trial and error
        res = np.rad2deg(res)
        new_values = []
        for i in range(len(res)):
            if x_angle[i] > 0 and y_angle[i] > 0:  #in quadrant I
                final_angle = 270 - res[i]
            if x_angle[i] < 0 and y_angle[i] > 0:  #in quadrant II
                final_angle = 90 - res[i]
            if x_angle[i] < 0 and y_angle[i] < 0:  #in quadrant III
                final_angle = 90 - res[i]
            if x_angle[i] > 0 and y_angle[i] < 0:  #in quadrant IV
                final_angle = 270 - res[i]

            #print final_angle

            old_min = float(min_angle)
            old_max = float(max_angle)

            new_min = float(min_value)
            new_max = float(max_value)

            old_value = final_angle

            old_range = (old_max - old_min)
            new_range = (new_max - new_min)
            new_values.append((((old_value - old_min) * new_range) / old_range) + new_min)

        return new_values

    def estimate_gauge(self, img):
        gauge_number = 1
        # name the calibration image of your gauge 'gauge-#.jpg', for example 'gauge-5.jpg'.  It's written this way so you can easily try multiple images
        min_angle, max_angle, min_value, max_value, units, circles = self.calibrate_gauge(img, gauge_number) # previously: (...), x,y,r = ...

        #feed an image (or frame) to get the current value, based on the calibration, by default uses same image as calibration
        val = self.get_current_value(img, circles, min_angle, max_angle, min_value, max_value, gauge_number)
        # print ("Current reading: %s %s" %(val, units))

