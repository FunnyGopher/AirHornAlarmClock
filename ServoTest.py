import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

green = GPIO.PWM(16, 100)
#red = GPIO.PWM(23, 100)

green.start(0)
#red.start(100)

sleep(2)

pause = 0.02

GPIO.output(23, GPIO.HIGH)

try:
    while True:
        for i in range(101):
            green.ChangeDutyCycle(i)
 #           red.ChangeDutyCycle(100 - i)
            sleep(pause)
        for i in range(100, -1, -1):
            green.ChangeDutyCycle(i)
  #          red.ChangeDutyCycle(100 - i)
            sleep(pause)

except KeyboardInterrupt:
    green.stop()
   # red.stop()
    GPIO.cleanup()
