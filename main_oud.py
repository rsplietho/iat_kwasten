from adafruit_shell import Shell
import busio
import digitalio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import sys
import RPi.GPIO as GPIO
import time
import adafruit_74hc595
import random
import asyncio

from setuptools import setup

# ADC0
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs0 = digitalio.DigitalInOut(board.CE0)
cs1 = digitalio.DigitalInOut(board.CE1)

mcp0 = MCP.MCP3008(spi, cs0)
mcp1 = MCP.MCP3008(spi, cs1)

A = [
AnalogIn(mcp0, MCP.P0),
AnalogIn(mcp0, MCP.P1),
AnalogIn(mcp0, MCP.P2),
AnalogIn(mcp0, MCP.P3),
AnalogIn(mcp0, MCP.P4),
AnalogIn(mcp0, MCP.P5),
AnalogIn(mcp0, MCP.P6),
AnalogIn(mcp0, MCP.P7),
AnalogIn(mcp1, MCP.P0),
AnalogIn(mcp1, MCP.P1),
AnalogIn(mcp1, MCP.P2),
AnalogIn(mcp1, MCP.P3),
AnalogIn(mcp1, MCP.P4),
AnalogIn(mcp1, MCP.P5),
AnalogIn(mcp1, MCP.P6),
AnalogIn(mcp1, MCP.P7)
]



latch_pin = digitalio.DigitalInOut(board.D20)
sr = adafruit_74hc595.ShiftRegister74HC595(spi, latch_pin)

LED = [sr.get_pin(n) for n in range(8)]

# GPIO.setup((17,27), GPIO.IN, pull_up_down=GPIO.PUD_UP)
# button0 = GPIO.input(17)
# button1 = GPIO.input(27)

btn0 = DigitalInOut(board.D17)
btn0.direction = Direction.INPUT
btn0.pull = Pull.UP

btn1 = DigitalInOut(board.D27)
btn1.direction = Direction.INPUT
btn1.pull = Pull.UP

from rpi_ws281x import ws, Color, Adafruit_NeoPixel
# LED strip configuration:
LED_1_COUNT = 11        # Number of LED pixels.
LED_1_PIN = 18          # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_1_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_1_DMA = 10          # DMA channel to use for generating signal (Between 1 and 14)
LED_1_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_1_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_1_CHANNEL = 0       # 0 or 1

LED_2_COUNT = 11        # Number of LED pixels.
LED_2_PIN = 13          # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_2_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_2_DMA = 11          # DMA channel to use for generating signal (Between 1 and 14)
LED_2_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_2_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_2_CHANNEL = 1       # 0 or 1

strips = [Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ,
                            LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS,
                            LED_1_CHANNEL),
        Adafruit_NeoPixel(LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ,
                            LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS,
                            LED_2_CHANNEL)
]

def ledStrip(strip, color, amount):
    for i in range(amount):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(100 / 1000.0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


SCORE = [0,0]

def scoreBijhouden(player):
    if SCORE[player] == 11:
        theaterChaseRainbow(strips[player])
    ledStrip(strips[player],Color(0,255,0),SCORE[player])
    

def scanLDR(player):
    LDR = random.randint(0,1)
    LED[LDR].value = True
    stopconditie = False
    while not stopconditie:
        if A[LDR].value < 10000:
            SCORE[player] += 1
            LED[LDR].value = False
            scoreBijhouden(player)



async def player1():
    while True:
        scanLDR(0)

async def player2():
    while True:
        scanLDR(1)

# async def buttons():
#     while True:
        
def blackout(strip):
    for i in range(max(strip.numPixels(), strip.numPixels())):
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()


# main
def main():
    for strip in strips:
        blackout(strip)
    strips[0].begin()
    strips[1].begin()

    asyncio.run(player1())
    asyncio.run(player2())

        

if __name__ == "__main__":
    # Shell.require_root()
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()