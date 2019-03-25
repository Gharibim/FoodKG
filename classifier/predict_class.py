from keras.models import load_model
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pickle
import pandas as pd


model = load_model('../models/my_model.h5')
encoder = LabelEncoder()
text_labels = np.load('../models/classes.npy')

teste = "class not found exception found"


handle = open('../models/tokenizer.pickle', 'rb')
tokenize = pickle.load(handle)


x_test = tokenize.texts_to_matrix(pd.Series(teste))
prediction = model.predict(np.array(x_test))
predicted_label = text_labels[np.argmax(prediction)]
print("Predicted label: " + predicted_label + "\n")


