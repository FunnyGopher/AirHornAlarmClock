from time import sleep
import serial

ser = serial.Serial('/dev/ttyAMA0', 9600)

try:
    while True:
        for i in range(181):
            ser.write(str(i))
            sleep(pause)
        for i in range(180, -1, -1):
            ser.write(str(i))
            sleep(pause)
            sleep(pause)

except KeyboardInterrupt:
    print('You stopped me!')
