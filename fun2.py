import cv2
import numpy as np
import matplotlib.pyplot as plt
from lbp import LocalBinaryPatterns
from imutils import paths
import sklearn.ensemble as se
# import tensorflow as tf

image_size = (300, 200)
lbp_size = (8,2)

def read_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, image_size)
    return img

def blurring(img):
    # img = cv2.GaussianBlur(img, (5, 5), 0)
    # img = cv2.bilateralFilter(img, 9, 75, 75)
    img = cv2.blur(img, (3, 3))
    return img


def extract_single_image(img, RGB=False, plot=False):
    local_bin_pat = LocalBinaryPatterns(*lbp_size)
    LBP, hist = local_bin_pat.compute_LBP(img, RGB=RGB, plot=plot)

    # Return the LBP image and the histogram
    return LBP, hist


def extract_multiple_images(path, RGB=False, plot=False, use_prev_data=False):
    # Classes of images (0 if not given object, 1 otherwise)
    classes = []
    # Features - merged histograms
    features = np.empty(0)

    # Compute histogram for every file in directory
    for imagePath in paths.list_images(path):
        _, hist = extract_single_image(read_image(imagePath), RGB=RGB, plot=plot)

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
def predict_single_image(classifier, imgPath, RGB=False, plot=False, plot_rect=False, proba=False):
    # RGB - prediction for RGB-LBP method;  plot_rect - plot a rectangle on the current window's position;
    # proba - print probability instead of full prediction in plot's title

    image = read_image(imgPath)
    # Blurring
    # image = blurring(image)

    responses = []
    # Divide image into windows (unnecessary?)
    # image_size is (300, 200), but the real one is REVERSED [cv2.resize function]
    img_size = image_size[::-1]
    percentage = 0.2 # percentage of cropped image relative to its original size
    i=0
    while percentage <= 1.0:
        x = 0
        y = 0
        cr_img_size = (int(img_size[0]*percentage), int(img_size[1]*percentage))
        while x < img_size[0] and y < img_size[1]:
            i = i+1
            cropped_image = image[x:cr_img_size[0]+x, y:cr_img_size[1]+y]

            # Plot a rectangle
            if plot:
                if not plot_rect:
                    plt.subplot(11,14,i)
                    plt.imshow(cropped_image)
                else:
                    img_with_rectangle = cv2.rectangle(image, (y,x), (cr_img_size[1]+y,cr_img_size[0]+x), (255,int((percentage+0.4)*255),int((percentage+0.4)*255)),2)
                    plt.imshow(img_with_rectangle)
                    plt.show()

            _, features = extract_single_image(cropped_image, RGB=RGB)

            if not proba:
                # if we want to see the probability instead of full prediction
                responses.append(classifier.predict(features.reshape(1,-1)))
                if plot:
                    if responses[i-1] == 1: # alternatively: if responses[i-1][0][1] >= 0.9:
                        plt.title("Pyramid")
                    else:
                        plt.title("Null")
            else:
                responses.append(classifier.predict_proba(features.reshape(1, -1)))
                if plot:
                    plt.title(responses[i - 1])

            y = int(cr_img_size[1]/2)+y
            if y >= img_size[1]:
                x = int(cr_img_size[0]/2)+x
                if x < img_size[0]:
                    y = 0
                # leave current y value for while stop condition otherwise
        percentage = percentage + 0.4
    if plot:
        plt.show()
    return responses


def predict_multiple_images(classifier, RGB=False, plot=False, proba=False):
    features2, _ = extract_multiple_images('Images/Test', RGB=RGB, plot=plot, use_prev_data=True)
    if not proba:
        predictions = classifier.predict(features2)
    else:
        predictions = classifier.predict_proba(features2)

    # plot images
    i= 1
    for imagePath in paths.list_images('Images/Test'):
        plt.subplot(6,5,i)
        plt.imshow(read_image(imagePath))

        if not proba:
            if predictions[i-1] == 0:
                plt.title("Null")
            else:
                plt.title("Pyramid")
        else:
            plt.title(predictions[i-1])
        i = i+1
    plt.show()
    return predictions


def advanced_predict_multiple_images(classifier, RGB=False, plot=False, proba=False, plot_rect=False):
    predictions = []
    for imagePath in paths.list_images('Images/Test'):
        res = 0
        responses = predict_single_image(classifier, imagePath, RGB=RGB, plot=plot, plot_rect=plot_rect, proba=proba)

        # Check every response
        for r in responses:
            # modify some condition depending on selected type of response
            if proba:
                cond = r[0][1] >= 0.6
            else:
                cond = r == 1

            if cond:
                res = 1
        # if any is equal 1 - there is a pyramid on the image
        if res == 1:
            predictions.append(1)
        else:
            predictions.append(0)

        # plot images
        i = 1
        plt.subplot(6,5,i)
        plt.imshow(read_image(imagePath))
        if not proba:
            if predictions[i-1] == 0:
                plt.title("Null")
            else:
                plt.title("Pyramid")
        else:
            plt.title(predictions[i-1])
        i = i+1
    plt.show()
    return predictions




def Main():
    # extract an matrix of histograms and vector of classes
    features, classes = extract_multiple_images('Images/Train')

    # Construct the strong classifier from image features (week classifier)
    classifier = se.AdaBoostClassifier(n_estimators=features.shape[1], random_state=0)
    classifier.fit(features, classes)

    # Test trained model
    print(predict_multiple_images(classifier, proba=False))

    # For comparison
    advanced_predict_multiple_images(classifier, proba=True)
    print("DONE")



if __name__ == '__main__':
    Main()


