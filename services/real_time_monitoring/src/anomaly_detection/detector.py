import numpy as np

def is_anomalous(heart_rate_data):
    # Example threshold-based anomaly detection
    if heart_rate_data > 100 or heart_rate_data < 60:
        return True
    return False