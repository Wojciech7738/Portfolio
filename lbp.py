import numpy as np
import cv2
import matplotlib.pyplot as plt
from imutils import paths

def __local_binary_pattern__(image, square_side):
    lbp_image = np.zeros(image.shape, dtype=np.int)
    Hist = None
    # 1: divide image into grid
    for r in range(3):
        for c in range(4):  # columns
            new_img = image[square_side * r:square_side * (r + 1),
                      square_side * c:square_side * (c + 1)]
            for i in range(square_side):
                for j in range(square_side):
                    binary_values = []
                    current = new_img[i, j]
                    nei_position = neighbour_positions(i, j)
                    for k in range(len(nei_position)):
                        # 2: compute LBP
                        if square_side * r + nei_position[k][0] < 0 or \
                                square_side * c + nei_position[k][1] < 0:
                            binary_values.append(0)
                        else:
                            if nei_position[k][0] >= square_side or nei_position[k][1] >= square_side:
                                if square_side * r + nei_position[k][0] >= image.shape[0] or \
                                        square_side * c + nei_position[k][1] >= image.shape[1]:
                                    # if given point is beyond the image - write 0
                                    binary_values.append(0)
                                else:
                                    __cond_check__(image, square_side * r + nei_position[k][0],
                                                        square_side * c + nei_position[k][1], current,
                                                        binary_values)
                            else:
                                __cond_check__(new_img, nei_position[k][0], nei_position[k][1], current,
                                                    binary_values)
                    # convert into decimal
                    value = int(bin(int(''.join(map(str, binary_values)), 2)), 2)
                    lbp_image[square_side * r + i, square_side * c + j] = value

            # create histogram of single window
            hist, _ = np.histogram(lbp_image[square_side * r:square_side * (r + 1),
                      square_side * c:square_side * (c + 1)].ravel(), bins=np.arange(0, 256, 1))
            # Concatenate histograms
            if type(Hist) != np.ndarray:
                Hist = hist
            else:
                Hist = np.concatenate((Hist,hist))
    return Hist, lbp_image

def neighbour_positions(row, col):
    return [(row, col + 1), (row + 1, col + 1), (row + 1, col), (row + 1, col - 1), (row, col - 1),
            (row - 1, col - 1), (row - 1, col), (row - 1, col + 1)]

def __cond_check__(img, p1, p2, current, binary_values):
    if img[p1][p2] < current:
        binary_values.append(0)
    else:
        binary_values.append(1)



class LocalBinaryPatterns:
    def __init__(self, nPoints, radius_of_scanning):
        self.nPoints = nPoints
        self.radius_of_scanning = radius_of_scanning
        # window's side
        self.square_side = 104
        self.image_size = (416, 312)

    def __read_image__(self, imgPath):
        img = cv2.imread(imgPath)
        return cv2.resize(img, (416, 312))

    def describe(self, IMG, RGB=False):
        if RGB == True:
            i = 3
        else:
            i = 1
        for j in range(i):
            if RGB == True:
                image = IMG[:, :, j]
            else:
                image = IMG
            image = np.ascontiguousarray(image, dtype=np.int)
            hist, lbp = __local_binary_pattern__(image, self.square_side)
            # normalize the histogram (values from 0 to 1)
            hist = hist.astype("float")
            hist = (hist-hist.min())/(hist.max()-hist.min())

            if j == 0:
                Hist = hist
            else:
                # Concatenate if given method is RGB-LBP
                Hist = np.concatenate((Hist, hist))
        # return the histogram of Local Binary Patterns
        # obviously, for RGB-LBP it returns only LBP image for the last channel
        return Hist, lbp


    def compute_LBP(self, img, RGB=False, plot=False):
        LBP = None
        if RGB == False:
            method_name = "LBP"
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # only histogram is needed for object detection
            hist, LBP = self.describe(gray_img)

        else:
            method_name = "RGB-LBP"
            hist, LBP = self.describe(img, RGB=True)
        # Show an image
        if plot:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.show()
        return LBP, hist

    def blurring(self, img):
        # img = cv2.GaussianBlur(img, (5, 5), 0)
        # img = cv2.bilateralFilter(img, 9, 75, 75)
        img = cv2.blur(img, (3, 3))
        return img



    def extract_single_image(self, img, RGB=False):
        LBP, hist = self.compute_LBP(img, RGB=RGB)
        # Return the LBP image and the histogram
        return LBP, hist


    def extract_multiple_images(self, path, RGB=False, use_prev_data=False):
        # Classes of images (0 if not given object, 1 otherwise)
        classes = []
        # Features - merged histograms
        features = np.empty(0)

        # Compute histogram for every file in directory
        for imagePath in paths.list_images(path):
            _, hist = self.extract_single_image(self.__read_image__(imagePath), RGB=RGB)

            # Create a list of classes (0 if there is "notpir" in filename)
            if not use_prev_data:
                if "notpir" in imagePath:
                    classes.append(0)
                else:
                    classes.append(1)

            # The image features which will be returned
            if len(features) == 0:
                features = hist
            else:
                features = np.vstack((features, hist))

        # Convert classes into numpy array
        classes = np.asarray(classes)
        return features, classes





    # Method which divides single image into windows
    def predict_single_image(self, classifier, imgPath, threshold, rows=11, columns=14, RGB=False, plot=False, plot_rect=False, proba=False):
        # RGB - prediction for RGB-LBP method;      plot_rect - plot a rectangle on the current window's position to see
        # if evetything works fine;     rows and columns - (...) on plot;   plot - show a plot;
        # threshold - value of probability needed for each sample for being classified as "1"
        # proba - print probability instead of full prediction in plot's title

        image = self.__read_image__(imgPath)
        # Blurring
        # image = blurring(image)

        responses = []
        # Divide image into windows
        # image_size is (300, 200), but the real one is REVERSED [cv2.resize function]
        img_size = self.image_size[::-1]
        percentage = 0.2 # percentage of cropped image relative to its original size
        counter = 0.2 # is added in every loop iteration
        i=0
        while percentage < 1.09:
            x = 0
            y = 0
            cr_img_size = (int(img_size[0]*percentage), int(img_size[1]*percentage))
            while x < img_size[0] and y < img_size[1]:
                i = i+1
                cropped_image = image[x:cr_img_size[0]+x, y:cr_img_size[1]+y]
                cropped_image = cv2.resize(cropped_image, self.image_size)

                # Plot a rectangle
                if plot:
                    if not plot_rect:
                        plt.subplot(rows,columns,i)
                        plt.imshow(cropped_image)
                    else:
                        img_with_rectangle = cv2.rectangle(image, (y,x), (cr_img_size[1]+y,cr_img_size[0]+x), (255,int((percentage+0.4)*255),int((percentage+0.4)*255)),2)
                        plt.imshow(img_with_rectangle)
                        plt.show()

                _, features = self.extract_single_image(cropped_image, RGB=RGB)

                if not proba:
                    # if we want to see the probability instead of full prediction
                    responses.append(classifier.predict(features.reshape(1,-1)))
                    if plot:
                        if responses[i-1] == 1: # alternatively: if responses[i-1][0][1] >= 0.55:
                            plt.title("Pyramid")
                        else:
                            plt.title("Null")
                else:
                    responses.append(classifier.predict_proba(features.reshape(1, -1)))
                    # round to two decimal places
                    responses[i - 1] = np.around(responses[i-1], 2)
                    if plot:
                        plt.title(str(responses[i - 1]))

                y = int(cr_img_size[1]/2)+y
                if y >= img_size[1]:
                    x = int(cr_img_size[0]/2)+x
                    if x < img_size[0]:
                        y = 0
                    # leave current y value for while stop condition otherwise
            percentage = percentage + counter
            if percentage >= 0.6:
                counter = 0.4
        if plot:
            plt.show()

        # Check every response
        res = 0
        for r in responses:
            # modify some condition depending on selected type of response
            if proba:
                cond = r[0][1] >= threshold
            else:
                cond = r == 1
            if cond:
                res = 1
        # if any is equal 1 - there is a pyramid on the image
        return responses, res


    def predict_multiple_images(self, classifier, path='Images/Test', RGB=False, proba=False):
        features2, _ = self.extract_multiple_images(path, RGB=RGB, use_prev_data=True)
        if not proba:
            predictions = classifier.predict(features2)
        else:
            predictions = classifier.predict_proba(features2)

        # plot images
        i= 1
        for imagePath in paths.list_images('Images/Test'):
            plt.subplot(6,5,i)
            plt.imshow(self.__read_image__(imagePath))

            if not proba:
                if predictions[i-1] == 0:
                    plt.title("Null")
                else:
                    plt.title("Pyramid")
            else:
                plt.title(str(predictions[i-1]))
            i = i+1
        plt.show()
        return predictions



    def advanced_predict_multiple_images(self, classifier, threshold, directory='Images/Test', RGB=False, plot=False, plot_rect=False):
        predictions = []
        i = 1
        for imagePath in paths.list_images(directory):
            _, resp = self.predict_single_image(classifier, imagePath, threshold, RGB=RGB, plot=plot, plot_rect=plot_rect, proba=True)
            predictions.append(resp)
            # plot images
            plt.subplot(6,5,i)
            plt.imshow(self.__read_image__(imagePath))
            if predictions[i-1] == 0:
                plt.title("Null")
            else:
                plt.title("Pyramid")
            i = i+1
        plt.show()
        return predictions

