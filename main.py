# Program to predict Gestures:
import pyttsx3
import serial
import time
from captures_data import gestures_map
import pandas as pd
import joblib

# TTS Speaker:
engine = pyttsx3.init()

# Arduino Connection:
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# Function to predict gesture
def predict_gesture(val):
    model = joblib.load("model/gesture_prediction_new.pkl")
    data = {
        "X1":[val[0]],
        "X2":[val[1]],
        "X3":[val[2]],
        "X4":[val[3]],
    }
    predict_val = model.predict(pd.DataFrame(data))
    engine.say(gestures_map[predict_val[0]])
    engine.runAndWait()
    return gestures_map[predict_val[0]]


while True:
    if arduino.in_waiting > 0:
        data = arduino.readline().decode('utf-8').strip()
        try:
            sensor_values = [int(val) for val in data.split(',')]
            print(f"Captured Values: {sensor_values[:4]}")
            print(f"BPM: {sensor_values[-1]}")
            print("Gesture: ",predict_gesture(sensor_values))
        except Exception as e:
            print(e)
    time.sleep(2)
