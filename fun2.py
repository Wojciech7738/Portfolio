from lbp import LocalBinaryPatterns
import sklearn.ensemble as se
import time
# import pandas as pd, csv

def Main():
    lbp_size = (8, 2)
    LBP = LocalBinaryPatterns(*lbp_size)
    # extract an matrix of histograms and vector of classes
    begin = time.time()
    features, classes = LBP.extract_multiple_images('Images/Train')

    # Construct the strong classifier from image features (week classifier)
    classifier = se.AdaBoostClassifier(n_estimators=features.shape[1], random_state=0)
    classifier.fit(features, classes)

    # Test trained model
    # (without dividing images)
    print(LBP.predict_multiple_images(classifier, proba=False))

    # For comparison
    _, response = LBP.predict_single_image(classifier, 'Images/Test/walshs-pyramid---south-of-cairn-36649_1280x731.jpg', 0.52, rows=10, columns=15, plot=True, proba=True)
    print(response)
    # advanced_predict_multiple_images(classifier, 0.52) # takes very long time
    end = time.time()
    print(end-begin)
    print("DONE")



if __name__ == '__main__':
    Main()
