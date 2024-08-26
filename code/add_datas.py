from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)
json_file = 'datas.json'

# Ensure the JSON file exists
if not os.path.exists(json_file):
    with open(json_file, 'w') as file:
        json.dump([], file)

@app.route('/')
def index():
    form_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Add Data</title>
    </head>
    <body>
        <h1>Submit Data to be added to the JSON file</h1>
        <form action="/submit" method="POST">
        <label for="tag">Tag:</label>
        <input type="text" id="tag" name="tag" required><br><br>
        <label for="patterns">Patterns:</label>
        <input type="text" id="patterns" name="patterns" required><br><br>
        <label for="responses">Responses:</label>
        <input type="text" id="responses" name="responses" required><br><br>
        <input type="submit" value="Submit">
    </form>
    </body>
    </html>
    '''
    return render_template_string(form_html)

@app.route('/submit', methods=['POST'])
def submit_data():
    # Read form data
    tag = request.form['tag']
    patterns = request.form['patterns']
    responses = request.form['responses']
    
    # Create a dictionary to store the data
    new_data = {
        "tag": tag,
        "patterns": [patterns],
        "responses": [responses]
    }

    # Read the existing data from the JSON file
    with open(json_file, 'r') as file:
        datas = json.load(file)
        
    exists = False
    #If data with same tag exists already
    for data in datas['datas']:
        if data['tag'] == tag:
            data['patterns'].append(patterns)
            data['responses'].append(responses)
            exists = True
    if not exists:
        # Append the new data
        datas['datas'].append(new_data)

    # Write the updated data back to the JSON file
    with open(json_file, 'w') as file:
        json.dump(datas, file, indent=4)

    return jsonify({"message": "Data submitted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)