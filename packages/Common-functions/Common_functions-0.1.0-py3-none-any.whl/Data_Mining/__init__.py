import pandas as pd
from sklearn.preprocessing import LabelEncoder
from matplotlib.colors import ListedColormap
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans, AgglomerativeClustering
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans, AgglomerativeClustering
import warnings
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.cluster import AgglomerativeClustering
import numpy as np
warnings.filterwarnings("ignore")
def data_exploration():
    dataset_path = input("Enter the dataset path: ")

    if not os.path.exists(dataset_path):
        print("File not found. Please provide a valid dataset path.")
        return

    try:
        # Load data
        data = pd.read_csv(dataset_path)

        # Print column types
        print("Column Types:")
        print(data.dtypes)

        # Print column names
        print("Column Names:")
        print(data.columns)

        # Print head
        print("Head:")
        print(data.head())

        # Print tail
        print("Tail:")
        print(data.tail())

        # Print mean
        print("Mean:")
        print(data.mean())

        # Print standard deviation
        print("Standard Deviation:")
        print(data.std())

    except Exception as e:
        print("An error occurred:", str(e))


def data_visualization():
    dataset_path = input("Enter the dataset path: ")

    if not os.path.exists(dataset_path):
        print("File not found. Please provide a valid dataset path.")
        return

    try:
        # Load data
        data = pd.read_csv(dataset_path)

        # Pairplot
        sns.pairplot(data)
        plt.show()

        # Distribution plot
        for column in data.columns:
            if data[column].dtype == 'float64':
                sns.displot(data[column])
                plt.title(column)
                plt.show()

        # Box plot
        sns.boxplot(data=data)
        plt.show()

        # Scatter plot
        for column1 in data.columns:
            if data[column1].dtype == 'float64':
                for column2 in data.columns:
                    if data[column2].dtype == 'float64' and column1 != column2:
                        sns.scatterplot(data=data, x=column1, y=column2)
                        plt.xlabel(column1)
                        plt.ylabel(column2)
                        plt.show()

    except Exception as e:
        print("An error occurred:", str(e))

def data_preprocessing():
    dataset_path = input("Enter the dataset path: ")

    if not os.path.exists(dataset_path):
        print("File not found. Please provide a valid dataset path.")
        return

    try:
        # Load data
        data = pd.read_csv(dataset_path)

        # Handling missing values
        data.fillna(0, inplace=True)

        # Print pre-processed data
        print("Pre-processed Data:")
        print(data)

    except Exception as e:
        print("An error occurred:", str(e))


def normalization():
    dataset_path = input("Enter the dataset path: ")

    if not os.path.exists(dataset_path):
        print("File not found. Please provide a valid dataset path.")
        return

    try:
        # Load data
        data = pd.read_csv(dataset_path)

        # Perform min-max normalization
        scaler = MinMaxScaler()
        normalized_data = scaler.fit_transform(data)

        # Print normalized data
        print("Normalized Data:")
        print(normalized_data)

    except Exception as e:
        print("An error occurred:", str(e))

def standardization():
    dataset_path = input("Enter the dataset path: ")

    if not os.path.exists(dataset_path):
        print("File not found. Please provide a valid dataset path.")
        return

    try:
        # Load data
        data = pd.read_csv(dataset_path)

        # Perform standardization
        scaler = StandardScaler()
        standardized_data = scaler.fit_transform(data)

        # Print standardized data
        print("Standardized Data:")
        print(standardized_data)

    except Exception as e:
        print("An error occurred:", str(e))


def data_reduction():
    dataset_path = input("Enter the dataset path: ")

    if not os.path.exists(dataset_path):
        print("File not found. Please provide a valid dataset path.")
        return

    try:
        # Load data
        data = pd.read_csv(dataset_path)

        # Perform PCA
        pca = PCA(n_components=2)
        reduced_data = pca.fit_transform(data)

        # Print reduced data
        print("Reduced Data:")
        print(reduced_data)

    except Exception as e:
        print("An error occurred:", str(e))



def binary_logistic_regression():
    dataset_path = input("Enter the dataset path: ")

    if not os.path.exists(dataset_path):
        print("File not found. Please provide a valid dataset path.")
        return

    target_column = input("Enter the name of the target column: ")

    try:
        # Load data
        data = pd.read_csv(dataset_path)

        # Perform binary logistic regression
        X = data.drop(target_column, axis=1)
        y = data[target_column]
        model = LogisticRegression()
        model.fit(X, y)

        # Perform predictions
        # ...
        return model
    except Exception as e:
        print("An error occurred:", str(e))


def decision_tree_classification():
    dataset_path = input("Enter the dataset path: ")
    print("Step 1: Loading the dataset...")
    time.sleep(2)  # Delay for 2 seconds

    if not os.path.exists(dataset_path):
        print("File not found. Please provide a valid dataset path.")
        return

    target_column = input("Enter the name of the target column: ")

    try:
        # Load data
        data = pd.read_csv(dataset_path)
        print("Step 2: Data loaded successfully.")
        time.sleep(2)  # Delay for 2 seconds

        # Perform decision tree classification
        X = data.drop(target_column, axis=1)
        y = data[target_column]
        print("Step 3: Performing decision tree classification...")
        time.sleep(2)  # Delay for 2 seconds

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print("Step 4: Splitting data into training and testing sets...")
        time.sleep(2)  # Delay for 2 seconds

        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)
        print("Step 5: Training the decision tree classifier...")
        time.sleep(2)  # Delay for 2 seconds

        # Perform predictions on the test set
        y_pred = model.predict(X_test)
        print("Step 6: Making predictions on the test set...")
        time.sleep(2)  # Delay for 2 seconds

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        print("Step 7: Model evaluation complete.")
        print("Model accuracy:", accuracy)
        print("Classification report:\n", report)

        return model
    except Exception as e:
        print("An error occurred:", str(e))

def naive_bayes_classification():
    dataset_path = input("Enter the dataset path: ")
    print("Step 1: Loading the dataset...")
    time.sleep(2)  # Delay for 2 seconds

    if not os.path.exists(dataset_path):
        print("File not found. Please provide a valid dataset path.")
        return

    target_column = input("Enter the name of the target column: ")

    try:
        # Load data
        data = pd.read_csv(dataset_path)
        print("Step 2: Data loaded successfully.")
        time.sleep(2)  # Delay for 2 seconds

        # Perform Naive Bayes classification
        X = data.drop(target_column, axis=1)
        y = data[target_column]
        print("Step 3: Performing Naive Bayes classification...")
        time.sleep(2)  # Delay for 2 seconds

        model = GaussianNB()
        model.fit(X, y)
        print("Step 4: Naive Bayes classification model trained.")
        time.sleep(2)  # Delay for 2 seconds

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print("Step 5: Splitting data into training and testing sets...")
        time.sleep(2)  # Delay for 2 seconds

        # Make predictions on the test set
        y_pred = model.predict(X_test)

        # Evaluate the Naive Bayes model
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        print("Step 6: Model evaluation complete.")
        print("Model accuracy:", accuracy)
        print("Classification report:\n", report)

        return model
    except Exception as e:
        print("An error occurred:", str(e))

def knn_classification():
    dataset_path = input("Enter the dataset path: ")
    print("Step 1: Loading the dataset...")
    time.sleep(2)  # Delay for 2 seconds

    if not os.path.exists(dataset_path):
        print("File not found. Please provide a valid dataset path.")
        return

    target_column = input("Enter the name of the target column: ")

    try:
        # Load data
        data = pd.read_csv(dataset_path)
        print("Step 2: Data loaded successfully.")
        time.sleep(2)  # Delay for 2 seconds

        # Perform KNN classification
        X = data.drop(target_column, axis=1)
        y = data[target_column]
        print("Step 3: Performing KNN classification...")
        time.sleep(2)  # Delay for 2 seconds

        model = KNeighborsClassifier()
        model.fit(X, y)
        print("Step 4: KNN classification model trained.")
        time.sleep(2)  # Delay for 2 seconds

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print("Step 5: Splitting data into training and testing sets...")
        time.sleep(2)  # Delay for 2 seconds

        # Make predictions on the test set
        y_pred = model.predict(X_test)

        # Evaluate the KNN model
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        print("Step 6: Model evaluation complete.")
        print("Model accuracy:", accuracy)
        print("Classification report:\n", report)

        return model
    except Exception as e:
        print("An error occurred:", str(e))




def frequent_item_set_mining():
    dataset_path = input("Enter the dataset path: ")
    print("Step 1: Loading the dataset...")
    time.sleep(2)  # Delay for 2 seconds

    if not os.path.exists(dataset_path):
        print("File not found. Please provide a valid dataset path.")
        return

    min_support = float(input("Enter the minimum support: "))
    min_threshold = float(input("Enter the minimum threshold: "))

    try:
        # Load data
        data = pd.read_csv(dataset_path)
        print("Step 2: Data loaded successfully.")
        time.sleep(2)  # Delay for 2 seconds

        # Perform frequent item set mining
        print("Step 3: Performing frequent item set mining...")
        frequent_itemsets = apriori(data, min_support=min_support, use_colnames=True)
        time.sleep(2)  # Delay for 2 seconds

        # Generate association rules
        print("Step 4: Generating association rules...")
        rules = association_rules(frequent_itemsets, metric="support", min_threshold=min_threshold)
        time.sleep(2)  # Delay for 2 seconds

        # Print frequent itemsets and association rules
        print("Step 5: Printing results...")
        print("Frequent Itemsets:")
        print(frequent_itemsets)
        print("Association Rules:")
        print(rules)

    except Exception as e:
        print("An error occurred:", str(e))



def linear_regression():
    dataset_path = input("Enter the dataset path: ")
    print("Step 1: Loading the dataset...")
    time.sleep(2)  # Delay for 2 seconds

    if not os.path.exists(dataset_path):
        print("File not found. Please provide a valid dataset path.")
        return

    target_column = input("Enter the name of the target column: ")

    try:
        # Load data
        data = pd.read_csv(dataset_path)
        print("Step 2: Data loaded successfully.")
        time.sleep(2)  # Delay for 2 seconds

        # Perform linear regression
        X = data.drop(target_column, axis=1)
        y = data[target_column]
        print("Step 3: Performing linear regression...")
        time.sleep(2)  # Delay for 2 seconds

        model = LinearRegression()
        model.fit(X, y)
        print("Step 4: Linear regression model trained.")
        time.sleep(2)  # Delay for 2 seconds

        # Perform predictions
        print("Step 5: Model Coefficients:", model.coef_)
        print("Step 6: Model Intercept:", model.intercept_)
        time.sleep(2)  # Delay for 2 seconds

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print("Step 7: Splitting data into training and testing sets...")
        time.sleep(2)  # Delay for 2 seconds

        # Make predictions on the test set
        y_pred = model.predict(X_test)

        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print("Step 8: Model evaluation complete.")
        print("Mean Squared Error (MSE):", mse)
        print("R-squared (R2):", r2)

    except Exception as e:
        print("An error occurred:", str(e))





def kmeans_clustering():
    dataset_path = input("Enter the dataset path: ")

    if not os.path.exists(dataset_path):
        print("File not found. Please provide a valid dataset path.")
        return

    num_clusters = int(input("Enter the number of clusters: "))

    try:
        # Load data
        data = pd.read_csv(dataset_path)
        print("Step 1: Data loaded successfully.")
        time.sleep(2)  # Delay for 2 seconds

        # Perform PCA to automatically select relevant columns
        pca = PCA(n_components=2)  # You can adjust the number of components as needed
        reduced_data = pca.fit_transform(data)
        print("Step 2: PCA performed for dimensionality reduction.")
        time.sleep(2)  # Delay for 2 seconds

        # Perform K-means clustering on the reduced data
        kmeans = KMeans(n_clusters=num_clusters)
        clusters = kmeans.fit_predict(reduced_data)
        print("Step 3: K-means clustering performed.")
        time.sleep(2)  # Delay for 2 seconds

        # Print cluster assignments
        print("Cluster Assignments:")
        print(clusters)
        time.sleep(2)  # Delay for 2 seconds

        # Visualize clusters
        plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=clusters)
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.title('K-means Clustering')
        plt.show()

    except Exception as e:
        print("An error occurred:", str(e))




def hierarchical_clustering():
    dataset_path = input("Enter the dataset path: ")
    print("Step 1: Loading the dataset...")
    time.sleep(2)  # Delay for 2 seconds

    if not os.path.exists(dataset_path):
        print("File not found. Please provide a valid dataset path.")
        return

    try:
        # Load data
        data = pd.read_csv(dataset_path)
        print("Step 2: Data loaded successfully.")
        time.sleep(2)  # Delay for 2 seconds

        # Automatically choose two columns to plot
        if len(data.columns) < 2:
            print("Dataset does not have enough columns to perform clustering.")
            return

        # Select the first two numeric columns for plotting
        columns_to_plot = data.select_dtypes(include=['number']).iloc[:, :2]

        # Perform hierarchical clustering
        num_clusters = int(input("Enter the number of clusters: "))
        clustering = AgglomerativeClustering(n_clusters=num_clusters, linkage='ward')
        clusters = clustering.fit_predict(columns_to_plot)
        print("Step 3: Hierarchical clustering performed.")
        time.sleep(2)  # Delay for 2 seconds

        # Print cluster assignments
        print("Cluster Assignments:")
        print(clusters)
        time.sleep(2)  # Delay for 2 seconds

        # Visualize clusters
        plt.scatter(columns_to_plot.iloc[:, 0], columns_to_plot.iloc[:, 1], c=clusters)
        plt.xlabel(columns_to_plot.columns[0])
        plt.ylabel(columns_to_plot.columns[1])
        plt.title('Hierarchical Clustering')
        plt.show()
        print("Step 4: Clustering visualization.")
    except Exception as e:
        print("An error occurred:", str(e))


import networkx as nx
import os

def social_network_analysis():
    dataset_path = input("Enter the dataset path: ")
    
    try:
        # Load the dataset
        dataset = pd.read_csv(dataset_path)
        
        # Extract features and labels
        X = dataset.iloc[:,2:4]
        y = dataset.iloc[:, 4]
        
        # Split the dataset into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
        
        # Standardize the features
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        
        # Fit a Gaussian Naive Bayes classifier
        clf1 = GaussianNB()
        clf1.fit(X_train, y_train)
        
        # Plot the decision boundary
        X_set, y_set = X_train, y_train
        X1, X2 = np.meshgrid(np.arange(start=X_set[:, 0].min() - 1, stop=X_set[:, 0].max() + 1, step=0.01),
                             np.arange(start=X_set[:, 1].min() - 1, stop=X_set[:, 1].max() + 1, step=0.01))
        plt.contourf(X1, X2, clf1.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                     alpha=0.75, cmap=ListedColormap(('red', 'green')))
        
        for i, j in enumerate(np.unique(y_set)):
            plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                        color=ListedColormap(('red', 'green'))(i), label=j)
        
        plt.xlim(X1.min(), X1.max())
        plt.ylim(X2.min(), X2.max())
        plt.title('Naive Bayes Classifier')
        plt.xlabel('Age')
        plt.ylabel('Estimated Salary')
        plt.legend()
        plt.show()
    
    except Exception as e:
        print("An error occurred:", str(e))

