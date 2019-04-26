#include <Servo.h>

int inByte;
int currentServo = 2;
Servo myservos[24];  // create servo object to control a servo

void setup() {
  for (int x = 2; x <= 13; x++) {
    pinMode(x, OUTPUT);
  }

  digitalWrite(8, LOW);
  digitalWrite(9, LOW);
  digitalWrite(12, HIGH);
  digitalWrite(13, HIGH);
  
  for (int x = 2; x <= 13; x++) {
    if (!block(x)) {
      myservos[x - 2].attach(x);  // attaches the servo on pin 9 to the servo object
    }
  }

  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    inByte = Serial.read();
    if (inByte >= 180) {
      inByte -= 180;
      if(!block(inByte)) {
        currentServo = inByte;
        Serial.println(currentServo);
      }
    } else {
      myservos[currentServo].write(inByte);
      Serial.print(currentServo);
      Serial.print('\t');
      Serial.println(inByte);
    }
  }
}

bool block(int pin) { // special pins for motor shield
  return (pin == 8 || pin == 9 || pin == 12 || pin == 13);
}
