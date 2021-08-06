from gpiozero import Robot
from time import sleep

robot = Robot(left=(4, 14), right=(17, 18))

# Draw a square
while True:
    robot.forward()
    sleep(10)
    robot.right()
    sleep(1)
