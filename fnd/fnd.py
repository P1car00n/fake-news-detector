import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix


class Detector:

    def __init__(
            self,
            data,
            test_size=0.25,
            train_size=0.75,
            column_title='text') -> None:
        # is there a better way to inspect these? maybe convert to propety at
        # least?
        self.test_size = test_size
        self.train_size = train_size
        # self.max_iter = max_iter # duplicating?
        #self.early_stopping = early_stopping

        self.data_frame = pd.read_csv(data)
        self.labels = self.data_frame.label
        x_train, x_test, self.y_train, self.y_test = train_test_split(
            self.data_frame[column_title], self.labels, test_size=self.test_size, train_size=self.train_size)
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_train = self.tfidf_vectorizer.fit_transform(x_train)
        self.tfidf_test = self.tfidf_vectorizer.transform(x_test)

    def predict(self, classifier, vectoriser, text):
        # using the same vectoriser?
        # list() divides sentences into letters, interesting
        vec_newtest = vectoriser.transform([text])
        t_pred = classifier.predict(vec_newtest)
        return t_pred


class PAClassifier(Detector):

    def __init__(
            self,
            data,
            test_size=0.25,
            train_size=0.75,
            max_iter=1000,
            early_stopping=False,
            column_title='text') -> None:
        Detector.__init__(
            self,
            data,
            test_size,
            train_size,
            column_title)  # meh

        self.classifier = 'Passive Aggressive Classifier'  # dirty

        self.max_iter = max_iter
        self.early_stopping = early_stopping

        self.pac = PassiveAggressiveClassifier(
            max_iter=self.max_iter,
            early_stopping=self.early_stopping)  # add max iter at a later point
        self.pac.fit(self.tfidf_train, self.y_train)
        self.y_pred = self.pac.predict(self.tfidf_test)
        # self.score wasn't visible until i added self tp y_pred, probably
        # bacause instances don't have access to variables created inside
        # functions
        self.score = accuracy_score(self.y_test, self.y_pred)
        # print(f'Accuracy: {round(score*100,2)}%')
        # print(confusion_matrix(y_test, y_pred, labels=['FAKE', 'REAL']))
        self.matrix = confusion_matrix(
            self.y_test, self.y_pred, labels=[
                'FAKE', 'REAL'])  # Make more user friendly?

    def predict(self, text):
        return Detector.predict(self, self.pac, self.tfidf_vectorizer, text)


class MultiNB(Detector):
    def __init__(
            self,
            data,
            test_size=0.25,
            train_size=0.75,
            column_title='text') -> None:
        Detector.__init__(
            self,
            data,
            test_size,
            train_size,
            column_title)  # meh
        self.classifier = 'Multinomial Naive Bayes'  # dirty

        # duplication of functionality: should rework
        self.mnb = MultinomialNB()
        self.mnb.fit(self.tfidf_train, self.y_train)
        self.y_pred = self.mnb.predict(self.tfidf_test)
        # duplicating
        self.score = accuracy_score(self.y_test, self.y_pred)
        # print(f'Accuracy: {round(score*100,2)}%')
        # print(confusion_matrix(y_test, y_pred, labels=['FAKE', 'REAL']))
        self.matrix = confusion_matrix(
            self.y_test, self.y_pred, labels=[
                'FAKE', 'REAL'])  # Make more user friendly?

    def predict(self, text):
        return Detector.predict(self, self.mnb, self.tfidf_vectorizer, text)


# Donald Trump says UFO is real
#input_data = [input()]
#vectorized_input_data = tfidf_vectorizer.transform(input_data)
#prediction = pac.predict(vectorized_input_data)
# print(prediction)
# def createModel():
#    # Read the data into a data frame
#    data_frame = pd.read_csv('/home/arthur/diploma/news.csv')
#
#    # Get the labels
#    labels = data_frame.label
#
#    # Split the dataset
#    x_train, x_test, y_train, y_test = train_test_split(
#        data_frame['text'], labels, test_size=0.3, random_state=7)
#
#    # Initialize a TfidfVectorizer
#    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
#
#    # Fit and transform train set, transform test set
#    tfidf_train = tfidf_vectorizer.fit_transform(x_train)
#    tfidf_test = tfidf_vectorizer.transform(x_test)
#
#    # Initialize a PassiveAggressiveClassifier
#    pac = PassiveAggressiveClassifier(max_iter=70)
#    pac.fit(tfidf_train, y_train)
#
#    # Predict on the test set and calculate accuracy
#    y_pred = pac.predict(tfidf_test)
#    score = accuracy_score(y_test, y_pred)
#    print(f'Accuracy: {round(score*100,2)}%')
#
#    # Build confusion matrix
#    print(confusion_matrix(y_test, y_pred, labels=['FAKE', 'REAL']))
#
#    return (tfidf_vectorizer, pac)
#
#
# def testModel(*newtext):
#    tfidf_vectorizer, pac = createModel()
#    vec_newtest = tfidf_vectorizer.transform(list(newtext))
#    t_pred = pac.predict(vec_newtest)
#    print(t_pred.shape)
#    return t_pred
#
#
# if __name__ == '__main__':
#    user_input = input('"1" to create a model, "2" to test: ')
#    if user_input == '1':
#        createModel()
#    elif user_input == '2':
#        print(testModel(input('Text = ')))
#
#
# TODO: rewrite with OOP; add naive baes option?
# Notes: cx_freeze was pita to install, whereas pyinstaller was pita to use. Cxfreeze didn't work
