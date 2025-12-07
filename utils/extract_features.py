import re
import pandas as pd

def extract_features(url):
    has_https = 1 if url.startswith("https") else 0
    num_digits = sum(c.isdigit() for c in url)
    num_special = len(re.findall(r'[?=&%\-_/]', url))
    length = len(url)
    has_ip = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0
    count_dots = url.count(".")

    features_df = pd.DataFrame([{
        'has_https': has_https,
        'num_digits': num_digits,
        'num_special': num_special,
        'length': length,
        'has_ip': has_ip,
        'count_dots': count_dots
    }])

    return features_df
