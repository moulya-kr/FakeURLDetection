import re
import pandas as pd

def extract_features(url):
    has_https = 1 if url.startswith("https") else 0
    num_digits = len(re.findall(r'\d', url))
    num_special = len(re.findall(r'[?=\-_@]', url))

    return pd.DataFrame([{
        "has_https": has_https,
        "num_digits": num_digits,
        "num_special": num_special
    }])