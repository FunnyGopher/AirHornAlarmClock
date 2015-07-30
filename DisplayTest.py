import RPi.GPIO as GPIO
from time import sleep

data = 21
latch = 16
clock = 12

numbers = {
    '0' : '12579adf',
    '1' : '31f',
    '2' : '521089ad',
    '3' : '5210fda',
    '4' : '7801f',
    '5' : '25780fda',
    '6' : '780fda9',
    '7' : '523c',
    '8' : '752180fda9',
    '9' : '521087f'
}

letters = {
    'A' : '13b0f',
    'B' : '52140fcda',
    'C' : '2579ad',
    'D' : '5241cfda',
    'E' : '257809ad',
    'F' : '25789',
    'G' : '2579adf0',
    'H' : '78901f',
    'I' : '524cad',
    'J' : '9adf1',
    'K' : '7893e',
    'L' : '79ad',
    'M' : '97631f',
    'N' : '976ef1',
    'O' : '12579adf',
    'P' : '5217809',
    'Q' : '52719adfe',
    'R' : '5217809e',
    'S' : '2560fda',
    'T' : '524c',
    'U' : '79adf1',
    'V' : '79b3',
    'W' : '79bef1',
    'X' : 'b63e',
    'Y' : '63c',
    'Z' : '253bad',
    'a' : '89acd',
    'b' : '78eda9',
    'c' : '980ad',
    'd' : '10badf',
    'e' : '89ba',
    'f' : '5789',
    'g' : '25601fda',
    'h' : '7809f',
    'i' : 'c',
    'j' : '1fda',
    'k' : '43ce',
    'l' : '4c',
    'm' : '98c0f',
    'n' : '98e',
    'o' : '980fda',
    'p' : '975238',
    'q' : '5784cd',
    'r' : '98',
    's' : '0ed',
    't' : '789ad',
    'u' : '9adf',
    'v' : '9b',
    'w' : '9bef',
    'x' : 'b63e',
    'y' : '401fd',
    'z' : '8ba'
}

def segmentreader(segmentstream):
    value = 0
    for i in segmentstream:
        power = int(i, 16)
        value += pow(2, power)
    return value

def write(on, flipped=True):
    if(flipped):
        on = not on
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

def writestream(streamofbits, numbofbits, flipped=True):
    if(len(streamofbits) < numbofbits):
        dif = numbofbits - len(streamofbits)
        for i in range(dif):
            streamofbits = '0' + streamofbits
            
    for bit in streamofbits:
        write(int(bit))
    out()

def writebitnumber(number, numbofbits):
    writestream(bin(number)[2:], numbofbits)


def clear():
    writestream('0', 16)

try:
    setup()
    clear()
    ###############
    for i in 'Brandon':
        writebitnumber(segmentreader(letters[i]), 16)
        sleep(.8)
    sleep(1)
    ###############
    clear()
    GPIO.cleanup()
except KeyboardInterrupt:
        print("Closing the program")
        clear()
        GPIO.cleanup()

