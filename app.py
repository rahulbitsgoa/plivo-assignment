import os
from flask import Flask, request, Response, jsonify
import plivo

app = Flask(__name__)

# --- Config ---
PLIVO_AUTH_ID = os.environ.get("PLIVO_AUTH_ID", "MAMTAWMGI0MZCTNTYZZS")
PLIVO_AUTH_TOKEN = os.environ.get("PLIVO_AUTH_TOKEN", "MDRlZjgzMWMtNjFkYS00YmM1LThjYTMtZGRlZGRk")
PLIVO_NUMBER = os.environ.get("PLIVO_NUMBER", "+918035454161")
LIVE_ASSOCIATE_NUMBER = os.environ.get("LIVE_ASSOCIATE_NUMBER", "02264236412")

MY_NUMBER = os.environ.get("MY_NUMBER", "+918210009277")
MY_DOB = os.environ.get("MY_DOB", "1911")  # your OTP, DDMM format
BASE_URL = os.environ.get("BASE_URL", "https://hungrily-essential-tucking.ngrok-free.dev")

AUDIO_URL = os.environ.get("AUDIO_URL", "https://s3.amazonaws.com/plivocloud/music.mp3")

client = plivo.RestClient(PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN)


@app.route('/')
def index():
    return f'<a href="/make_call">Trigger call to {MY_NUMBER}</a>'


@app.route('/make_call', methods=['GET'])
def make_call():
    try:
        call = client.calls.create(
            from_=PLIVO_NUMBER,
            to_=MY_NUMBER,
            answer_url=f"{BASE_URL}/otp_prompt",
            answer_method="POST"
        )
        return jsonify({"status": "Call initiated", "request_uuid": call["request_uuid"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/otp_prompt', methods=['GET', 'POST'])
def otp_prompt():
    xmlr = f'''<Response>
    <GetDigits action="{BASE_URL}/verify" method="POST" numDigits="4" timeout="15" retries="1">
        <Speak>Welcome. Please enter your 4 digit OTP.</Speak>
    </GetDigits>
    <Speak>We did not receive any input. Goodbye.</Speak>
</Response>'''
    return Response(xmlr, mimetype='text/xml')


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    digits = request.form.get('Digits', '')

    if digits == MY_DOB:
        xmlr = f'''<Response>
    <GetDigits action="{BASE_URL}/level2" method="POST" numDigits="1" timeout="15" retries="1">
        <Speak>Success. For English, press 1. Para espanol, presione 2.</Speak>
    </GetDigits>
    <Speak>We did not receive any input. Goodbye.</Speak>
</Response>'''
        return Response(xmlr, mimetype='text/xml')

    # wrong (or empty) OTP -> loop back to the prompt, indefinitely
    xmlr = f'''<Response>
    <Speak>Incorrect OTP.</Speak>
    <Redirect method="POST">{BASE_URL}/otp_prompt</Redirect>
</Response>'''
    return Response(xmlr, mimetype='text/xml')


@app.route('/level2', methods=['GET', 'POST'])
def level2():
    digits = request.form.get('Digits', '')

    if digits == '1':
        return Response(_level2_menu_xml("en"), mimetype='text/xml')
    elif digits == '2':
        return Response(_level2_menu_xml("es"), mimetype='text/xml')
    else:
        # invalid/no input -> repeat the language menu, don't guess
        xmlr = f'''<Response>
    <GetDigits action="{BASE_URL}/level2" method="POST" numDigits="1" timeout="15" retries="1">
        <Speak>Invalid choice. For English, press 1. Para espanol, presione 2.</Speak>
    </GetDigits>
    <Speak>We did not receive any input. Goodbye.</Speak>
</Response>'''
        return Response(xmlr, mimetype='text/xml')


def _level2_menu_xml(lang, invalid=False):
    if lang == "es":
        prompt = "Presione uno para escuchar un mensaje. Presione dos para hablar con un asociado."
        speak_attr = ' language="es-ES"'
    else:
        prompt = "Press 1 to play a short audio message. Press 2 to connect to a live associate."
        speak_attr = ""
    prefix = "Invalid choice. " if invalid else ""
    return f'''<Response>
    <GetDigits action="{BASE_URL}/action?lang={lang}" method="POST" numDigits="1" timeout="15" retries="1">
        <Speak{speak_attr}>{prefix}{prompt}</Speak>
    </GetDigits>
    <Speak>We did not receive any input. Goodbye.</Speak>
</Response>'''


@app.route('/action', methods=['GET', 'POST'])
def action():
    digits = request.form.get('Digits', '')
    lang = request.args.get('lang', 'en')

    if digits == '1':
        return Response(f'<Response><Play>{AUDIO_URL}</Play></Response>', mimetype='text/xml')
    elif digits == '2':
        xmlr = f'''<Response>
    <Speak>Connecting you to an associate.</Speak>
    <Dial><Number>{LIVE_ASSOCIATE_NUMBER}</Number></Dial>
</Response>'''
        return Response(xmlr, mimetype='text/xml')
    else:
        # invalid/no input -> repeat this exact menu, in the right language
        return Response(_level2_menu_xml(lang, invalid=True), mimetype='text/xml')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
