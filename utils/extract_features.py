import re
import pandas as pd

def extract_features(url):
    url_length = len(url)
    has_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0
    https_count = url.count("https")

    # Keep same order and names as during training
    features = pd.DataFrame([{
        "url_length": url_length,
        "has_ip": has_ip,
        "https_count": https_count
    }])
    return features
