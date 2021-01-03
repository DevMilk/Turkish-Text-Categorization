from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn import tree
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import StackingClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from models.preprocessing import clean_text
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
class Direct_BOW_Model:  
  def __init__(self, model):
    self.models = {
        'SVC': LinearSVC(),
        'RF': RandomForestClassifier(),
        'MNB': MultinomialNB()       
    }
    self.model = self.models[model]
    self.bow_transformer = None

  def fit(self, X_train, y_train):
    self.bow_transformer = CountVectorizer().fit(X_train)
    text_bow_train = self.bow_transformer.transform(X_train)
    self.model.fit(text_bow_train, y_train)

  def predict(self, text):
    return self.model.predict(self.bow_transformer.transform([clean_text(text, remove_whitespaces=False)]))[0]

  def evaluate(self, X_test, y_test):
    text_bow_X = self.bow_transformer.transform(X_test)
    y_pred = self.model.predict(text_bow_X)
    return str(confusion_matrix(y_test, y_pred))+"\n\n"+str(accuracy_score(y_test,y_pred))

class TfIdf_BOW_Model:  
  def __init__(self, model):
    self.models = {
        'SVC': LinearSVC(),
        'RF': RandomForestClassifier(),
        'MNB': MultinomialNB()       
    }
    self.model = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', self.models[model] ),
    ])

  def fit(self, X_train, y_train):
    self.model.fit(X_train, y_train)

  def predict(self, text):
    return self.model.predict([clean_text(text, remove_whitespaces=False)])[0]

  def evaluate(self, X_test, y_test):
    y_pred = self.model.predict(X_test)
    return str(confusion_matrix(y_test, y_pred))+"\n\n"+str(accuracy_score(y_test,y_pred))