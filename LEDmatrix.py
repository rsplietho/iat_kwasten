from machine import I2C, Pin, RTC
from HT16k33matrix import HT16k33matrix
from time import sleep

import RPi.GPIO as GPIO
import time 


I2C = I2C(scl=pin(22), sda=pin(21))
display = HT16k33matrix(I2C)
display.set_brightness(10)
display.set_angle(270)

#code voor letter op de cijfer 5 op de matrix
display.set_character(ord(5), True)


# Code voor de win animatie:
while True:
    x = 7
    y = 0
    dx = 0 
    dy = 1
    mx = 6
    my = 7
    nx = 0
    ny = 0

    for i in range(0,64):
        display.plot(x, y).draw();

        if dx == 1 and x == mx:
            dy = 1;
            dx = 0;
            mx -= 1;
        elif dx == -1 and x == nx:
            nx += 1;
            dy = -1;



#LDR connectie

GPIO.setmode(GPIO.BOARD)
delayt = .1
value = 0
ldr = 7 
led = 11
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, false)

def rc_time(ldr):
    count = 0


    GPIO.setup(ldr, GPIO.OUT)
    GPIO.output(ldr, False)
    time.sleep(delayt)

    GPIO.setup(ldr, GPIO.IN)

    while(GPIO.input(ldr) == 0):
        count +=1

    return count


try:
        while True:
            print("Ldr Value:")
            value = rc_time(ldr)
            print(value)
            if(value <= 10000):
                print("lights are ON")
                GPIO.output(led, True)
            if(value > 10000):
                print("Lights are OFF")
                GPIO.output(led, False)

except Keyboardinterrup:
    pass
finally: 
    GPIO.cleanup()

