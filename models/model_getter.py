from models.basic_bow_models import Direct_BOW_Model
from models.basic_bow_models import TfIdf_BOW_Model
from utils.model import load_model
from models.dataset import get_train_test_dataset, read_original_data
import pandas as pd

DATA_PATH = "./dataset/SMSSPAMCollection.txt";

cleaned_data = read_original_data(pd.read_csv(DATA_PATH,delimiter='\t',names=["class","text"]))

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

