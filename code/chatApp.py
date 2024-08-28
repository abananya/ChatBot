import nltk
nltk.download("punkt")
nltk.download("wordnet")
nltk.download('punkt_tab')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import json
import pickle
import numpy as np
import random


from tensorflow.keras.models import load_model
model = load_model('chatbot_model.h5')
datas = json.loads(open('datas.json', encoding="utf8").read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

def clean_sentence(message):
    #tokenize pattern 
    sentence = nltk.word_tokenize(message)
    sentence = [lemmatizer.lemmatize(word.lower()) for word in sentence]
    return sentence

def bag_of_words(message, words, show_details=True):
    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
    sentence = clean_sentence(message)
    
    bag = [0] * len(words)
    for word_in_sentence in sentence:
        for idx, word in enumerate(words):
            if word == word_in_sentence:
                # assign 1 if current word is present
                bag[idx] = 1
                if show_details:
                    print ("found in bag: %s" % word)
            
    return(np.array(bag))

def predict_class(message, model):
    # filter out predictions below a threshold
    bag = bag_of_words(message, words, show_details=False)
    print("bag", bag)
    response = model.predict(np.array([bag]))[0]
    print("response", response)
    ERROR_THRESHOLD = 0.25
    
    results = [[idx, res] for idx, res in enumerate(response) if res > ERROR_THRESHOLD]
    print("results", results)
    # sort by probability
    results.sort(key=lambda x: x[1], reverse=True)
    
    res = []
    for idx, result in results:
        res.append(classes[idx])
    print("res:", res)
    return res


def chatbot_response(message):
    print("classes", classes)
    print("words", words)
    print("model", model)
    class_name = predict_class(message, model)
    response = get_response(class_name, datas)
    return response
    
def get_response(class_name, datas):
    tag = class_name[0]
    list_of_intents = datas['datas']
    
    for intent in list_of_intents:
        if(intent['tag']== tag):
            res = random.choice(intent['responses'])
            break
        
    return res


''' Flask '''
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/", methods=['GET'])
def check():
    return jsonify({"health":"Server is running successfully!"})

def replace_seperator(message):
     #replaces + with space
     new_message = message.replace("+", " ")
     
     return new_message

@app.route("/query/<sentence>")
def query_chatbot(sentence):
    message = replace_seperator(sentence)
    response = chatbot_response(message)
    
    json_obj = jsonify({"reply" : {"response": response}})
    return json_obj

if __name__ == '__main__':
    app.run(debug=True , threaded = False)
