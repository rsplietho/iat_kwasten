import RPi.GPIO as GPIO
import adafruit_74hc595
import digitalio
import board
import busio
import time

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs_sr = digitalio.DigitalInOut(board.D12)
cs_sr2 = digitalio.DigitalInOut(board.D13)
sr = adafruit_74hc595.ShiftRegister74HC595(spi, cs_sr)
sr2 = adafruit_74hc595.ShiftRegister74HC595(spi, cs_sr2)

LED = [sr.get_pin(n) for n in range(8), sr2.get_pin(0)]
# LEDappend= [sr2.get_pin(n) for n in range(2)]
LED.append(sr2.get_pin(0))
LED.append(sr2.get_pin(1))

while True:
    for led in LED:
        led.value = True
        time.sleep(0.5)
        led.value = False

# pin1 = sr.get_pin(1)

# while True:
#     pin1.value = True
#     time.sleep(1)
#     pin1.value = False
#     time.sleep(1)

