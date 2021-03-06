# $Id: TODO $
# Author: Arthur Zevaloff <no@mail.gov>
# Copyright: Apache-2.0

"""Text classification

This module is intended to be used for classifying text as either
fake news or not and defines the following classes:

- `Detector`, a classifier superclass
- `LinearDetector`, a linear classifer superclass
- `BayesDetector`, a bayes classifer superclass
- `PAClassifier`, a linear passive aggressive classifier
- `Percept`, a linear perceptron classifier
- `MultiNB`, a multinomial naive bayes classifier
- `ComplNB`, a complement naive bayes classifier

"""

__docformat__ = 'restructuredtext'

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier, Perceptron
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.metrics import accuracy_score, confusion_matrix


class Detector:
    def __init__(
            self, classifier,
            data='',
            test_size=0.25,
            train_size=0.75,
            column_title='text',
            data_frame=None) -> None:
        # is there a better way to inspect these? maybe convert to propety at
        # least?
        self.test_size = test_size
        self.train_size = train_size

        self.classifier = classifier

        if data == '':
            self.data_frame = data_frame
        else:
            self.data_frame = pd.read_csv(data, encoding='utf-8')

        self.labels = self.data_frame.label
        x_train, x_test, self.y_train, self.y_test = train_test_split(
            self.data_frame[column_title], self.labels, test_size=self.test_size, train_size=self.train_size)
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_train = self.tfidf_vectorizer.fit_transform(x_train)
        self.tfidf_test = self.tfidf_vectorizer.transform(x_test)

        self.classifier.fit(self.tfidf_train, self.y_train)
        self.y_pred = self.classifier.predict(self.tfidf_test)
        self.score = accuracy_score(self.y_test, self.y_pred)
        self.matrix = confusion_matrix(
            self.y_test, self.y_pred, labels=[
                'FAKE', 'REAL'])  # Make more user friendly?

    def predict(self, text):
        # using the same vectoriser?
        # list() divides sentences into letters, interesting
        vec_newtest = self.tfidf_vectorizer.transform([text])
        t_pred = self.classifier.predict(vec_newtest)
        return t_pred

    def __getattr__(self, attr):  # fix for Pickle
        """Return None for all unknown attributes and raise an exception for all unknown dunder-attributes"""
        if attr.startswith('__') and attr.endswith('__'):
            raise AttributeError
        return None


class LinearDetector(Detector):
    def __init__(
            self, classifier,
            data='',
            test_size=0.25,
            train_size=0.75,
            max_iter=1000,
            early_stopping=False,
            column_title='text',
            data_frame=None) -> None:

        self.max_iter = max_iter
        self.early_stopping = early_stopping

        Detector.__init__(
            self, classifier(
                max_iter=self.max_iter,
                early_stopping=self.early_stopping),
            data,
            test_size,
            train_size,
            column_title,
            data_frame)


class PAClassifier(LinearDetector):

    def __init__(
            self,
            data='',
            test_size=0.25,
            train_size=0.75,
            max_iter=1000,
            early_stopping=False,
            column_title='text',
            data_frame=None) -> None:

        LinearDetector.__init__(
            self, PassiveAggressiveClassifier,
            data,
            test_size,
            train_size,
            max_iter,
            early_stopping,
            column_title,
            data_frame)

    def __str__(self) -> str:
        return 'Passive Aggressive Classifier'


class Percept(LinearDetector):
    def __init__(
            self,
            data='',
            test_size=0.25,
            train_size=0.75,
            max_iter=1000,
            early_stopping=False,
            column_title='text',
            data_frame=None) -> None:

        LinearDetector.__init__(
            self, Perceptron,
            data,
            test_size,
            train_size,
            max_iter,
            early_stopping,
            column_title,
            data_frame)

    def __str__(self) -> str:
        return 'Perceptron'


class BayesDetector(Detector):
    def __init__(
            self, classifier,
            data='',
            test_size=0.25,
            train_size=0.75,
            column_title='text',
            data_frame=None) -> None:

        Detector.__init__(
            self, classifier(),
            data,
            test_size,
            train_size,
            column_title,
            data_frame)


class MultiNB(BayesDetector):
    def __init__(
            self,
            data='',
            test_size=0.25,
            train_size=0.75,
            column_title='text', data_frame=None, **kwargs) -> None:

        BayesDetector.__init__(
            self, MultinomialNB,
            data,
            test_size,
            train_size,
            column_title,
            data_frame)

    def __str__(self) -> str:
        return 'Multinomial Naive Bayes'


class ComplNB(BayesDetector):
    def __init__(
            self,
            data='',
            test_size=0.25,
            train_size=0.75,
            column_title='text', data_frame=None, **kwargs) -> None:

        BayesDetector.__init__(
            self, ComplementNB,
            data,
            test_size,
            train_size,
            column_title,
            data_frame)

    def __str__(self) -> str:
        return 'Complement Naive Bayes'
