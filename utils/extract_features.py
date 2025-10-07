import re
import pandas as pd

def extract_features(url):
    features = {}
    features['url_length'] = len(url)
    features['num_digits'] = len(re.findall(r'\d', url))
    features['num_special'] = len(re.findall(r'\W', url))
    features['has_https'] = 1 if "https" in url else 0
    return pd.DataFrame([features])