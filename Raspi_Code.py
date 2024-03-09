#!/usr/bin/env python3
import serial
import RPi.GPIO as GPIO
from time import sleep
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.130.3'  # Server's IP address. '' means bind to all interfaces.
port = 5003  # Port to listen on
server_socket.bind((host, port))
# Listen for incoming connections
server_socket.listen(1)
print(f"Listening on {port}...")

# Accept a connection
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} has been established.")
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(20, 50)
pwm1=GPIO.PWM(2, 50)
pwm2=GPIO.PWM(3, 50)
pwm1.start(0)
pwm.start(0)
pwm2.start(0)

def SetAng1(angle):
    duty = angle / 18 + 2
    GPIO.output(20, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(20, False)
    pwm.ChangeDutyCycle(0)

def SetAng2(angle):
    duty = angle / 18 + 2
    GPIO.output(2, True)
    pwm1.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(2, False)
    pwm1.ChangeDutyCycle(0)

def SetAng3(angle):
    duty = angle / 18 + 2
    GPIO.output(3, True)
    pwm2.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(3, False)
    pwm2.ChangeDutyCycle(0)


SetAng1(90)
SetAng2(0)
SetAng3(0)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
#SetAng3(60)
while True:
    line = ser.read()
    A = line.decode("utf-8")
    if A == '1':
        print(A)
        SetAng1(35)
        SetAng1(135)
        SetAng1(90)
        try:
            while True:
                # Receive data from the client
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break  # If no data is received, break the loop
                print(f"Received command: {data}")

                if "3" or "5" in data:
                    SetAng3(180)
                    SetAng2(30)
                    SetAng2(0)
                    
                else:
                    SetAng3(0)
                    SetAng2(30)
                    SetAng2(0)
        finally:
            # Close the connection
            client_socket.close()
            server_socket.close()
        
        

