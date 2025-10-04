# Pulse Recognition:
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib

df_pulse = pd.read_csv("pulse_data.csv")
df_pulse.head()

X = df_pulse[["Pulse"]]
y = df_pulse[["State_Label"]]

pulse_knn = KNeighborsClassifier(n_neighbors = 3)
pulse_knn.fit(X,y)

if joblib.dump(pulse_knn, "model/pulse_rate_prediction.pkl"):
    print("Model Saved!")