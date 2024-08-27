#importing dependencies

import nltk
nltk.download("punkt")
nltk.download("wordnet")
nltk.download('punkt_tab')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
import random

words = []
classes = []
documents = []
ignore_words = ["?", "!"]

#importing the json file
data_file = open('datas.json', encoding="utf-8").read()
datas = json.loads(data_file)
#populating the lists initialized earlier

for data in datas['datas']:
    for pattern in data['patterns']:
        #tokenizing each word
        word = nltk.word_tokenize(pattern)
        words.extend(word)
        
        #adding documents
        documents.append((word, data['tag']))
        
        #adding classes
        if data['tag'] not in classes:
            classes.append(data['tag'])

words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

#initializing the training data
training = []
output = [0] * len(classes)

for document in documents:
    #initializing the bag of words
    bag_of_words = []
    pattern_words = document[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    
    for word in words:
        if word in pattern_words:
            bag_of_words.append(1) 
        else:
            bag_of_words.append(0)
            
    output[classes.index(document[1])] = 1
    
    training.append([bag_of_words, output])
        
random.shuffle(training)
training = np.array(training, dtype="object")

print(words)

train_x = list(training[:, 0])
train_y = list(training[:, 1])


model = Sequential()
model.add(Dense(128, input_shape = (len(train_x[0]), ), activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),  activation = 'softmax'))

sgd = SGD(learning_rate = 0.0001, momentum = 0.9, nesterov = True)
model.compile(loss = 'categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs = 200, batch_size = 5, verbose = 1)
model.save('chatbot_model.h5', hist)



        
        