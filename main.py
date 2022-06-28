import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


def main():
    print("hello world")

if (__name__ == "__main__"):
    try:
        main()
    except:
        print("error")
