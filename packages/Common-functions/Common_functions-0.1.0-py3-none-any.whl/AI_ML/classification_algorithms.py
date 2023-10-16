import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB

def run_classifiers(csv_file, target_column):
    # Load data from CSV file
    data = pd.read_csv(csv_file)

    # Split data into features and target
    X = data.drop(target_column, axis=1)
    y = data[target_column]

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Random Forest Classifier
    rf_classifier = RandomForestClassifier()
    rf_classifier.fit(X_train, y_train)
    rf_accuracy = rf_classifier.score(X_test, y_test)

    # Decision Tree Classifier
    dt_classifier = DecisionTreeClassifier()
    dt_classifier.fit(X_train, y_train)
    dt_accuracy = dt_classifier.score(X_test, y_test)

    # K-Nearest Neighbors Classifier
    knn_classifier = KNeighborsClassifier()
    knn_classifier.fit(X_train, y_train)
    knn_accuracy = knn_classifier.score(X_test, y_test)

    # AdaBoost Classifier
    ada_classifier = AdaBoostClassifier()
    ada_classifier.fit(X_train, y_train)
    ada_accuracy = ada_classifier.score(X_test, y_test)

    # SGD Classifier
    sgd_classifier = SGDClassifier()
    sgd_classifier.fit(X_train, y_train)
    sgd_accuracy = sgd_classifier.score(X_test, y_test)

    # Extra Trees Classifier
    et_classifier = ExtraTreesClassifier()
    et_classifier.fit(X_train, y_train)
    et_accuracy = et_classifier.score(X_test, y_test)

    # Gaussian Naive Bayes Classifier
    nb_classifier = GaussianNB()
    nb_classifier.fit(X_train, y_train)
    nb_accuracy = nb_classifier.score(X_test, y_test)

    # Return accuracy scores
    return {
        'Random Forest': rf_accuracy,
        'Decision Tree': dt_accuracy,
        'K-Nearest Neighbors': knn_accuracy,
        'AdaBoost': ada_accuracy,
        'SGD': sgd_accuracy,
        'Extra Trees': et_accuracy,
        'Gaussian Naive Bayes': nb_accuracy
    }
