from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from preprocessing import clean_text
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score,f1_score
from xgboost import XGBClassifier

def convert_results_to_str(y_test,y_pred):
  return str(confusion_matrix(y_test, y_pred))+"\n\n accuracy: "+str(accuracy_score(y_test,y_pred)) \
    +"\n f1 score: " + str(f1_score(y_test,y_pred,average="weighted"))

class Direct_BOW_Model:  
  def __init__(self, model):
    self.models = {
        'SVC': LinearSVC(),
        'RF': RandomForestClassifier(),
        'MNB': MultinomialNB(),
        'NC' : NearestCentroid(),
        "XGB": XGBClassifier()       
    }
    self.model = self.models[model]
    self.bow_transformer = None
  def get_params(self,a,b):
    return self.model.get_params()

  def set_params_of_model(self,params):
    model = self.model
    model.set_params(**params)

  def fit(self, X_train, y_train):
    self.bow_transformer = CountVectorizer().fit(X_train)
    text_bow_train = self.bow_transformer.transform(X_train)
    self.model.fit(text_bow_train, y_train)

  def predict(self, text):
    return self.model.predict(self.bow_transformer.transform([clean_text(text, remove_whitespaces=False)]))[0]

  def evaluate(self, X_test, y_test):
    text_bow_X = self.bow_transformer.transform(X_test)
    y_pred = self.model.predict(text_bow_X)
    return convert_results_to_str(y_test,y_pred)

class TfIdf_BOW_Model:  
  def __init__(self, model):
    self.models = {
        'SVC': LinearSVC(),
        'RF': RandomForestClassifier(),
        'MNB': MultinomialNB(),
        'NC' : NearestCentroid(),
        "XGB": XGBClassifier()                
    }
    self.modelName = model
    self.model = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', self.models[model] ),
    ])

  def get_params(self,a,b):
    model = self.models[self.modelName]
    return model.get_params()

  def set_params_of_model(self,params):
    model = self.models[self.modelName]
    model.set_params(**params)
    self.model = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', model),
    ])

  def fit(self, X_train, y_train):
    self.model.fit(X_train, y_train)

  def predict(self, text):
    return self.model.predict([clean_text(text, remove_whitespaces=False)])[0]

  def evaluate(self, X_test, y_test):
    y_pred = self.model.predict(X_test)
    return convert_results_to_str(y_test,y_pred)