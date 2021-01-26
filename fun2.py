from lbp import LocalBinaryPatterns
from sklearn.naive_bayes import GaussianNB
import sklearn.ensemble as se
import sklearn.linear_model as skl
import time
import pickle
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from GNaiveBayes_with_Laplace import *


def isRGB(RGB):
    if RGB:
        return 'Bclassifier_RGB.pkl'
    else:
        return 'classifier.pkl'

def is_ft_RGB(RGB):
    if RGB:
        return "RGB_features.pkl"
    else:
        return "features.pkl"

def is_etc(string, RGB, norm):
    if RGB:
        string += "RGB"
    if norm:
        string += "n"
    string += ".pkl"
    return string

def create_model(object, RGB=False, skip_norm=False):
    # extract an matrix of histograms and vector of classes
    # features, classes = object.extract_multiple_images('Images/Train', RGB=RGB, skip_norm=skip_norm)

    # Load features and classes instead of extraction
    filename = "features"
    filename = is_etc(filename, RGB, skip_norm)
    file = open(filename, 'rb')
    features = pickle.load(file)
    file.close()
    file = open("classes.pkl", 'rb')
    classes = pickle.load(file)
    file.close()

    # Construct the strong classifier from image features (week classifiers)
    # AdaBoost:
    # model = se.AdaBoostClassifier(n_estimators=128, random_state=0)
    # Naive Bayes
    # model = GaussianNB()

    # List of models
    # Winner: RidgeClassifier
    # MUCH LESS INTERESTED: LinearRegression, Ridge(+CV),
    model = skl.RidgeClassifier()
    model.fit(features, classes)

    # save model into file
    filename = "RCLclassifier"
    filename = is_etc(filename, RGB, skip_norm)
    file = open(filename, 'wb')
    pickle.dump(model, file)
    file.close()

    # filename = "features"
    # filename = is_etc(filename, RGB, skip_norm)
    # file = open(filename, 'wb')
    # pickle.dump(features, file)
    # file.close()
    # file = open("classes.pkl", 'wb')
    # pickle.dump(classes, file)
    # file.close()


def tests(fname, RGB=False, proba=False, skip_norm=False, debug=False):
    filename = "RCLclassifier"
    filename = is_etc(filename, RGB, skip_norm)

    # Load model
    file = open(filename, 'rb')
    classifier = pickle.load(file)
    file.close()

    # Test trained model
    begin = time.time()
    print(LBP.advanced_predict_multiple_images(classifier, 0.59, fname, RGB=RGB, proba=proba))  # takes very long time
    end = time.time()
    print(end-begin)


if __name__ == '__main__':
    lbp_size = (8, 2)
    LBP = LocalBinaryPatterns(*lbp_size)
    RGB = False
    skip_norm = False

    args = sys.argv[1:]
    if args[0] == '1':
        RGB = True
        args.pop(0)
    if args[0] == 'n':
        skip_norm = True
        args.pop(0)

    for arg in args:
        if arg in ('--learning', '-l'):
            create_model(LBP, RGB=RGB, skip_norm=skip_norm)
        elif arg in ('--testing', '-t'):
            tests(args[0], RGB=RGB, skip_norm=skip_norm, proba=False)

    print("DONE")

