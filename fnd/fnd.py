import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier, Perceptron
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.metrics import accuracy_score, confusion_matrix


class Detector:

    def __init__(
            self,
            data, classifier,
            test_size=0.25,
            train_size=0.75,
            column_title='text') -> None:
        # is there a better way to inspect these? maybe convert to propety at
        # least?
        self.test_size = test_size
        self.train_size = train_size

        self.classifier = classifier

        self.data_frame = pd.read_csv(data)
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
            self,
            data, classifier,
            test_size=0.25,
            train_size=0.75,
            max_iter=1000,
            early_stopping=False,
            column_title='text') -> None:

        self.max_iter = max_iter
        self.early_stopping = early_stopping

        Detector.__init__(
            self,
            data,
            classifier(
                max_iter=self.max_iter,
                early_stopping=self.early_stopping),
            test_size,
            train_size,
            column_title)


class PAClassifier(LinearDetector):

    def __init__(
            self,
            data,
            test_size=0.25,
            train_size=0.75,
            max_iter=1000,
            early_stopping=False,
            column_title='text') -> None:

        LinearDetector.__init__(
            self,
            data, PassiveAggressiveClassifier,
            test_size,
            train_size,
            max_iter,
            early_stopping,
            column_title)

    def __str__(self) -> str:
        return 'Passive Aggressive Classifier'


class Percept(LinearDetector):
    def __init__(
            self,
            data,
            test_size=0.25,
            train_size=0.75,
            max_iter=1000,
            early_stopping=False,
            column_title='text') -> None:

        LinearDetector.__init__(
            self,
            data, Perceptron,
            test_size,
            train_size,
            max_iter,
            early_stopping,
            column_title)

    def __str__(self) -> str:
        return 'Perceptron'


class BayesDetector(Detector):
    def __init__(
            self,
            data, classifier,
            test_size=0.25,
            train_size=0.75,
            column_title='text') -> None:

        Detector.__init__(
            self,
            data,
            classifier(),
            test_size,
            train_size,
            column_title)


class MultiNB(BayesDetector):
    def __init__(
            self,
            data,
            test_size=0.25,
            train_size=0.75,
            column_title='text', **kwargs) -> None:

        BayesDetector.__init__(
            self,
            data, MultinomialNB,
            test_size,
            train_size,
            column_title)

    def __str__(self) -> str:
        return 'Multinomial Naive Bayes'


class ComplNB():
    def __init__(
            self,
            data,
            test_size=0.25,
            train_size=0.75,
            column_title='text', **kwargs) -> None:

        BayesDetector.__init__(
            self,
            data, ComplementNB,
            test_size,
            train_size,
            column_title)

    def __str__(self) -> str:
        return 'Complement Naive Bayes'
