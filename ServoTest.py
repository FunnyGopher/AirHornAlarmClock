from time import sleep
import serial

ser = serial.Serial('/dev/ttyACM1', 9600)
pause = .01
'''
try:
    ser.write(b'0')
    
    while True:
        #for i in range(181):
            #string = str(i)
        print("Left")
        ser.write(b'0')
        sleep(pause)
        #for i in range(180, -1, -1):
            #string = str(i)
        print("Right")
        ser.write(b'180')
        sleep(pause)
        
except KeyboardInterrupt:
    ('You stopped me!')
    '''

while 1:
    x = int(input("Enter a char: "))
    ser.write(bytes(str(x), "UTF-8"))
    print(ser.readline())
    sleep(pause)
    
