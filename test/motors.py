from gpiozero import Robot
from time import sleep

robot = Robot(left=(4, 14), right=(17, 18))

# Draw a square
if __name__ == "__main__":
    inc = 0
    while inc!=5:
        robot.forward()
        sleep(10)
        robot.right()
        sleep(1)
        inc += 1
