from flask import Flask, request, Response
import plivo

app = Flask(__name__)
# Credentials provided in the assignment
client = plivo.RestClient("MAMTAWMGI0MZCTNTYZZS", "M2Y2Mz11MWEt0GU5Ny00YzYxLWFkNzItZmE5ZmNI")

MY_NUMBER = "+918210009277" # UPDATE THIS: Replace with your mobile number (e.g., +919876543210)
MY_DOB = "1911"             # UPDATE THIS: Replace with your birthdate in DDMM format
BASE_URL = "https://hungrily-essential-tucking.ngrok-free.dev" # Pre-filled from your ngrok terminal

@app.route('/make_call', methods=['GET'])
def make_call():
    client.calls.create(
        from_="+918035454161",
        to_=MY_NUMBER,
        answer_url=f"{BASE_URL}/otp_prompt",
        answer_method="POST"
    )
    return "Call initiated", 200

@app.route('/otp_prompt', methods=['POST'])
def otp_prompt():
    xml = f'<Response><GetDigits action="{BASE_URL}/verify" method="POST" numDigits="4"><Speak>Enter your 4 digit O T P.</Speak></GetDigits></Response>'
    return Response(xml, mimetype='text/xml')

@app.route('/verify', methods=['POST'])
def verify():
    if request.form.get('Digits') == MY_DOB:
        xml = f'<Response><GetDigits action="{BASE_URL}/level2" method="POST" numDigits="1"><Speak>Success. Press 1 for English, 2 for Spanish.</Speak></GetDigits></Response>'
        return Response(xml, mimetype='text/xml')
    xml = f'<Response><Speak>Incorrect O T P.</Speak><Redirect method="POST">{BASE_URL}/otp_prompt</Redirect></Response>'
    return Response(xml, mimetype='text/xml')

@app.route('/level2', methods=['POST'])
def level2():
    lang = "Press 1 to play audio. Press 2 for an associate." if request.form.get('Digits') == '1' else "Presione uno para audio, dos para un representante."
    xml = f'<Response><GetDigits action="{BASE_URL}/action" method="POST" numDigits="1"><Speak>{lang}</Speak></GetDigits></Response>'
    return Response(xml, mimetype='text/xml')

@app.route('/action', methods=['POST'])
def action():
    if request.form.get('Digits') == '1':
        return Response('<Response><Play>https://s3.amazonaws.com/plivocloud/music.mp3</Play></Response>', mimetype='text/xml')
    return Response('<Response><Speak>Connecting.</Speak><Dial><Number>02264236412</Number></Dial></Response>', mimetype='text/xml')

if __name__ == '__main__':
    app.run(port=5000)
