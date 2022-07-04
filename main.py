import RPi.GPIO as GPIO
# import charlieplexing.py
import threading
import time
import board
import digitalio
import random
import busio
import adafruit_74hc595
from adafruit_max7219 import matrices
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

GPIO.setmode(GPIO.BCM)

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs0 = digitalio.DigitalInOut(board.CE0)
cs1 = digitalio.DigitalInOut(board.CE1)
cs2 = digitalio.DigitalInOut(board.D20)
cs3 = digitalio.DigitalInOut(board.D21)

mcp0 = MCP.MCP3008(spi, cs0)
mcp1 = MCP.MCP3008(spi, cs1)

matrixen = [
    matrices.Matrix8x8(spi, cs2),
    matrices.Matrix8x8(spi, cs3)
    ]

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

cs_sr = digitalio.DigitalInOut(board.D12)
sr = adafruit_74hc595.ShiftRegister74HC595(spi, cs_sr)

LED = [sr.get_pin(n) for n in range(8)]

SCORE = [0,0]

def scanLDR(player):
    LDR = random.randint(0,1)
    stopconditie = False
    while not stopconditie:
        if A[LDR].value < 10000:
            SCORE[player] += 1
            

def main():
    print("hello world")

if (__name__ == "__main__"):
    try:
        main()
    except:
        print("error")
