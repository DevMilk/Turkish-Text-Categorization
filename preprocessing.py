import re
import nltk

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from text_preprocessing import preprocess_text, remove_stopword
from text_preprocessing import to_lower, remove_email, remove_url, lemmatize_word, remove_punctuation, check_spelling, expand_contraction, remove_name, remove_number, remove_special_character, remove_punctuation, remove_whitespace, normalize_unicode, remove_stopword, preprocess_text

# A list of contractions from http://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
contractions = { 
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he's": "he is",
"how'd": "how did",
"how'll": "how will",
"how's": "how is",
"i'd": "i would",
"i'll": "i will",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'll": "it will",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"must've": "must have",
"mustn't": "must not",
"needn't": "need not",
"oughtn't": "ought not",
"shan't": "shall not",
"sha'n't": "shall not",
"she'd": "she would",
"she'll": "she will",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"that'd": "that would",
"that's": "that is",
"there'd": "there had",
"there's": "there is",
"they'd": "they would",
"they'll": "they will",
"they're": "they are",
"they've": "they have",
"wasn't": "was not",
"we'd": "we would",
"we'll": "we will",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"where'd": "where did",
"where's": "where is",
"who'll": "who will",
"who's": "who is",
"won't": "will not",
"wouldn't": "would not",
"you'd": "you would",
"you'll": "you will",
"you're": "you are"
}


def clean_text(text, remove_stopwords=True, remove_whitespaces=False):
  preprocess_functions = [to_lower, remove_email, remove_url, remove_punctuation, lemmatize_word, check_spelling, expand_contraction, remove_name, remove_stopword]
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