# import os
# from flask import Flask, request, Response, jsonify
# import plivo

# app = Flask(__name__)

# # --- Config ---
# PLIVO_AUTH_ID = os.environ.get("PLIVO_AUTH_ID", "MAMTAWMGI0MZCTNTYZZS")
# PLIVO_AUTH_TOKEN = os.environ.get("PLIVO_AUTH_TOKEN", "MDRlZjgzMWMtNjFkYS00YmM1LThjYTMtZGRlZGRk")
# PLIVO_NUMBER = os.environ.get("PLIVO_NUMBER", "+918035454161")
# LIVE_ASSOCIATE_NUMBER = os.environ.get("LIVE_ASSOCIATE_NUMBER", "02264236412")

# MY_NUMBER = os.environ.get("MY_NUMBER", "+918210009277")
# MY_DOB = os.environ.get("MY_DOB", "1911")  # your OTP, DDMM format
# BASE_URL = os.environ.get("BASE_URL", "https://hungrily-essential-tucking.ngrok-free.dev")

# AUDIO_URL = os.environ.get("AUDIO_URL", "https://s3.amazonaws.com/plivocloud/music.mp3")

# client = plivo.RestClient(PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN)


# @app.route('/')
# def index():
#     return f'<a href="/make_call">Trigger call to {MY_NUMBER}</a>'


# @app.route('/make_call', methods=['GET'])
# def make_call():
#     try:
#         call = client.calls.create(
#             from_=PLIVO_NUMBER,
#             to_=MY_NUMBER,
#             answer_url=f"{BASE_URL}/otp_prompt",
#             answer_method="POST"
#         )
#         return jsonify({"status": "Call initiated", "request_uuid": call["request_uuid"]}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/otp_prompt', methods=['GET', 'POST'])
# def otp_prompt():
#     xmlr = f'''<Response>
#     <GetDigits action="{BASE_URL}/verify" method="POST" numDigits="4" timeout="15" retries="1">
#         <Speak>Welcome. Please enter your 4 digit OTP.</Speak>
#     </GetDigits>
#     <Speak>We did not receive any input. Goodbye.</Speak>
# </Response>'''
#     return Response(xmlr, mimetype='text/xml')


# @app.route('/verify', methods=['GET', 'POST'])
# def verify():
#     digits = request.form.get('Digits', '')

#     if digits == MY_DOB:
#         xmlr = f'''<Response>
#     <GetDigits action="{BASE_URL}/level2" method="POST" numDigits="1" timeout="15" retries="1">
#         <Speak>Success. For English, press 1. Para espanol, presione 2.</Speak>
#     </GetDigits>
#     <Speak>We did not receive any input. Goodbye.</Speak>
# </Response>'''
#         return Response(xmlr, mimetype='text/xml')

#     # wrong (or empty) OTP -> loop back to the prompt, indefinitely
#     xmlr = f'''<Response>
#     <Speak>Incorrect OTP.</Speak>
#     <Redirect method="POST">{BASE_URL}/otp_prompt</Redirect>
# </Response>'''
#     return Response(xmlr, mimetype='text/xml')


# @app.route('/level2', methods=['GET', 'POST'])
# def level2():
#     digits = request.form.get('Digits', '')

#     if digits == '1':
#         return Response(_level2_menu_xml("en"), mimetype='text/xml')
#     elif digits == '2':
#         return Response(_level2_menu_xml("es"), mimetype='text/xml')
#     else:
#         # invalid/no input -> repeat the language menu, don't guess
#         xmlr = f'''<Response>
#     <GetDigits action="{BASE_URL}/level2" method="POST" numDigits="1" timeout="15" retries="1">
#         <Speak>Invalid choice. For English, press 1. Para espanol, presione 2.</Speak>
#     </GetDigits>
#     <Speak>We did not receive any input. Goodbye.</Speak>
# </Response>'''
#         return Response(xmlr, mimetype='text/xml')


# def _level2_menu_xml(lang, invalid=False):
#     if lang == "es":
#         prompt = "Presione uno para escuchar un mensaje. Presione dos para hablar con un asociado."
#         speak_attr = ' language="es-ES"'
#     else:
#         prompt = "Press 1 to play a short audio message. Press 2 to connect to a live associate."
#         speak_attr = ""
#     prefix = "Invalid choice. " if invalid else ""
#     return f'''<Response>
#     <GetDigits action="{BASE_URL}/action?lang={lang}" method="POST" numDigits="1" timeout="15" retries="1">
#         <Speak{speak_attr}>{prefix}{prompt}</Speak>
#     </GetDigits>
#     <Speak>We did not receive any input. Goodbye.</Speak>
# </Response>'''


# @app.route('/action', methods=['GET', 'POST'])
# def action():
#     digits = request.form.get('Digits', '')
#     lang = request.args.get('lang', 'en')

#     if digits == '1':
#         return Response(f'<Response><Play>{AUDIO_URL}</Play></Response>', mimetype='text/xml')
#     elif digits == '2':
#         xmlr = f'''<Response>
#     <Speak>Connecting you to an associate.</Speak>
#     <Dial><Number>{LIVE_ASSOCIATE_NUMBER}</Number></Dial>
# </Response>'''
#         return Response(xmlr, mimetype='text/xml')
#     else:
#         # invalid/no input -> repeat this exact menu, in the right language
#         return Response(_level2_menu_xml(lang, invalid=True), mimetype='text/xml')


# if __name__ == '__main__':
#     app.run(port=5000, debug=True)
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


INDEX_HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>IVR Call Console</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #0e1116;
    --panel: #161b23;
    --panel-border: #262d38;
    --text: #e8e6df;
    --text-dim: #8b93a1;
    --amber: #f0a63d;
    --amber-dim: #7a5a26;
    --green: #4ade80;
    --red: #f0665f;
    --mono: 'JetBrains Mono', monospace;
    --display: 'Space Grotesk', sans-serif;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    min-height: 100vh;
    background: radial-gradient(circle at 20% 0%, #161b23 0%, var(--bg) 55%);
    color: var(--text);
    font-family: var(--mono);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }}
  .console {{
    width: 100%;
    max-width: 440px;
    background: var(--panel);
    border: 1px solid var(--panel-border);
    border-radius: 14px;
    padding: 28px 26px 24px;
    box-shadow: 0 30px 60px -20px rgba(0,0,0,0.6);
  }}
  .console-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 22px;
  }}
  .brand {{
    font-family: var(--display);
    font-weight: 600;
    font-size: 15px;
    letter-spacing: 0.02em;
    color: var(--text);
  }}
  .brand span {{ color: var(--amber); }}
  .line-status {{
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 11px;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }}
  .dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--amber);
    box-shadow: 0 0 0 0 rgba(240,166,61,0.6);
    animation: pulse 2s infinite;
  }}
  .dot.live {{ background: var(--green); box-shadow: 0 0 0 0 rgba(74,222,128,0.6); animation: pulse-green 1.2s infinite; }}
  @keyframes pulse {{
    0% {{ box-shadow: 0 0 0 0 rgba(240,166,61,0.5); }}
    70% {{ box-shadow: 0 0 0 8px rgba(240,166,61,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(240,166,61,0); }}
  }}
  @keyframes pulse-green {{
    0% {{ box-shadow: 0 0 0 0 rgba(74,222,128,0.6); }}
    70% {{ box-shadow: 0 0 0 8px rgba(74,222,128,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(74,222,128,0); }}
  }}
  label {{
    display: block;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-dim);
    margin-bottom: 8px;
  }}
  input[type=tel] {{
    width: 100%;
    background: #0e1116;
    border: 1px solid var(--panel-border);
    border-radius: 8px;
    padding: 12px 14px;
    font-family: var(--mono);
    font-size: 16px;
    color: var(--text);
    letter-spacing: 0.03em;
    outline: none;
    transition: border-color 0.15s;
  }}
  input[type=tel]:focus {{ border-color: var(--amber); }}
  .call-btn {{
    width: 100%;
    margin-top: 16px;
    padding: 13px;
    border-radius: 8px;
    border: none;
    background: var(--amber);
    color: #1a1300;
    font-family: var(--display);
    font-weight: 600;
    font-size: 14px;
    letter-spacing: 0.02em;
    cursor: pointer;
    transition: transform 0.1s, background 0.15s;
  }}
  .call-btn:hover {{ background: #f7b658; }}
  .call-btn:active {{ transform: scale(0.98); }}
  .call-btn:disabled {{ background: var(--amber-dim); cursor: not-allowed; }}
  .flow {{
    margin-top: 22px;
    padding-top: 18px;
    border-top: 1px solid var(--panel-border);
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  .flow-step {{
    display: flex;
    gap: 10px;
    font-size: 12px;
    color: var(--text-dim);
  }}
  .flow-step .n {{
    color: var(--amber);
    font-weight: 700;
    width: 14px;
  }}
  .log {{
    margin-top: 18px;
    font-size: 12px;
    color: var(--text-dim);
    min-height: 18px;
    line-height: 1.6;
    word-break: break-word;
  }}
  .log .ok {{ color: var(--green); }}
  .log .err {{ color: var(--red); }}
</style>
</head>
<body>
  <div class="console">
    <div class="console-top">
      <div class="brand">Inspire<span>Works</span> IVR</div>
      <div class="line-status"><span class="dot" id="dot"></span><span id="statusLabel">standby</span></div>
    </div>

    <label for="to_number">Destination number</label>
    <input type="tel" id="to_number" value="{MY_NUMBER}" placeholder="+91XXXXXXXXXX" />

    <button class="call-btn" id="callBtn" onclick="triggerCall()">Place call</button>

    <div class="flow">
      <div class="flow-step"><span class="n">1</span> Answer &amp; enter 4-digit OTP</div>
      <div class="flow-step"><span class="n">2</span> Choose language (English / Spanish)</div>
      <div class="flow-step"><span class="n">3</span> Play message or connect to associate</div>
    </div>

    <div class="log" id="log"></div>
  </div>

<script>
  async function triggerCall() {{
    const btn = document.getElementById('callBtn');
    const dot = document.getElementById('dot');
    const statusLabel = document.getElementById('statusLabel');
    const log = document.getElementById('log');
    const to_number = document.getElementById('to_number').value.trim();

    btn.disabled = true;
    btn.textContent = 'Dialing...';
    statusLabel.textContent = 'dialing';
    log.innerHTML = '';

    try {{
      const res = await fetch('/make_call', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ to_number }})
      }});
      const data = await res.json();
      if (res.ok) {{
        dot.classList.add('live');
        statusLabel.textContent = 'call placed';
        log.innerHTML = '<span class="ok">Call initiated</span> &mdash; UUID: ' + data.request_uuid;
      }} else {{
        statusLabel.textContent = 'error';
        log.innerHTML = '<span class="err">Error:</span> ' + data.error;
      }}
    }} catch (err) {{
      statusLabel.textContent = 'error';
      log.innerHTML = '<span class="err">Error:</span> ' + err.message;
    }} finally {{
      btn.disabled = false;
      btn.textContent = 'Place call';
    }}
  }}
</script>
</body>
</html>'''


@app.route('/')
def index():
    return Response(INDEX_HTML, mimetype='text/html')


@app.route('/make_call', methods=['GET', 'POST'])
def make_call():
    to_number = MY_NUMBER
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        to_number = data.get('to_number') or MY_NUMBER

    try:
        call = client.calls.create(
            from_=PLIVO_NUMBER,
            to_=to_number,
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