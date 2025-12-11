from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import numpy as np
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

base_path = os.path.dirname(os.path.abspath(__file__))

# Load Models
def load(name):
    try:
        with open(os.path.join(base_path, name), 'rb') as f: return pickle.load(f)
    except: return None

url_model = load('url_model.pkl')
email_model = load('email_model.pkl')
vectorizer = load('vectorizer.pkl')

print("✅ Server Online & Models Loaded.")

# --- SAFETY NETS ---
WHITELIST = [
    "google.com", "facebook.com", "amazon.com", "youtube.com", "wikipedia.org", 
    "twitter.com", "linkedin.com", "microsoft.com", "apple.com", "netflix.com",
    "github.com", "stackoverflow.com", "reddit.com", "zoom.us", "bing.com", "live.com"
]

PHISHING_TRIGGERS = [
    "verify your identity", "verify your account", "account suspended", 
    "unusual sign-in activity", "bank account locked", "update your payment",
    "password expiration", "unauthorized access", "confirm your details",
    "immediate action required", "your account will be closed", "pay now"
]

# --- FEATURE EXTRACTION ---
def get_url_features(url):
    url = str(url).lower()
    parsed = urlparse(url)
    return [
        len(url),
        parsed.netloc.count('.'),
        url.count('-'),
        1 if "@" in url else 0,
        1 if "https" not in url and "http" in url else 0,
        1 if any(c.isdigit() for c in parsed.netloc) else 0,
    ]

@app.route('/scan_url', methods=['POST'])
def scan_url():
    url = request.json.get('url', '').lower()
    domain = urlparse(url).netloc.replace("www.", "")
    
    # 1. Whitelist Check (Instant Safe)
    if any(w in domain for w in WHITELIST):
        return jsonify({"result": "SAFE", "confidence": "100% (Trusted)"})

    # 2. AI Check
    if not url_model: return jsonify({"result": "Error", "confidence": "0%"})
    
    features = np.array(get_url_features(url)).reshape(1, -1)
    prediction = url_model.predict(features)[0]
    
    # --- CALC CONFIDENCE ---
    try:
        probs = url_model.predict_proba(features)[0] # Returns [prob_safe, prob_phishing]
        score = max(probs) * 100
        confidence = f"{score:.1f}%"
    except:
        confidence = "N/A"

    return jsonify({
        "result": "PHISHING" if prediction == 1 else "SAFE", 
        "confidence": confidence
    })

@app.route('/scan_email', methods=['POST'])
def scan_email():
    if not email_model: return jsonify({"result": "Error", "confidence": "0%"})
    
    text = request.json.get('text', '')
    text_lower = text.lower()
    
    # 1. Trigger Check (Instant Phishing)
    trigger_score = 0
    for phrase in PHISHING_TRIGGERS:
        if phrase in text_lower: trigger_score += 1

    # 2. AI Check
    vec = vectorizer.transform([text])
    ai_prediction = email_model.predict(vec)[0]
    
    # --- CALC CONFIDENCE ---
    try:
        probs = email_model.predict_proba(vec)[0]
        score = max(probs) * 100
        confidence = f"{score:.1f}%"
    except:
        confidence = "N/A"
    
    # Decision Logic
    if trigger_score >= 1: 
        result = "PHISHING" 
        confidence = "100% (Keyword Detected)"
    elif ai_prediction == 1:
        result = "PHISHING"
    else:
        result = "SAFE"
        
    return jsonify({"result": result, "confidence": confidence})

if __name__ == '__main__':
    app.run(port=5000)