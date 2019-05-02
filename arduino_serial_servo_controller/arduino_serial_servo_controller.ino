#include <Servo.h>

int inByte;
int currentServo = 2; // changes based on values sent over serial
Servo myservos[24];  // create servo object to control a servo

void setup() {
  for (int x = 2; x <= 13; x++) {
    pinMode(x, OUTPUT);
  }

  digitalWrite(12, HIGH); // Direction pin for A
  digitalWrite(13, HIGH); // Direction pin for B
  
  for (int x = 2; x <= 11; x++) {
    if(x != 3 && x != 11) {
      myservos[x - 2].attach(x);  // attaches the servo on pin 9 to the servo object

      switch(x) {
        case 8: // claw
          myservos[x-2].write(45);
          break;
        case 9: // linear actuator
          myservos[x-2].write(45);
        default:
          myservos[x-2].write(92);
      }
    }
//    if (!block(x)) {
//      myservos[x - 2].attach(x);  // attaches the servo on pin 9 to the servo object
//    }
  }

  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    inByte = Serial.read();
    if (inByte >= 182 && inByte < 192) { // if it's a reasonable servo value
      inByte -= 180;
      currentServo = inByte;
//      if(!block(inByte)) {
//        Serial.println(currentServo);
//      }
    } else if(inByte <= 180) {
      if(currentServo != 3 && currentServo != 11) {
        myservos[currentServo - 2].write(inByte);
      } else {
        if(inByte > 90) {
          digitalWrite(currentServo + 9, HIGH); // Set direction
          analogWrite(currentServo, float(inByte - 90) * (255.0 / 90.0));
        } else {
          digitalWrite(currentServo + 9, LOW); // Set direction
          analogWrite(currentServo, float(90 - inByte) * (255.0 / 90.0));          
        }
      }
//      Serial.print(currentServo);
//      Serial.print('\t');
//      Serial.println(inByte);
    }
  }
}

//bool block(int pin) { // special pins for motor shield
//  return (pin == 12 || pin == 13);
//}
