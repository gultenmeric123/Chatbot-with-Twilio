from twilio.rest import Client 
sid='AC1109ce3b41919916492b23eb5004cc7c'
authToken='332d9fa5da4f64217eefc692f9db15ab'

client=Client(sid , authToken)
message=client.messages.create(to='whatsapp:+905317368966', from_='whatsapp:+14155238886',body='Selam ben Gülten.' )