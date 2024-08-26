**Python Chatbot**
This is a simple chatbot created using Python that runs on customized data from the user.

STEPS:
1. Storing data in a JSON file in the format of {tag, patterns, responses} that corresponds to questions and answers. For this created a simple webpage where users can enter
   the data using an HTML form and used Flask to fetch the data and store it in the JSON file.
2. After the intial cleaning and lemmatizing the data is stored in pickle files - words.pickle and classes.pickle
3. Used the Sequential model from keras to create 2 hidden layers and an output layer.
