#include <Servo.h>

Servo servo;
const int servoPin = 10;
int servoValue;
int count;

void setup() {
  Serial.begin(9600);
  servo.attach(servoPin);
  servoValue = 90;
  count = 0;
}

void loop() {
  if (Serial.available() > 0) {
    servoValue = Serial.parseInt();
    Serial.print("value = "); Serial.println(servoValue);
    setServo(servoValue);
  }
}

void setServo(int angle) {
  if(angle < 0) {
    angle = 0;
  }
  if(angle > 180) {
    angle = 180;
  }
  
  servo.write(angle);
}
