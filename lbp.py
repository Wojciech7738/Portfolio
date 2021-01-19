import numpy as np
import cv2
import matplotlib.pyplot as plt
from imutils import paths
from skimage import feature
from lbp_core import LBP_core
# from c_python.lbp_cy import LBP_core

class LocalBinaryPatterns(LBP_core):
    def __init__(self, nPoints, radius_of_scanning):
        self.nPoints = nPoints
        self.radius_of_scanning = radius_of_scanning
        # window's side
        self.__square_side__ = 104
        self.image_size = (416, 312)

    def __read_image__(self, imgPath):
        img = cv2.imread(imgPath)
        return cv2.resize(img, (416, 312))

    def describe(self, IMG, RGB=False, use_sklearn=False):
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
            if not use_sklearn:
                hist, lbp = self.__local_binary_pattern__(image, self.__square_side__)
            else:
                lbp = feature.local_binary_pattern(image, self.nPoints, self.radius_of_scanning)
                hist, _ = np.histogram(lbp, bins=np.arange(0, 256, 1))
            # normalize the histogram (values from 0 to 1)
            hist = hist.astype("float")
            hist = (hist-hist.min())/(hist.max()-hist.min())

            if j == 0:
                Hist = hist
            else:
                # Concatenate if given method is RGB-LBP
                Hist = np.concatenate((Hist, hist))
        # Return the histogram of Local Binary Patterns
        # For RGB-LBP it returns only LBP image for the last channel
        return Hist, lbp

    def blurring(self, img):
        # img = cv2.GaussianBlur(img, (5, 5), 0)
        # img = cv2.bilateralFilter(img, 9, 75, 75)
        img = cv2.blur(img, (3, 3))
        return img



    def extract_single_image(self, img, RGB=False, plot=False, use_sklearn=False):
        LBP = None
        if RGB == False:
            method_name = "LBP"
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # only histogram is needed for object detection
            hist, LBP = self.describe(gray_img)

        else:
            method_name = "RGB-LBP"
            hist, LBP = self.describe(img, RGB=True, use_sklearn=use_sklearn)
        # Show an image
        if plot:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.show()
        return LBP, hist

    def extract_multiple_images(self, path, RGB=False, use_prev_data=False, use_sklearn=False):
        # Classes of images (0 if not given object, 1 otherwise)
        classes = []
        # Features - merged histograms
        features = np.empty(0)

        # Compute histogram for every file in directory
        for imagePath in paths.list_images(path):
            _, hist = self.extract_single_image(self.__read_image__(imagePath), RGB=RGB, use_sklearn=use_sklearn)

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
    def predict_single_image(self, classifier, imgPath, threshold, RGB=False, use_sklearn=False, proba=False, debug=False):
        # RGB - prediction for RGB-LBP method;
        # debug - plot a single window to see if everything works fine;
        # threshold - value of probability needed for each sample for being classified as "1";
        # use_sklearn - use an sklearn implementation of LBP instead of the slowest one in the world;
        # proba - print probability instead of full prediction in plot's title

        image = self.__read_image__(imgPath)
        # Blurring
        # image = blurring(image)

        responses = []
        # Divide image into windows
        # image_size is (300, 200), but the real one is REVERSED (see cv2.resize function)
        img_size = self.image_size[::-1]
        percentage = 0.2 # percentage of cropped image relative to its original size
        counter = 0.2 # is added in every loop iteration
        i=0
        res = 0
        while percentage < 1.09:
            x = 0
            y = 0
            # TO REMOVE !!!
            cr_img_size = (int(img_size[0]*percentage), int(img_size[1]*percentage))
            while x < img_size[0] and y < img_size[1]:
                i = i+1
                cropped_image = image[x:cr_img_size[0]+x, y:cr_img_size[1]+y]
                cropped_image = cv2.resize(cropped_image, self.image_size)

                _, features = self.extract_single_image(cropped_image, RGB=RGB, use_sklearn=use_sklearn)

                if not proba:
                    # if we want to see the probability instead of full prediction
                    responses.append(classifier.predict(features.reshape(1,-1)))
                    if responses[i-1] == 1:
                        image = cv2.rectangle(image, (y, x), (cr_img_size[1] + y, cr_img_size[0] + x),
                        (255, 192, 203), 2)
                        res = 1
                else:
                    responses.append(classifier.predict_proba(features.reshape(1, -1)))
                    # round to two decimal places
                    responses[i - 1] = np.around(responses[i-1], 2)
                    if responses[i - 1][0][1] >= threshold:
                        image = cv2.rectangle(image, (y, x), (cr_img_size[1] + y, cr_img_size[0] + x),
                                              (255, 192, 203), 2)
                        res = 1

                y = int(cr_img_size[1]/2)+y
                if y >= img_size[1]:
                    x = int(cr_img_size[0]/2)+x
                    if x < img_size[0]:
                        y = 0
                    # leave current y value for while stop condition otherwise

                # It will be removed in the future
                if debug:
                    fig, ax = plt.subplots(1,1)
                    ax.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
                    plt.title(str(responses[i-1]))
                    somestring = "DEBUG/p2"
                    if proba:
                        somestring="DEBUG/p2/AAAAAAAAA"
                    fig.savefig(somestring+imgPath[12:16]+str(i)+".png")
                    plt.close(fig)
            percentage = percentage + counter
            if percentage >= 0.6:
                counter = 0.4

        # if any is equal 1 - there is a pyramid on the image
        return responses, res, image


    def predict_multiple_images(self, classifier, path='Images/Test', RGB=False, proba=False):
        features2, _ = self.extract_multiple_images(path, RGB=RGB, use_prev_data=True)
        if not proba:
            predictions = classifier.predict(features2)
        else:
            predictions = classifier.predict_proba(features2)

        # plot images
        i= 1
        if path == 'Images/Test':
            x = 6
            y = 5
        else:
            x = 13
            y = 12
        for imagePath in paths.list_images(path):
            plt.subplot(x,y,i)
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


    def advanced_predict_multiple_images(self, classifier, threshold, fname, directory='Images/Test', RGB=False, use_sklearn=False, proba=False):
        predictions = []
        images = []
        i = 0
        # new:
        rows = 4
        cols = 4
        fig, ax = plt.subplots(rows, cols, figsize=(19.20,10.80))
        fig.tight_layout()
        for imagePath in paths.list_images(directory):
            _, resp, img = self.predict_single_image(classifier, imagePath, threshold, RGB=RGB, use_sklearn=use_sklearn, proba=proba)
            predictions.append(resp)
            images.append(img)

            # plot images
            # old:
            # plt.subplot(4,4,i)
            # plt.imshow(cv2.cvtColor(images[i-1], cv2.COLOR_BGR2RGB))

            # new:
            ax[int(i/cols), i%cols].imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
            ax[int(i/cols), i%cols].axis('off')

            if predictions[i] == 0:
                ax[int(i/cols), i%cols].set_title('Null')
            else:
                ax[int(i/cols), i%cols].set_title('Pyramid')
            i = i+1
        fig.savefig("RESULTS/"+fname+".png")
        plt.close(fig)
        # plt.show()
        return predictions

