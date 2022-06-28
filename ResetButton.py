import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

BUTTON = 17
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if GPIO.input(BUTTON) == False:
        print("Hij doet het!")
    else:
        print("Hij doet het niet!")