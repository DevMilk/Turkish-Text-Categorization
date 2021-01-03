from flask import Flask, jsonify, redirect, request
from flask import render_template
from models.wrapper import StyleBased
import os
from enum import Enum
import pickle
import pandas as pd
from flasgger import Swagger

from models.model_getter import *


Model_dict = {
    "NGRAM": {
        "WRD": getNgram(WordLevelTextgram),
        "CHR": getNgram(CharLevelTextNgram),
        "POS": getNgram(WordLevelPOSNgram),
        "DEFAULT": "POS"
    },
    "BASIC-BOW": {
        "RF": getBasicBow("RF"),
        "MNB": getBasicBow("MNB"),
        "SVC": getBasicBow("SVC"),
        "DEFAULT": "SVC"
    },
    "TF-IDF-BOW": {
        "RF": getTfidfBow("RF"),
        "MNB": getTfidfBow("MNB"),
        "SVC": getTfidfBow("SVC"),
        "DEFAULT": "SVC"
    },
    "STYLE-BASED": {
        "RF": StyleBased("RF"),
        "LR": StyleBased("LR"),
        "DEFAULT": "RF"
    }
}

# Model_dict = {
#     "NGRAM": {
#         "WRD": get_ngram_wrd(),
#         "CHR": get_ngram_chr(),
#         # "POS": get_ngram_pos()
#     },
#     "BASIC-BOW": {
#         "RF": None,
#         "MNB": None,
#         "SVC": None
#     },
#     "TF-IDF-BOW": {
#         "RF": None,
#         "MNB": None,
#         "SVC": None
#     },
#     "STYLE-BASED": {
#         "RF": None,
#         "SVC": None
#     }
# }



# def load_model(mainModel, subModel):
#   pickle_filename = "./models/saved_models/"+mainModel+ '/' + subModel+".pkl"
#   picklefile = open(pickle_filename, 'rb')
#   model = pickle.load(picklefile)
#   picklefile.close()
#   return model


# def load_models():
#     models = []
#     try:
#         for mainModel in list(Model_dict.keys()):
#             if mainModel == 'NGRAM': continue
#             for subModel in list(Model_dict[mainModel].keys()):
#                 model= mainModel + '/' + subModel
#                 try:
#                     Model_dict[mainModel][subModel] = load_model(mainModel, subModel)
#                     print(model + 'was installed successfully!')
#                 except Exception as e:
#                     print('An error has occurred while installing ' + model)
#                     print(e)
                
#     except Exception as e: 
#         print(e)
#     return models


def load_dataset():
    col_list = ["author","text"]
    return pd.read_csv("dataset/train.csv",usecols=col_list),pd.read_csv("dataset/test.csv",usecols=col_list)

# load_models()

train_data, test_data = load_dataset()

app = Flask(__name__)
swagger = Swagger(app)


def getModelFromDict(args):
    print(args[-1],args[-2])
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
            results.append(getattr(Model_dict[key][Model_dict[key]["DEFAULT"]], methodName)(material))
        results = [most_frequent(results)]
    else:
        model =  getModelFromDict(args)
        results.append(getattr(model,methodName)(material))

    return results

@app.route('/')
def hello():
    return render_template("index.html");


#Modele tahmin yaptırır

@app.route('/predict', methods= ["POST"])
def predict():
    parameters = request.get_json()
    text = parameters.get("text")
    args = parameters.get("args")

    return jsonify(runMethodOfModel("predict",args,text))



#Mevcut modeli eğitir ve train accuracy'sini döndürür

@app.route('/train', methods= ["POST"])
def train(): 
    parameters = request.get_json()
    args = parameters.get("args")
    return jsonify(runMethodOfModel("fit",args,test_data))



#Mevcut modeli test eder ve test accuracy'sini döndürür

@app.route('/test', methods= ["POST"])
def test(): 
    parameters = request.get_json()
    args = parameters.get("args")
    return jsonify(runMethodOfModel("evaluate", args, train_data))


if __name__ == '__main__':
    pass