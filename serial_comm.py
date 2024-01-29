import serial
import time

print("Importing serial comm")
try:
    arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)

except:
    print("Error connecting to sensor!")


time.sleep(2)
print("Connected to sensor ... ")

def sensorData():

    try:

        arduino.write(b'S')  # Send 'S' to request sensor value
        time.sleep(0.1)  # Allow time for Arduino to process and send the value

        data = arduino.readline().decode('utf-8').strip()
        if data:
            int_data = int(data)
            #print(f"Received Sensor Value: {int_data}")
            return int_data
    
    except:
        print("Some error occurred!")




