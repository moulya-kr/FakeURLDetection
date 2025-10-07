import re
import pandas as pd

def extract_features(url):
    # Feature 1: Does URL use HTTPS?
    has_https = 1 if url.startswith("https") else 0

    # Feature 2: Count how many digits (0–9) are in the URL
    num_digits = len(re.findall(r'\d', url))

    # Feature 3: Count special characters like ?, =, -, _, @, etc.
    num_special = len(re.findall(r'[?=\-_@]', url))

    # Return DataFrame with the *same feature names as model training*
    features_df = pd.DataFrame([{
        'has_https': has_https,
        'num_digits': num_digits,
        'num_special': num_special
    }])

    return features_df
