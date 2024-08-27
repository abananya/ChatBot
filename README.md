**Python Chatbot**

This is a simple chatbot created using Python that runs on customized data from the user.

The different steps are:
1. Storing data in a JSON file in the format of {tag, patterns, responses} that corresponds to questions and answers. For this created a simple webpage where users can enter
   the data using an HTML form and used Flask to fetch the data and store it in the JSON file.
2. After the intial cleaning and lemmatizing, data is stored in pickle files - words.pickle and classes.pickle
3. Used the Sequential model from keras and created 2 hidden layers and an output layer.
4. Created a Flask backend that returns chatbot response as a json object.
