from flask import Flask, request
from google.api_core.exceptions import InvalidArgument
from twilio.twiml.messaging_response import MessagingResponse
import requests
from google.cloud import dialogflow
import base64
import os
import logging

# Loglama konfigürasyonu
logging.basicConfig(level=logging.DEBUG)
credentials = f'AC1109ce3b41919916492b23eb5004cc7c:2ZA5E83bdwAJ9W5pXxZ9qDVCmmt_6L7a3SxpEarXLKTum4uoz'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/meric/OneDrive/Belgeler/pythonders/app.py/private_key.json'
credentials_base64 = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

DIALOGFLOW_PROJECT_ID = 'ordersummary-ccot'
DIALOGFLOW_LANGUAGE_CODE = 'tr'
SESSION_ID = 'me'
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/status_callback', methods=['GET'])
@app.route('/')
def root():
    return 'WhatsApp Chatbot'

@app.route('/api/getMessage', methods=['POST'])
def home():
    message = request.form.get('Body')
    mobnum = request.form.get('From')

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.TextInput(text=message, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)
    
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    
    print('Query text:', response.query_result.query_text)
    print('Detected intent:', response.query_result.intent.display_name)
    print('Detected intent confidence:', response.query_result.intent_detection_confidence)
    print('Fulfillment text:', response.query_result.fulfillment_text)
    sendMessage(mobnum, response.query_result.fulfillment_text)

    return response.query_result.fulfillment_text

def sendMessage(mobnum, message):
    print('Mobile number : ', mobnum)
    url = 'https://api.twilio.com/2010-04-01/Accounts/AC1109ce3b41919916492b23eb5004cc7c/Messages.json'
    payload = {'From': 'whatsapp:+14155238886', 'Body': message, 'To': mobnum}
    headers = {'Authorization': 'Basic ' + base64.b64encode(f'AC1109ce3b41919916492b23eb5004cc7c:332d9fa5da4f64217eefc692f9db15ab'.encode('utf-8')).decode('utf-8')}
    response = requests.post(url, headers=headers, json=payload)
    
    print('Response Status Code:', response.status_code)
    print('Response Content:', response.text)

if __name__ == '_main_':
    app.run()