"""Main setup"""

from gpiozero import Robot, AngularServo

# func for initial setup of the car
def init():
    global servo, init_angle
    servo.angle = init_angle
# Motors' pins
left_motor_pins = (4, 14)
right_motor_pins = (17, 18)

# Servo's pins
servo_pin = 21
min_servo_angle = -90
max_servo_angle = 90
init_angle = 0

# Using ready class Robot for controlling movement
robot = Robot(left=left_motor_pins, right=right_motor_pins)

# Using class AngularServo for precise setting of the angle
servo = AngularServo(servo_pin, min_angle=min_servo_angle, max_angle=max_servo_angle)
