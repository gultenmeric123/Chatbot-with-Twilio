from flask import Flask, request
from google.api_core.exceptions import InvalidArgument
from twilio.twiml.messaging_response import MessagingResponse
from google.cloud import dialogflow
from twilio.rest import Client
import base64
import os

app = Flask(__name__)
app.config['DEBUG'] = True

# Dialogflow konfigürasyonları
DIALOGFLOW_PROJECT_ID = 'ordersummary-ccot'
DIALOGFLOW_LANGUAGE_CODE = 'tr'
SESSION_ID = 'me'

# Twilio konfigürasyonları
account_sid = 'AC1109ce3b41919916492b23eb5004cc7c'
auth_token = '332d9fa5da4f64217eefc692f9db15ab'
twilio_client = Client(account_sid, auth_token)

# Dialogflow API'ye bağlanmak için gerekli olan base64 kodunu oluşturun
credentials = f'AC1109ce3b41919916492b23eb5004cc7c:2ZA5E83bdwAJ9W5pXxZ9qDVCmmt_6L7a3SxpEarXLKTum4uoz'
credentials_base64 = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

# Flask uygulaması için /status_callback ve / endpoint'leri
@app.route('/status_callback', methods=['GET'])
@app.route('/', methods=['GET'])
def root():
    return 'WhatsApp Chatbot'

# WhatsApp mesajları için endpoint
@app.route('/api/getMessage', methods=['POST'])
def home():
    
    # Gelen isteği JSON formatına çevir
    data = request.get_json()

    # Gelen JSON içinden message değerini al
    message = data.get('Body', '')
    
    # Dialogflow'a göndermek üzere mesajı işle
    fulfillment_text = process_message(message)

    # WhatsApp'a cevap gönder
    send_whatsapp_message(fulfillment_text)

    # Cevap olarak fulfillment_text'i döndür
    return fulfillment_text


def process_message(message):
    # Dialogflow ile iletişim kurmak için bir session oluştur
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    # Dialogflow'a göndermek üzere bir TextInput nesnesi oluştur
    text_input = dialogflow.TextInput(text=message, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        # Dialogflow'a isteği gönder
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    # Dialogflow'dan gelen yanıtın metinini al ve döndür
    return response.query_result.fulfillment_text

def send_whatsapp_message(message):
    # Twilio kullanarak WhatsApp mesajı gönder
    twilio_client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to='whatsapp:+905317368966'
    )

if __name__ == '__main__':
    app.run()

