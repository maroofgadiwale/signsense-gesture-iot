import serial
import time
import pyttsx3
import pandas as pd
import csv

# Loading csv file:
df = pd.read_csv("gesture_loaded.csv")

engine = pyttsx3.init()
# Define the number of sensors and their corresponding pins
num_sensors = 4
flex_pins = ["A0","A1","A3","A4"]  # These are just labels for reference; actual pins are handled by Arduino

# Open serial connection to Arduino
arduino = serial.Serial('COM4', 9600, timeout=1)  # Replace 'COM4' with your Arduino's port
time.sleep(2)  # Give some time for the connection to establish

def main():
    i = 1
    while i<=30:
        if arduino.in_waiting > 0:
            # Read data from Arduino
            data = arduino.readline().decode('utf-8').strip()

            if not data:
                continue  # Ignore empty data

            print(f"Raw data: {data}")  # Debugging output

            try:
                # Convert the received string into a list of integers
                sensor_values = [int(val) for val in data.split(',')]

                # Ensure we received exactly 2 sensor values
                if len(sensor_values) != 5:
                    print("Invalid data format. Skipping...")
                    continue
                # sensor_values.append("I want water")
                with open("gesture_loaded.csv",mode = "a",newline = '') as file:
                    writer = csv.writer(file)
                    writer.writerow(sensor_values[:4] + ["I want to go to washroom"])

                print(f"Sensor values: {sensor_values}")  # Debugging output
                i += 1

            except ValueError as e:
                print(f"ValueError: {e}. Data: {data}")
            except Exception as e:
                print(f"Unexpected error: {e}")


        # Small delay to match the Arduino's loop delay
        time.sleep(1)

    print("complete")

if __name__ == "__main__":
    main()
