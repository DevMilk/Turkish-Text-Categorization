from preprocessing import clean_text
from sklearn.model_selection import train_test_split


def read_original_data(data):
    cleaned_data = data.copy()
    cleaned_data["text"] = data["text"].apply(lambda x: clean_text(x, remove_whitespaces=False))
    return cleaned_data

def get_train_test_dataset(cleaned_data,test_ratio=0.2):
    return train_test_split(cleaned_data["text"],cleaned_data["class"],test_size=test_ratio)