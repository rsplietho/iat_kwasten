import RPi.GPIO as GPIO
import busio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import board
import digitalio

GPIO.setmode(GPIO.BCM)

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

def main():
    while True:
        # for pin in A:# range(0,3):
        #     print(pin.value)
        # print("")
        # print(A[0].value)
        # time.sleep(0.5)

        for ldr in range(16):
            if(A[ldr].value < 30000):
                print(ldr, A[ldr].value)
            time.sleep(0.5)

main()