import pickle

def load_model(mainModel, subModel):
  pickle_filename = "./models/saved_models/"+mainModel+ '/' + subModel+".pkl"
  picklefile = open(pickle_filename, 'rb')
  model = pickle.load(picklefile)
  picklefile.close()
  return model