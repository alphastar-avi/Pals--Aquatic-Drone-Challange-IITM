#include <Ultrasonic.h>
#include <Servo.h>

#define TRIG_PIN 12   // HC-SR04 Trig
#define ECHO_PIN 13   // HC-SR04 Echo
#define SERVO_PIN 5   // Servo Signal

Ultrasonic ultrasonic(TRIG_PIN, ECHO_PIN);
Servo myServo;

void setup() {
    Serial.begin(9600);
    myServo.attach(SERVO_PIN);
}

void loop() {
    for (int angle = 0; angle <= 180; angle += 10) {
        myServo.write(angle);
        delay(15);  
        sendDistance(angle);
    }
    for (int angle = 180; angle >= 0; angle -= 10) {
        myServo.write(angle);
        delay(15);
        sendDistance(angle);
    }
}

void sendDistance(int angle) {
    int distance = ultrasonic.read();
    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
}`