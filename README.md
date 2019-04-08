# underwater-robotics

## Arduino Control: `arduino_serial_servo_controller.ino`

Controls servos on pins 2+
Receives bytes over serial to control each of the servos.
If the byte is 180+, it sets the servo in focus to pin `182 - <byte>`
If the byte is less than 180, it sets the servo in focus to that value
