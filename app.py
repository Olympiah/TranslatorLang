from flask import Flask, redirect, url_for, request, render_template, session
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])

def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    # Load the values from .env
    key = os.environ.get('KEY')
    # endpoint = os.environ['ENDPOINT']
    endpoint = os.environ.get('ENDPOINT')
    # location = os.environ['LOCATION']
    location = os.environ.get('LOCATION')

    # Indicate that we want to translate and the API version (3.0) and the target language
    #Creates the necessary path to call the Translator service, which includes the target language (the source language is automatically detected)
    path = '/translate?api-version=3.0'
    # Add the target language parameter
    target_language_parameter = '&to=' + target_language
    # Create the full URL
    constructed_url = str(endpoint) + str(path) + str(target_language_parameter)

    # Set up the header information, which includes our subscription key
    headers = {
        'Ocp-Apim-Subscription-Key': key, #key for the Translator service
        'Ocp-Apim-Subscription-Region': location, #the location of the service
        'Content-type': 'application/json', 
        'X-ClientTraceId': str(uuid.uuid4()) #arbitrary ID for the translation
    }

    # Create the body of the request with the text to be translated
    body = [{ 'text': original_text }]

    # Make the call using post
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Retrieve the JSON response
    translator_response = translator_request.json()
    # Retrieve the translation
    #Specifically, we need to read the first result, then to the collection of translations, 
    #the first translation, and then to the text. 
    #This is done by the call: translator_response[0]['translations'][0]['text']
    translated_text = translator_response[0]['translations'][0]['text']

    # Call render template, passing the translated text,
    # original text, and target language to the template
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )