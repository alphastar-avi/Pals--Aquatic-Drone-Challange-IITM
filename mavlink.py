import RPi.GPIO as GPIO
import time
from pymavlink import mavutil
from dronekit import connect, VehicleMode, LocationGlobalRelative

# Ultrasonic Sensor Pins
TRIG_LEFT = 23
ECHO_LEFT = 25
TRIG_RIGHT = 24
ECHO_RIGHT = 26

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_LEFT, GPIO.OUT)
GPIO.setup(ECHO_LEFT, GPIO.IN)
GPIO.setup(TRIG_RIGHT, GPIO.OUT)
GPIO.setup(ECHO_RIGHT, GPIO.IN)

# Connect to Pixhawk via USB 
vehicle = connect('/dev/ttyACM0', baud=115200, wait_ready=True)

# Get distance from ultrasonic sensor
def get_distance(trig, echo):
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(echo) == 0:
        start_time = time.time()

    while GPIO.input(echo) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  
    return distance

# Function to control motors using RC override
def control_motors(left_speed, right_speed):
    vehicle.channels.overrides = {
        "1": left_speed,  
        "3": right_speed 
    }

# Set waypoints for GPS navigation
waypoints = [
    LocationGlobalRelative(37.7749, -122.4194, 1),  
    LocationGlobalRelative(37.7750, -122.4200, 1)
]

# Function to follow GPS waypoints
def follow_waypoints():
    vehicle.mode = VehicleMode("AUTO")  
    vehicle.commands.next = 0
    vehicle.commands.upload()

# Main loop for obstacle avoidance
try:
    follow_waypoints()
    while True:
        left_distance = get_distance(TRIG_LEFT, ECHO_LEFT)
        right_distance = get_distance(TRIG_RIGHT, ECHO_RIGHT)

        if left_distance < 30:
            print("Obstacle on Left! Turning Right")
            control_motors(1500, 1600)  # Increase right motor speed
        elif right_distance < 30:
            print("Obstacle on Right! Turning Left")
            control_motors(1600, 1500)  # Increase left motor speed
        else:
            print("Following GPS Waypoints")
            control_motors(1600, 1600)  # Normal speed

        time.sleep(0.1)

except KeyboardInterrupt:
    vehicle.close()
    GPIO.cleanup()
