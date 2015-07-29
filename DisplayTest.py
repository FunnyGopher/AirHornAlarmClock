import RPi.GPIO as GPIO
from time import sleep   

data = 21
latch = 16
clock = 12
    
def write(on):
    GPIO.output(data, on)
    GPIO.output(clock, GPIO.HIGH)
    GPIO.output(clock, GPIO.LOW)
    GPIO.output(data, GPIO.LOW)

def writeout(on):
    write(on)
    out()

def out():
    GPIO.output(latch, GPIO.HIGH)
    sleep(.1)
    GPIO.output(latch, GPIO.LOW)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(data, GPIO.OUT)
    GPIO.setup(latch, GPIO.OUT)
    GPIO.setup(clock, GPIO.OUT)

    GPIO.output(latch, GPIO.LOW)
    GPIO.output(data, GPIO.LOW)
    GPIO.output(clock, GPIO.LOW)

def writeoutstream(streamofbits):
    for bit in streamofbits:
        writeout(int(bit))

def writestream(streamofbits):
    if(len(streamofbits) < 8):
        dif = 8 - len(streamofbits)
        eightZeros = '00000000'[:dif - 1]
        streamofbits = eightZeros + streamofbits
    for bit in streamofbits:
        write(int(bit))
    out()

def write8bitnumber(number):
    writestream(bin(number)[2:])

def clear():
    writestream('00000000')

try:
    setup()
    clear()
    #for i in range(256):
        #write8bitnumber(i)
        #sleep(.01)
    #sleep(1)
    GPIO.cleanup()
except KeyboardInterrupt:
        print("losing the program")
        clear()
        GPIO.cleanup()

