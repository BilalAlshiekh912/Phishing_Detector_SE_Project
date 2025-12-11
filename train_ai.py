import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from urllib.parse import urlparse

# Setup Paths
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
os.makedirs(backend_path, exist_ok=True)

print("--- STARTING MASTER TRAINING ---")


#  URL MODEL 

print("\nTraining URL Detector...")
url_file = 'data.csv'

if os.path.exists(url_file):
    # Load Data
    df_url = pd.read_csv(url_file, on_bad_lines='skip')
    
    # Auto-detect columns
    cols = [c.lower() for c in df_url.columns]
    url_col = df_url.columns[cols.index('url')] if 'url' in cols else df_url.columns[0]
    lbl_col = df_url.columns[cols.index('label')] if 'label' in cols else df_url.columns[1]

    # Map Labels (Force 0=Safe, 1=Phishing)
    def map_url(val):
        val = str(val).lower()
        if val in ['good', 'benign', 'safe', '0']: return 0
        return 1

    df_url['binary_label'] = df_url[lbl_col].apply(map_url)

    # BALANCE DATA (15k Safe / 15k Phishing)
    bad_urls = df_url[df_url['binary_label'] == 1]
    good_urls = df_url[df_url['binary_label'] == 0]
    
    min_len = min(len(bad_urls), len(good_urls), 15000)
    
    df_balanced = pd.concat([
        bad_urls.sample(n=min_len, random_state=42),
        good_urls.sample(n=min_len, random_state=42)
    ])
    
    print(f"   > Training on {len(df_balanced)} URLs (Balanced).")

    # FEATURE EXTRACTION (The Set that works best)
    def get_url_features(url):
        url = str(url).lower()
        parsed = urlparse(url)
        return [
            len(url),                                     # 1. Length
            parsed.netloc.count('.'),                     # 2. Dot count
            url.count('-'),                               # 3. Hyphen count
            1 if "@" in url else 0,                       # 4. Obfuscation
            1 if "https" not in url and "http" in url else 0, # 5. Insecure
            1 if any(c.isdigit() for c in parsed.netloc) else 0, # 6. IP/Digits
        ]

    df_balanced['features'] = df_balanced[url_col].apply(get_url_features)
    
    # Train Random Forest
    clf_url = RandomForestClassifier(n_estimators=60, random_state=42)
    clf_url.fit(list(df_balanced['features']), df_balanced['binary_label'])

    with open(os.path.join(backend_path, 'url_model.pkl'), 'wb') as f:
        pickle.dump(clf_url, f)
    print(" URL Model Saved.")

else:
    print(" Error: 'data.csv' missing.")


#EMAIL MODEL (Real Emails + N-Grams)

print("\nTraining Email Detector...")
email_file = 'real_emails.csv' # Expecting the "Phishing Email" dataset

if os.path.exists(email_file):
    try:
        df = pd.read_csv(email_file, on_bad_lines='skip')
        
        # Auto-detect Columns
        cols = [c.lower() for c in df.columns]
        
        if 'email text' in cols: text_col = df.columns[cols.index('email text')]
        elif 'text' in cols: text_col = df.columns[cols.index('text')]
        else: text_col = df.columns[0]

        if 'email type' in cols: label_col = df.columns[cols.index('email type')]
        elif 'label' in cols: label_col = df.columns[cols.index('label')]
        else: label_col = df.columns[-1]

        # Map Labels
        def map_label(val):
            val = str(val).lower()
            if 'phishing' in val: return 1
            return 0 # Safe

        df['binary_label'] = df[label_col].apply(map_label)
        df[text_col] = df[text_col].astype(str).fillna("")

        # Balance Data
        phishing = df[df['binary_label'] == 1]
        safe = df[df['binary_label'] == 0]
        
        min_len = min(len(phishing), len(safe), 8000)
        df_balanced = pd.concat([phishing.sample(min_len), safe.sample(min_len)])
        
        print(f"   > Training on {len(df_balanced)} real emails (Balanced).")

        # VECTORIZATION (TF-IDF + Bigrams)
        # Learns shady phrases like "account suspended"
        tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=10000)
        features = tfidf.fit_transform(df_balanced[text_col])

        # Train Naive Bayes
        clf_email = MultinomialNB()
        clf_email.fit(features, df_balanced['binary_label'])

        with open(os.path.join(backend_path, 'email_model.pkl'), 'wb') as f:
            pickle.dump(clf_email, f)
        with open(os.path.join(backend_path, 'vectorizer.pkl'), 'wb') as f:
            pickle.dump(tfidf, f)
            
        print("Email Model Saved.")

    except Exception as e:
        print(f"Error: {e}")
else:
    print(" Error: 'real_emails.csv' not found.")