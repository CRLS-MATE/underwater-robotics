#include <Servo.h>

int inByte;
int currentServo = 2;
Servo myservos[7];  // create servo object to control a servo

void setup() {
  for (int x = 2; x <= 8; x++) 
    myservos[x - 2].attach(x);  // attaches the servo on pin 9 to the servo object

  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    inByte = Serial.read();
    if (inByte >= 180) {
      inByte -= 180;
      currentServo = inByte;
      Serial.println(currentServo);
    } else {
      myservos[currentServo].write(inByte);
      Serial.print(currentServo);
      Serial.print('\t');
      Serial.println(inByte);
    }
  }
}
