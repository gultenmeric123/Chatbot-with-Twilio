from flask import Flask, request
import os
import dialogflow
from google.api_core.exceptions import InvalidArgument
from twilio.twiml.messaging_response import MessagingResponse
import requests

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "private_key.json"

DIALOGFLOW_PROJECT_ID = "ordersummary-ccot"
DIALOGFLOW_LANGUAGE_CODE = "tr"
SESSION_ID = "me"

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/sms')
def root():
  return "wp bot"

@app.route('/api/getMessage', methods=['POST'])
def home():
    message = request.form.get('Body')
    mobnum = request.form.get('From')
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    text_input = dialogflow.types.TextInput(text=message, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    print("query text", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    print("Fulfillment text", response.query_result.fulfillment_text)

   
    sendMessage(mobnum, response.query_result.fulfillment_text)

    return response.query_result.fulfillment_text
if __name__ == "__main__":
    app.run()

