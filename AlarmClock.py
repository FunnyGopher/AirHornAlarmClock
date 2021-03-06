import RPi.GPIO as GPIO
from time import sleep
import datetime
import serial
import math

# A class that represents the 5 displays
class ClockDisplay:
    def __init__(self, shift_register):
        self.shift_register = shift_register
        self.displays = 6
        self.curr_display= 0
        self.show_dots = True
		
		# Dictionary for all of the supported characters and their hex codes
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
            ' ': '',
            ':': ''
        }
	
	# Relates a characters hex code to a decimal number relating to the segments
    def charToSegment(self, char):
        value = 0
        for i in char:
            power = int(i, 16)
            value += pow(2, power)
        return value
	
	# Clears the displays. Basically turns them off.
    def clear(self):
        clear_string = ""
        for i in range(self.shift_register.bits):
            clear_string += '0'
        self.shift_register.writestream(clear_string, self.shift_register.bits)
	
	# Converts a text string into a binary bit stream for the shift registers
    def writeText(self, text):
        bin_output = ""
        
        if self.show_dots:
            text = ':'+ text
        else:
            text = ' ' + text;
            
        for i in text:
            hexcode = self.chars[i]
            dec = self.charToSegment(hexcode)
            if i == ':':
                dec = 3
            if i == ' ':
                dec = 0
            bincode = bin(dec)[2:]

            if len(bincode) < 16:
                dif = 16 - len(bincode)
                for i in range(dif):
                    bincode = '0' + bincode
            
            bin_output += bincode
            
        #self.shift_register.multiplexwritestream(bin_output, self.curr_display, self.displays)
        self.shift_register.writestream(bin_output)
        self.curr_display +=1
        if self.curr_display >= self.displays:
            self.curr_display = 0

# A class that represents a button! :D
class Button:
    def __init__(self, pin, light_pin):
        self.pin = pin # Data pin
        self.light_pin = light_pin # Pin for the light

        self.lastValue = False
        self.down = False

        GPIO.setup(self.pin, GPIO.IN)
        GPIO.setup(self.light_pin, GPIO.OUT)
	
	# Returns the button state
    def isdown(self):
        return GPIO.input(self.pin)
	
	# Returns if a button has been pushed down and released
    def ispressed(self):
        return self.lastValue != self.isdown() and self.isdown()
	
	# Returns if a button has been held down
    def isheld(self):
        return self.lastValue == self.isdown() and self.isdown()
	
	# Turns the light for the button on
    def lighton(self):
        GPIO.output(self.light_pin, 1)

	#  Turns the light for the button off
    def lightoff(self):
        GPIO.output(self.light_pin, 0)
	
	# Updates the buttons state
    def update(self):
        self.down = self.isdown()
	
	# Updates the button's last state for pressed and held calculations
    def updatelast(self):
        self.lastValue = self.down

# A class that represents the shift register array
class ShiftRegister:
    def __init__(self, data_pin, latch_pin, clock_pin, bits):
        self.data_pin = data_pin # Data pin
        self.latch_pin = latch_pin # Latch pin
        self.clock_pin = clock_pin # Clock pin
        self.bits = bits # The number of bits this shift register is represents

        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.latch_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)

        GPIO.output(self.data_pin, GPIO.LOW)
        GPIO.output(self.latch_pin, GPIO.LOW)
        GPIO.output(self.clock_pin, GPIO.LOW)
	
	# Writes a stream of bits to the shift register
    def writestream(self, streamofbits):
        for bit in streamofbits:
            self.write(int(bit))
        self.out()
	
	# Writes a stream of bits to the shift register using multiplexing. This
	# sequentially looping through each 16 bits of data
    def multiplexwritestream(self, streamofbits, curr_display, displays):
        firstindex = curr_display * 16
        secondindex = firstindex + 16
        keeperbits = streamofbits[firstindex:secondindex]
        zerosafter = (displays - curr_display - 1) * 16
        
        zerosbeforestring = ""
        for i in range(firstindex):
            zerosbeforestring += '0'

        zerosafterstring = ""
        for i in range(zerosafter):
            zerosafterstring += '0'

        newstreamofbits = zerosbeforestring + keeperbits + zerosafterstring
        self.writestream(newstreamofbits)

        curr_display += 1
        if(curr_display >= displays):
            curr_display = 0
	
	# Writes a single bit to the shift register
    def write(self, on, flipped=True):
        if (flipped):
            on = not on
        GPIO.output(self.data_pin, on)
        GPIO.output(self.clock_pin, 1)
        GPIO.output(self.clock_pin, 0)
        GPIO.output(self.data_pin, 0)
	
	# Latches the shift register
    def out(self):
        GPIO.output(self.latch_pin, 1)
        #sleep(.1)
        GPIO.output(self.latch_pin, 0)
	
	# Clears the shift register by passing the register zeros
    def clear(self):
        zeros = ""
        for i in range(self.bits):
            zeros += '0'
        self.writestream(zeros)

# The class that represents the project as a whole
class AlarmClock:
    def __init__(self):
        self.time_minute = 0
        self.time_hour = 0 # saved in military time, easier to use

        self.alarm_minute = 0
        self.alarm_hour = 0 # saved in military time easier to use

        self.military_time = False
        self.alarm_active = False
        
		# Trys to intstantiate the servo
		# Problems with the port the Arduino is plugged into, hopefully this finds the Arduino...
        try:
            self.servo = serial.Serial("/dev/ttyACM0", 9600)
        except: 
            self.servo = serial.Serial("/dev/ttyACM1", 9600)
           
		# Currently, the light pins are random
        self.btn_minute = Button(6, 2)
        self.btn_hour = Button(22, 25)
        self.btn_snooze = Button(4, 18)
        self.btn_alarm = Button(19, 8)
        self.btn_time = Button(17, 10)
        self.buttons = [self.btn_minute, self.btn_hour, self.btn_snooze, self.btn_alarm, self.btn_time]
        
        shift_register = ShiftRegister(21, 16, 12, 80)
        self.display = ClockDisplay(shift_register)
	
	# Adds a minute to the time minute or alarm minute
    def addminute(self, minute):
        minute += 1
        if minute > 59:
            minute = 0

        return minute
	
	# Adds an hour to the time hour or alarm hour
    def addhour(self, hour):
        hour += 1
        if hour > 23:
            hour = 0
        return hour
	
	# Clears the display. Pretty much turns the displays off
    def cleardisplay(self):
        self.shift_register.clear()
	
	# Rotates the servo to a designated degree of rotation using the Arduino
    def rotateservo(self, degrees):
        self.servo.write(bytes(str(int(degrees)), "UTF-8"))
        sleep(.1)
	
	# Formats the time recieved from Pi to display on the segment displays
	# Adds an A or a P for am or pm
	# Also checks for military time or standard time
    def formattime(self, hours, minutes):
        ampm = "A"
        if hours >= 12:
            ampm = "P"            
            
        if not self.military_time:
            if hours == 0:
                hours = 12
            if hours > 12:
                hours %= 12
        else:
            if hours > 23:
                hours %= 24

        if minutes > 59:
            minutes %= 60

        # Blanks out the first display if the hour is a single digit
        hour_string = str(hours)
        if hours < 10:
            hour_string = ' ' + hour_string

        # Adds a 0 if the minute is a single digit
        minute_string = str(minutes)
        if minutes < 10:
            minute_string = '0' + minute_string

        time_string = hour_string + minute_string + ampm
        return time_string
	
	# The update loop for the alarm clock
    def update(self):
		# Updates the button states
        for btn in self.buttons:
            btn.update()
        
		# Logic for the different button presses
        if self.btn_time.isheld():
            if self.btn_minute.ispressed():
                self.time_minute = self.addminute(self.time_minute)
            if self.btn_hour.ispressed():
                self.time_hour = self.addhour(self.time_hour)
        
        if self.btn_alarm.isheld():
            if self.btn_minute.ispressed():
                self.alarm_minute = self.addminute(self.alarm_minute)
            if self.btn_hour.ispressed():
                self.alarm_hour = self.addhour(self.alarm_hour)

            self.display.writeText(self.formattime(self.alarm_hour, self.alarm_minute))      
        else:
			# Shows the time
            d = datetime.datetime.now()
            hours = d.hour + self.time_hour
            minutes = d.minute + self.time_minute
            time_string = self.formattime(hours, minutes)
            self.display.writeText(time_string)
            
        # Snooze button logic
        if self.btn_snooze.ispressed() and self.alarm_active:
            self.alarm_active = False
            for i in range(5):
                self.alarm_minute = self.addminute(self.alarm_minute)
            if self.alarm_minute <= 4:
                self.alarm_hour = self.addhour(self.alarm_hour)
		
		# Alarm logic
        d = datetime.datetime.now()
        hour = d.hour
        minute = d.minute
        if hour == self.alarm_hour and minute == self.alarm_minute:
            self.alarm_active = True
		
		# Moves the servo if the alarm is active
        if self.alarm_active:
            self.rotateservo(30)
        else:
            self.rotateservo(180)
		
		#Resets the alarm if snooze is pressed
        if self.alarm_active and abs(minute - self.alarm_minute) >= 3:
            self.alarm_active = False
	
	# Updates the last state of the button
    def updatelast(self):
        for btn in self.buttons:
            btn.updatelast()

# The function that starts the alarm clock runs the loop
def main():
    GPIO.setmode(GPIO.BCM)
    try:
        alarm_clock = AlarmClock()
        while True:
            alarm_clock.update()
            alarm_clock.updatelast()
            sleep(.00000000000001)

    except KeyboardInterrupt:
        alarm_clock.cleardisplay()
        GPIO.cleanup()
        
main()
GPIO.cleanup()
