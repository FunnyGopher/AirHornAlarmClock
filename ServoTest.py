# Servo test code. Used this to determine if our servo worked.

from time import sleep
import serial

ser = serial.Serial('/dev/ttyACM1', 9600)
pause = .01

while 1:
    x = int(input("Enter a char: "))
    ser.write(bytes(str(x), "UTF-8"))
    print(ser.readline())
    sleep(pause)
    
