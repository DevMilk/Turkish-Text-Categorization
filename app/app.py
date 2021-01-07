# Preprocessing
import re
import nltk

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from text_preprocessing import preprocess_text, remove_stopword
from text_preprocessing import to_lower, remove_email, remove_url, lemmatize_word, remove_punctuation, check_spelling, \
    expand_contraction, remove_name, remove_number, remove_special_character, remove_punctuation, remove_whitespace, \
    normalize_unicode, remove_stopword, preprocess_text

# A list of contractions from http://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in
# -python
contractions = {
    "ain't"      : "am not",
    "aren't"     : "are not",
    "can't"      : "cannot",
    "can't've"   : "cannot have",
    "'cause"     : "because",
    "could've"   : "could have",
    "couldn't"   : "could not",
    "couldn't've": "could not have",
    "didn't"     : "did not",
    "doesn't"    : "does not",
    "don't"      : "do not",
    "hadn't"     : "had not",
    "hadn't've"  : "had not have",
    "hasn't"     : "has not",
    "haven't"    : "have not",
    "he'd"       : "he would",
    "he'd've"    : "he would have",
    "he'll"      : "he will",
    "he's"       : "he is",
    "how'd"      : "how did",
    "how'll"     : "how will",
    "how's"      : "how is",
    "i'd"        : "i would",
    "i'll"       : "i will",
    "i'm"        : "i am",
    "i've"       : "i have",
    "isn't"      : "is not",
    "it'd"       : "it would",
    "it'll"      : "it will",
    "it's"       : "it is",
    "let's"      : "let us",
    "ma'am"      : "madam",
    "mayn't"     : "may not",
    "might've"   : "might have",
    "mightn't"   : "might not",
    "must've"    : "must have",
    "mustn't"    : "must not",
    "needn't"    : "need not",
    "oughtn't"   : "ought not",
    "shan't"     : "shall not",
    "sha'n't"    : "shall not",
    "she'd"      : "she would",
    "she'll"     : "she will",
    "she's"      : "she is",
    "should've"  : "should have",
    "shouldn't"  : "should not",
    "that'd"     : "that would",
    "that's"     : "that is",
    "there'd"    : "there had",
    "there's"    : "there is",
    "they'd"     : "they would",
    "they'll"    : "they will",
    "they're"    : "they are",
    "they've"    : "they have",
    "wasn't"     : "was not",
    "we'd"       : "we would",
    "we'll"      : "we will",
    "we're"      : "we are",
    "we've"      : "we have",
    "weren't"    : "were not",
    "what'll"    : "what will",
    "what're"    : "what are",
    "what's"     : "what is",
    "what've"    : "what have",
    "where'd"    : "where did",
    "where's"    : "where is",
    "who'll"     : "who will",
    "who's"      : "who is",
    "won't"      : "will not",
    "wouldn't"   : "would not",
    "you'd"      : "you would",
    "you'll"     : "you will",
    "you're"     : "you are"
}


def clean_text(text, remove_stopwords=True, remove_whitespaces=False):
    preprocess_functions = [to_lower, remove_email, remove_url, remove_punctuation, lemmatize_word, check_spelling,
                            expand_contraction, remove_name, remove_stopword]
    # text = preprocess_text(text, preprocess_functions)

    # Convert words to lower case
    # text = text.lower()

    # Replace contractions with their longer forms
    if True:
        text = text.split()
        new_text = []
        for word in text:
            if word in contractions:
                new_text.append(contractions[word])
            else:
                new_text.append(word)
        text = " ".join(new_text)

    # Format words and remove unwanted characters
    text = re.sub(r'&amp;', '', text)
    text = re.sub(r'0,0', '00', text)
    text = re.sub(r'[_"\-;%()|.,+&=*%.,!?:#@\[\]]', ' ', text)
    text = re.sub(r'\'', ' ', text)
    text = re.sub(r'\$', ' $ ', text)
    text = re.sub(r'j k ', ' jk ', text)
    text = re.sub(r' s ', ' ', text)
    text = re.sub(r' yr ', ' year ', text)
    text = re.sub(r' l g b t ', ' lgbt ', text)
    if remove_whitespaces:
        text = re.sub(r' ', '', text)

    # Optionally, remove stop words
    if remove_stopwords:
        text = text.split()
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops]
        text = " ".join(text)
    return text


# Basic Bow Models
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
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

# Dataset

from sklearn.model_selection import train_test_split


def read_original_data(data):
    cleaned_data = data.copy()
    cleaned_data["text"] = data["text"].apply(lambda x: clean_text(x, remove_whitespaces=False))
    return cleaned_data

def get_train_test_dataset(cleaned_data,test_ratio=0.2):
    return train_test_split(cleaned_data["text"],cleaned_data["class"],test_size=test_ratio)

# Model Getter
import pandas as pd

DATA_PATH = "dataset/7allV03.csv";
cleaned_data = read_original_data(pd.read_csv(DATA_PATH,names=["class","text"],skiprows=[0]))
X_train, X_test, y_train, y_test = get_train_test_dataset(cleaned_data)
# NGRAM MODELS
def getModel(model,init_arg,fit_args):
    model_object = model(init_arg)
    model_object.fit(*fit_args)
    print('{} was installed successfully!'.format(model))
    return model_object

def getBasicBow(ml):
    return getModel(Direct_BOW_Model,ml,(X_train,y_train))

# TF-IDF BOW MODELS
def getTfidfBow(ml):
    return getModel(TfIdf_BOW_Model,ml,(X_train,y_train))

# App.py

from flask import Flask, jsonify, request
from flask import render_template


Model_dict = {
    "BASIC-BOW": {
        "RF": getBasicBow("RF"),
        "MNB": getBasicBow("MNB"),
        "SVC": getBasicBow("SVC"),
        "NC": getBasicBow("NC"),
        "XGB": getBasicBow("XGB")
    },
    "TF-IDF-BOW": {
        "RF": getTfidfBow("RF"),
        "MNB": getTfidfBow("MNB"),
        "SVC": getTfidfBow("SVC"),
        "NC": getTfidfBow("NC"),
        "XGB": getTfidfBow("XGB")
    },
}

app = Flask(__name__, template_folder='templates')


def getModelFromDict(args):
    return Model_dict[args[-1]][args[-2]]

def most_frequent(List): 
    counter = 0
    num = List[0] 
      
    for i in List: 
        curr_frequency = List.count(i) 
        if(curr_frequency> counter): 
            counter = curr_frequency 
            num = i 
  
    return num 


def runMethodOfModel(methodName, args,material):
    results = []
    if(args[-1]=="ALL"):
        for key in list(Model_dict.keys()):
            for ml_model in list(Model_dict[key].keys()):
                results.append(getattr(Model_dict[key][ml_model], methodName)(*material))
        results = [most_frequent(results)]
    else:
        model =  getModelFromDict(args)
        results.append(getattr(model,methodName)(*material))

    return results

@app.route('/')
def hello():
    return render_template("index.html");


#Make the model predict

@app.route('/predict', methods= ["POST"])
def predict():
    parameters = request.get_json()
    text = parameters.get("text")
    args = parameters.get("args")

    return jsonify(runMethodOfModel("predict",args,[text]))

#Verisetini boler
@app.route("/split",methods = ["POST"])
def change_split():
    global X_train,y_train,X_test,y_test
    try:
        parameters = request.get_json()
        test_ratio = parameters.get("test_ratio")
        X_train, X_test, y_train, y_test = get_train_test_dataset(cleaned_data,test_ratio)
        return jsonify(["Data Splitted with {} test data ratio".format(test_ratio)])
    except Exception as e:
        print(e)
        return jsonify(["Error on splitting dataset"])

#Train the current model and return train accuracy

@app.route('/train', methods= ["POST"])
def train(): 
    try:
        parameters = request.get_json()
        args = parameters.get("args")
        params = parameters.get("params") #must be a dict
        runMethodOfModel("set_params_of_model",args,[(params)])
        runMethodOfModel("fit",args,(X_train,y_train))
        return jsonify(["Training Success"])
    except Exception as e:
        print(e)
        return jsonify(["ERROR ON TRAINING"])

#Test the current model and return test accuracy

@app.route('/test', methods= ["POST"])
def test(): 
    parameters = request.get_json()
    args = parameters.get("args")
    return jsonify(runMethodOfModel("evaluate", args, (X_test,y_test)))


@app.route('/param', methods= ["POST"])
def get_param(): 
    parameters = request.get_json()
    args = parameters.get("args")
    return jsonify(runMethodOfModel("get_params", args,(0,0)))


if __name__ == '__main__':
  app.run()