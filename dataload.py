import os
import pandas as pd
import numpy as np

def find_csv():
    folder = os.path.dirname(os.path.abspath(__file__))
    for f in os.listdir(folder):
        if f.endswith('.csv'):
            return os.path.join(folder, f)
    return None

def load(filepath):
    print("loading data from:", filepath)
    df = pd.read_csv(filepath, index_col=0)
    names = list(df.index)
    dist = df.values.astype(float)
    print(f"  got {len(names)} cities")
    return dist, names, len(names), np.array(dist)
