import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

while True:
BUTTON = 17
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if GPIO.input(BUTTON) == FALSE:
    print("Hij doet het!")
else:
    print("Hij doet het niet!")