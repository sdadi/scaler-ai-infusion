import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor

np.random.seed(42)
n = 5000

df = pd.DataFrame({
    "distance_km":np.random.uniform(0.5, 12, n),
    "prepa_time_min":np.random.uniform(5, 30, n),
    "rider_available":np.random.randint(0, 2, n),
    "is_raining":np.random.randint(0, 2, n),
})