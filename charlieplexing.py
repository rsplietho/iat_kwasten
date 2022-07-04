import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# charliePins=[6,13,19,26]
# charliePins = []
# charlieLEDS=[]

def initCharlieLeds(pins):
    leds = []
    for i in range(0,len(pins)-1):
            for j in range(i+1,len(pins)):
                    leds.append([pins[i],pins[j]])
                    leds.append([pins[j],pins[i]])
    return leds
    

class Charlieplexing:
    def __init__(self, charlie_pins):
        print("init begin")
        self.charliePins = charlie_pins
        self.charlieLEDS = initCharlieLeds(self.charliePins)
        print("init end")
    
    # def lightLED(led):
    #     self.igniteled(led)

    def lightLED(self, led):
        #First clear the pins, by setting them all to input

        for pin in self.charliePins:
            GPIO.setup(pin,GPIO.IN)


        for pin in self.charliePins:
            print("Pin "+str(pin)+": "+str(GPIO.input(pin)))
        
        #Now setup the first pin for HIGH OUTPUT
        GPIO.setup(self.charlieLEDS[led][0],GPIO.OUT)
        GPIO.output(self.charlieLEDS[led][0],GPIO.HIGH)
        
        #Now setup the second pin for LOW OUTPUT
        GPIO.setup(self.charlieLEDS[led][1],GPIO.OUT)
        GPIO.output(self.charlieLEDS[led][1],GPIO.LOW)

        for pin in self.charliePins:
            print("Pin "+str(pin)+": "+str(GPIO.input(pin)))
        print("")

    def clearLEDS(self):
        for pin in self.charliePins:
            GPIO.setup(pin,GPIO.IN)








