from flask import Flask, jsonify, redirect, request
from flask import render_template
import os
import pandas as pd
from models.preprocessing import clean_text
from models.model_getter import *


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

app = Flask(__name__)


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


#Modele tahmin yaptırır

@app.route('/predict', methods= ["POST"])
def predict():
    parameters = request.get_json()
    text = parameters.get("text")
    args = parameters.get("args")

    return jsonify(runMethodOfModel("predict",args,[text]))

#Verisetini böler
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

#Mevcut modeli eğitir ve train accuracy'sini döndürür

@app.route('/train', methods= ["POST"])
def train(): 
    try:
        parameters = request.get_json()
        args = parameters.get("args")
        params = parameters.get("params") #dictionary olmalı
        runMethodOfModel("set_params_of_model",args,[(params)])
        runMethodOfModel("fit",args,(X_train,y_train))
        return jsonify(["Training Success"])
    except Exception as e:
        print(e)
        return jsonify(["ERROR ON TRAINING"])




#Mevcut modeli test eder ve test accuracy'sini döndürür

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
    pass