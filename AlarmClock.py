import RPi.GPIO as GPIO
from time import sleep
import datetime


class ClockDisplay:
    def __init__(self, shift_register, numb_of_displays):
        self.shift_register = shift_register
        self.numb_of_displays = numb_of_displays

        self.chars = {
            'A': '13b0f',
            'B': '52140fcda',
            'C': '2579ad',
            'D': '5241cfda',
            'E': '257809ad',
            'F': '25789',
            'G': '2579adf0',
            'H': '78901f',
            'I': '524cad',
            'J': '9adf1',
            'K': '7893e',
            'L': '79ad',
            'M': '97631f',
            'N': '976ef1',
            'O': '12579adf',
            'P': '5217809',
            'Q': '52719adfe',
            'R': '5217809e',
            'S': '2560fda',
            'T': '524c',
            'U': '79adf1',
            'V': '79b3',
            'W': '79bef1',
            'X': 'b63e',
            'Y': '63c',
            'Z': '253bad',
            'a': '89acd',
            'b': '78eda9',
            'c': '980ad',
            'd': '10badf',
            'e': '89ba',
            'f': '5789',
            'g': '25601fda',
            'h': '7809f',
            'i': 'c',
            'j': '1fda',
            'k': '43ce',
            'l': '4c',
            'm': '98c0f',
            'n': '98e',
            'o': '980fda',
            'p': '975238',
            'q': '5784cd',
            'r': '98',
            's': '0ed',
            't': '789ad',
            'u': '9adf',
            'v': '9b',
            'w': '9bef',
            'x': 'b63e',
            'y': '401fd',
            'z': '8ba',
            '0': '12579adf',
            '1': '31f',
            '2': '521089ad',
            '3': '5210fda',
            '4': '7801f',
            '5': '25780fda',
            '6': '780fda9',
            '7': '523c',
            '8': '752180fda9',
            '9': '521087f',
            ' ': '0'
        }

    def charToSegment(self, char):
        value = 0
        for i in char: #52140fcda
            power = int(i, 16)
            value += pow(2, power)
        return value

    def clear(self):
        self.shift_register.writestream((0 for x in range(80)), self.shift_register.bits)

    def write(self, text): #0130
        bin_output = ""
        for i in text:
            hexcode = self.chars[i]
            dec = self.charToSegment(hexcode)
            bincode = bin(dec)[2:]
            bincode.zfill(16)

            '''
            if len(bincode) < 16:
                dif = 16 - len(bincode)
                for i in range(dif):
                    bincode = '0' + bincode
            '''

            bin_output += bincode

        self.shift_register.writestream(bin_output)



class Button:
    def __init__(self, pin, light_pin):
        self.pin = pin
        self.light_pin = light_pin

        self.lastValue = False

        GPIO.setup(self.pin, GPIO.IN)
        GPIO.setup(self.light_pin, GPIO.OUT)

    def isdown(self):
        return GPIO.input(self.pin)

    def ispressed(self):
        return self.lastValue != self.isdown() and self.isdown()

    def isheld(self):
        return self.lastValue == self.isdown() and self.isdown()

    def lighton(self):
        GPIO.output(self.light_pin, 1)

    def lightoff(self):
        GPIO.output(self.light_pin, 0)

    def updatelast(self):
        self.lastValue = self.isdown()


class ShiftRegister:
    def __init__(self, data_pin, latch_pin, clock_pin, bits):
        self.data_pin = data_pin
        self.latch_pin = latch_pin
        self.clock_pin = clock_pin
        self.bits = bits

        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.latch_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)

        GPIO.output(self.shift_register.data_pin, GPIO.LOW)
        GPIO.output(self.shift_register.latch_pin, GPIO.LOW)
        GPIO.output(self.shift_register.clock_pin, GPIO.LOW)

    def writestream(self, streamofbits):
        for bit in streamofbits:
            self.write(int(bit))
        self.out()

    def write(self, on, flipped=True):
        if (flipped):
            on = not on
        GPIO.output(self.shift_register.data_pin, on)
        GPIO.output(self.shift_register.clock_pin, 1)
        GPIO.output(self.shift_register.clock_pin, 0)
        GPIO.output(self.shift_register.data_pin, 0)

    def out(self):
        GPIO.output(self.shift_register.latch_pin, 1)
        sleep(.1)
        GPIO.output(self.shift_register.latch_pin, 0)

    def clear(self):
        zeros = str(0).zfill(80)
        self.writestream(zeros)

class AlarmClock:
    def __init__(self):
        self.time_minute = 0
        self.time_hour = 12

        self.alarm_minute = 0
        self.alarm_hour = 12

        self.btn_minute = Button()
        self.btn_hour = Button()
        self.btn_snooze = Button()
        self.btn_alarm = Button()
        self.btn_time = Button()
        self.buttons = [self.btn_minute, self.btn_hour, self.btn_snooze, self.btn_alarm, self.btn_time]

        self.shift_register = ShiftRegister(21, 16, 12)
        self.display = ClockDisplay()

    def addminute(self, minute):
        minute += 1
        if minute > 59:
            minute = 0

    def addhour(self, hour):
        hour += 1
        if hour > 12:
            hour = 1

    def cleardisplay(self):
        self.shift_register.clear()

    def update(self):
        if self.btn_time.isheld():
            if self.btn_minute.ispressed():
                self.addminute(self.time_minute)
            if self.btn_hour.ispressed():
                self.addhour(self.time_hour)

        elif self.btn_alarm.isheld():
            if self.btn_minute.ispressed():
                self.addminute(self.alarm_minute)
            if self.btn_hour.ispressed():
                self.addhour(self.alarm_hour)

            hour_string = str(self.alarm_hour)
            if self.alarm_hour < 10:
                hour_string = ' ' + hour_string

            time_string = hour_string + str(self.alarm_minute).zfill(2)
            self.display.write(time_string)
        else:
            format_string = '%H%M'
            time_string = datetime.datetime.now().strftime(format_string)
            self.display.write(" 130")


    def updatelast(self):
        for btn in self.buttons:
            btn.updatelast()

def main():
    try:
        while True:
            alarm_clock = AlarmClock()
            alarm_clock.update()
            alarm_clock.updatelast()

    except KeyboardInterrupt:
        alarm_clock.cleardisplay()
        GPIO.cleanup()