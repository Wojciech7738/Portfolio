from lbp import LocalBinaryPatterns
import sklearn.ensemble as se
import time
import pickle
import sys


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


def tests(fname, RGB=False, proba=False, debug=False):
    filename = isRGB(RGB)

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

    args = sys.argv[1:]
    if args[0] == '1':
        RGB = True
        args.pop(0)

    for arg in args:
        if arg in ('--learning', '-l'):
            create_model(LBP, RGB=RGB)
        elif arg in ('--testing', '-t'):
            tests(args[0], RGB=RGB, proba=True)

    print("DONE")

