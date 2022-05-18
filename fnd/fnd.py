import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix


# Donald Trump says UFO is real
#input_data = [input()]
#vectorized_input_data = tfidf_vectorizer.transform(input_data)
#prediction = pac.predict(vectorized_input_data)
# print(prediction)
def createModel():
    # Read the data into a data frame
    data_frame = pd.read_csv('/home/arthur/diploma/news.csv')

    # Get the labels
    labels = data_frame.label

    # Split the dataset
    x_train, x_test, y_train, y_test = train_test_split(
        data_frame['text'], labels, test_size=0.3, random_state=7)

    # Initialize a TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)

    # Fit and transform train set, transform test set
    tfidf_train = tfidf_vectorizer.fit_transform(x_train)
    tfidf_test = tfidf_vectorizer.transform(x_test)

    # Initialize a PassiveAggressiveClassifier
    pac = PassiveAggressiveClassifier(max_iter=70)
    pac.fit(tfidf_train, y_train)

    # Predict on the test set and calculate accuracy
    y_pred = pac.predict(tfidf_test)
    score = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {round(score*100,2)}%')

    # Build confusion matrix
    print(confusion_matrix(y_test, y_pred, labels=['FAKE', 'REAL']))

    return (tfidf_vectorizer, pac)


def testModel(*newtext):
    tfidf_vectorizer, pac = createModel()
    vec_newtest = tfidf_vectorizer.transform(list(newtext))
    t_pred = pac.predict(vec_newtest)
    print(t_pred.shape)
    return t_pred


if __name__ == '__main__':
    user_input = input('"1" to create a model, "2" to test: ')
    if user_input == '1':
        createModel()
    elif user_input == '2':
        print(testModel(input('Text = ')))


# TODO: rewrite with OOP
