from lbp import LocalBinaryPatterns
import sklearn.ensemble as se
import time
import pickle
# import pandas as pd, csv


def isRGB(RGB):
    if RGB:
        return 'classifier_RGB.pkl'
    else:
        return 'classifier.pkl'

def create_model(object, RGB=False):
    # extract an matrix of histograms and vector of classes
    features, classes = object.extract_multiple_images('Images/Train', RGB=RGB)
    # Construct the strong classifier from image features (week classifiers)
    model = se.AdaBoostClassifier(n_estimators=features.shape[1], random_state=0)
    model.fit(features, classes)
    # save model into file
    filename = isRGB(RGB)
    file = open(filename, 'wb')
    pickle.dump(model, file)
    file.close()


def tests(RGB=False):
    filename = isRGB(RGB)

    # Load model
    file = open(filename, 'rb')
    classifier = pickle.load(file)
    file.close()

    # Test trained model
    # (without dividing images)
    # print(LBP.predict_multiple_images(classifier, path='Images/Train', proba=False))

    # # For comparison
    # _, response = LBP.predict_single_image(classifier, 'Images/Test/walshs-pyramid---south-of-cairn-36649_1280x731.jpg', 0.52)#, rows=10, columns=15, plot=False, proba=True)
    # print(response)
    begin = time.time()
    print(LBP.advanced_predict_multiple_images(classifier, 0.52))  # takes very long time
    end = time.time()
    print(end-begin)


if __name__ == '__main__':
    lbp_size = (8, 2)
    LBP = LocalBinaryPatterns(*lbp_size)

    # create_model(LBP)
    tests()

    print("DONE")

