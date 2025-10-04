# Program to implement gesture recognition:
from flask import Flask, render_template,redirect,url_for
from flask_socketio import SocketIO
import time
import joblib
import serial
from captures_data import gestures_map,pulse_map
import pandas as pd

flag,arduino = None,None
gesture = ""

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def home():
    global gesture
    return render_template('index.html',gesture = gesture,len = len)

# Start Monitoring:
@app.route("/start")
def start_now():
    global flag,arduino
    flag = True
    # Arduino connectivity:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
    send_bpm_data()
    return redirect(url_for('home'))

# Stop Monitoring:
@app.route("/stop")
def stop_now():
    global flag,arduino
    arduino = None
    flag = False
    return redirect(url_for('home'))


#TODO: ML Part:

# Gesture Recognition:
def predict_gesture(val):
    model = joblib.load("model/gesture_prediction_new.pkl")
    data = {
        "X1":[val[0]],
        "X2":[val[1]],
        "X3":[val[2]],
        "X4":[val[3]],
    }
    predict_val = model.predict(pd.DataFrame(data))
    return gestures_map[predict_val[0]]

# Pulse Recognition:
def predict_pulse(bpm):
    pulse_model = joblib.load("model/pulse_rate_prediction.pkl")
    pulse = {
        "Pulse":[bpm]
    }
    pulse_frame = pd.DataFrame(pulse)
    predict = pulse_model.predict(pulse_frame)[0]
    return pulse_map[predict]

# BPM Data:
def send_bpm_data():
    global flag,arduino,gesture
    while flag:
        if arduino.in_waiting > 0:
            data = arduino.readline().decode('utf-8').strip()
            try:
                sensor_values = [int(val) for val in data.split(',')]
                print(f"Captured Values: {sensor_values[:4]}")
                print(f"BPM: {sensor_values[-1]}")
                print("Gesture: ", predict_gesture(sensor_values))
                gesture = predict_gesture(sensor_values)
                bpm = sensor_values[-1]
                bpm_state = predict_pulse(bpm)
                print("State: ",bpm_state)
                socketio.emit('gesture_data', gesture)
                socketio.emit('bpm_data', bpm)
                socketio.emit("state_data",bpm_state)
            except Exception as e:
                print(e)


@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    import threading
    threading.Thread(target=send_bpm_data).start()
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

