from lbp import LocalBinaryPatterns
import sklearn.ensemble as se
import sklearn.linear_model as skl
import time
import pickle
import sys


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

def create_model(object, n_est, RGB=False, skip_norm=False, use_sklearn=False):
    # n_est - number of estimators;     RGB - use RGB-LBP;      skip_norm - skip normalization of features;
    # use_sklearn - use the sklearn implementation of LBP instead of the slowest one in the world

    # extract an matrix of histograms and vector of classes
    features, classes = object.extract_multiple_images('Images/Train', RGB=RGB, skip_norm=skip_norm, use_sklearn=use_sklearn)

    # Load features and classes instead of extraction
    # filename = "features"
    # filename = is_etc(filename, RGB, skip_norm)
    # file = open(filename, 'rb')
    # features = pickle.load(file)
    # file.close()
    # file = open("classes.pkl", 'rb')
    # classes = pickle.load(file)
    # file.close()

    # Construct the strong classifier from image features (week classifiers)
    model = se.AdaBoostClassifier(n_estimators=n_est, random_state=0)
    # Learn the model
    model.fit(features, classes)
    # save model into file
    filename = model.__name__
    filename = is_etc(filename, RGB, skip_norm)
    file = open(filename, 'wb')
    pickle.dump(model, file)
    file.close()

    # Save features and classes into a file
    filename = "features"
    filename = is_etc(filename, RGB, skip_norm)
    file = open(filename, 'wb')
    pickle.dump(features, file)
    file.close()
    file = open("classes.pkl", 'wb')
    pickle.dump(classes, file)
    file.close()


def tests(fname, RGB=False, proba=False, skip_norm=False, debug=False):
    models = [skl.LinearRegression, skl.RidgeCV]
    # models = [se.RandomForestClassifier]
    names = []
    for m in models:
        names.append(m.__name__)
    for i in range(len(models)):
        filename = names[i]
        filename = is_etc(filename, RGB, skip_norm)
        fname = names[i]

        # Load model
        file = open(filename, 'rb')
        classifier = pickle.load(file)
        file.close()
        # Test trained model
        begin = time.time()
        # print(LBP.predict_single_image(classifier, 'Images/Test/great-pyramid-996800.jpeg', 0.5, RGB=RGB, proba=proba, debug=True))
        # print(LBP.advanced_predict_multiple_images(classifier, 0.55, fname, RGB=RGB, proba=proba))
        print(LBP.predict_multiple_images(classifier, RGB=RGB, proba=proba, use_sklearn=True))
        end = time.time()
        print(end-begin)
        print("\n")


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
            create_model(LBP, int(args[0]), RGB=RGB, skip_norm=skip_norm)
        elif arg in ('--testing', '-t'):
            tests(args[0], RGB=RGB, skip_norm=skip_norm, proba=True)

    print("DONE")

