"""Main setup"""

from gpiozero import Robot
from time import sleep

# Motors' pins
left_motor_pins = (4, 14)
right_motor_pins = (17, 18)

# Using ready class Robot for controlling movement
robot = Robot(left=left_motor_pins, right=right_motor_pins)
