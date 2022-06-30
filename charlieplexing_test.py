from charlieplexing import Charlieplexing
import RPi.GPIO as GPIO

leds = Charlieplexing([6,13,19,26])

def main():
    for led in range(0,11):
        print("LED nummer: " + str(led))
        leds.lightLED(led)
        try:
            input("Press enter to continue")
        except SyntaxError:
            pass


try:
    main()
except KeyboardInterrupt:
        print('Interrupted')
        GPIO.cleanup()