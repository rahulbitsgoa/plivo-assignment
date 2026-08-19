# Plivo Forward Deployed Engineer (FDE) Technical Assignment

This repository contains a demo Interactive Voice Response (IVR) system built with Python, Flask, and the Plivo Voice API. It demonstrates outbound call initiation, OTP authentication with branching logic, and a multi-level IVR menu.

## Setup Instructions
1. **Prerequisites:** Ensure you have Python 3 and `pip` installed on your Ubuntu/Linux system.
2. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd plivo-fde
   ```
3. **Environment Setup:** Create and activate a Python virtual environment.
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. **Install Dependencies:** Install the Flask framework and the Plivo Python SDK.
   ```bash
   pip install Flask plivo
   ```
5. **Install Ngrok:** You will need Ngrok to securely expose your local Flask server to the internet so Plivo can communicate with your webhook endpoints.
   ```bash
   sudo snap install ngrok
   ```

## Required Plivo Credentials
As per the assignment requirements, the following credentials and numbers were provided to run this application:
*   **Auth ID:** `MAMTAWMGIOMZCTNTYZZS`
*   **Auth Token:** `M2Y2MzIIMWEtOGU5Ny00YzYxLWFkNzItZmE5ZmNI`
*   **Plivo Outbound Number:** `+918035454161`
*   **Live Associate Placeholder Number:** `02264236412`

*Note: The receiver's test phone number used for this demonstration is **+918210009277**.*

## Steps to Run and Test
1. **Update Configurations:** Open `app.py` and ensure the `MY_NUMBER` (set to `+918210009277`) and `MY_DOB` (set to `1911`) variables are configured correctly.
2. **Start Ngrok:** In a terminal, run `ngrok http 5000`. Copy the generated HTTPS Forwarding URL (e.g., `https://your-url.ngrok-free.dev`).
3. **Update Webhook URL:** Paste your new Ngrok URL into the `BASE_URL` variable in `app.py`.
4. **Start the Flask Server:** In a new terminal tab (with your virtual environment active), run the server:
   ```bash
   python app.py
   ```
5. **Trigger the Call:** Open a third terminal tab and send a GET request to the initiation endpoint to trigger the outbound call:
   ```bash
   curl http://localhost:5000/make_call
   ```
6. **Test Flow:** 
   * Answer the incoming call on speakerphone.
   * Enter an incorrect OTP to test the fallback/re-prompt logic.
   * Enter the correct OTP (`1911`) to successfully authenticate.
   * Navigate Level 1 by pressing `1` (English) or `2` (Spanish).
   * Navigate Level 2 by pressing `1` (Play Audio) or `2` (Forward to Live Associate).