
# Phishing Detector: AI-Powered Phishing Detection System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Backend-Flask-green)
![Chrome](https://img.shields.io/badge/Extension-Chrome-yellow)
![ML](https://img.shields.io/badge/AI-Scikit--Learn-orange)

**Phishing Detector** is a robust cybersecurity tool designed to protect users from online threats in real-time. It combines a **Google Chrome Extension** with a **Machine Learning Backend** to instantly analyze websites and emails for phishing indicators.

---

## 🚀 Features

* **🌐 Real-Time URL Scanning:** Instantly analyzes the website you are visiting to detect malicious domains.
* **📧 Email Content Analysis:** Uses Natural Language Processing (NLP) to detect phishing attempts in email text (e.g., "Verify your account" scams).
* **🧠 Hybrid Detection Engine:** Combines **Machine Learning** (Random Forest & Naive Bayes) with **Static Whitelisting** (Google, Amazon, etc.) for high accuracy.
* **⚡ Instant Feedback:** Provides a clear "SAFE" or "PHISHING" verdict with a confidence percentage.
* **🔒 Privacy Focused:** URLs and text are processed locally or via a private API; no data is stored.

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3, JavaScript (Chrome Extension Manifest V3)
* **Backend:** Python, Flask (REST API)
* **Machine Learning:** Scikit-Learn, Pandas, NumPy
    * *URL Model:* Random Forest Classifier
    * *Email Model:* Multinomial Naive Bayes (with TF-IDF)
* **Data Sources:** Kaggle Phishing URL Dataset & Phishing Email Corpus

---

## 📂 Project Structure

```text
Phishing Detector/
├── backend/
│   ├── app.py              # Flask API Server
│   ├── url_model.pkl       # Trained URL Model
│   ├── email_model.pkl     # Trained Email Model
│   └── vectorizer.pkl      # Text Vectorizer
├── extension/
│   ├── manifest.json       # Chrome Extension Config
│   ├── popup.html          # Extension UI
│   ├── popup.js            # Frontend Logic
│   └── style.css           # Styling
├── train_master.py         # ML Training Script
├── data.csv                # URL Dataset
├── real_emails.csv         # Email Dataset
└── README.md               # Documentation
