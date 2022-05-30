import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import MultinomialNB
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
        # self.max_iter = max_iter # duplicating?
        #self.early_stopping = early_stopping

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

    def predict(self, classifier, vectoriser, text):
        # using the same vectoriser?
        # list() divides sentences into letters, interesting
        vec_newtest = vectoriser.transform([text])
        t_pred = classifier.predict(vec_newtest)
        return t_pred

    def __getattr__(self, attr):  # fix for Pickle
        """Return None for all unknown attributes and raise an exception for all unknown dunder-attributes"""
        if attr.startswith('__') and attr.endswith('__'):
            raise AttributeError
        return None


class PAClassifier(Detector):

    def __init__(
            self,
            data,
            test_size=0.25,
            train_size=0.75,
            max_iter=1000,
            early_stopping=False,
            column_title='text') -> None:

        self.max_iter = max_iter
        self.early_stopping = early_stopping

        self.pac = PassiveAggressiveClassifier(
            max_iter=self.max_iter,
            early_stopping=self.early_stopping)  # add max iter at a later point

        Detector.__init__(
            self,
            data, self.pac,
            test_size,
            train_size,
            column_title)  # meh

    def predict(self, text):
        return Detector.predict(self, self.pac, self.tfidf_vectorizer, text)


class MultiNB(Detector):
    def __init__(
            self,
            data,
            test_size=0.25,
            train_size=0.75,
            column_title='text', **kwargs) -> None:

        # didn't find a better way rather than putting these additional arguments in each class. think of solutions
        #self.max_iter = max_iter
        #self.early_stopping = early_stopping

        self.mnb = MultinomialNB()

        Detector.__init__(
            self,
            data, self.mnb,
            test_size,
            train_size,
            column_title)  # meh

    def predict(self, text):
        return Detector.predict(self, self.mnb, self.tfidf_vectorizer, text)
