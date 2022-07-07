from ast import arg
import RPi.GPIO as GPIO
import asyncio
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
cs4 = digitalio.DigitalInOut(board.D12)
cs5 = digitalio.DigitalInOut(board.D13)

mcp0 = MCP.MCP3008(spi, cs0)
mcp1 = MCP.MCP3008(spi, cs1)

B = [27,17]
GPIO.setup(B[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(B[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)

matrixen = [
    matrices.Matrix8x8(spi, cs2),
    matrices.Matrix8x8(spi, cs3)
    ]

A = [
        [
            AnalogIn(mcp0, MCP.P0),
            AnalogIn(mcp0, MCP.P1),
            AnalogIn(mcp0, MCP.P2),
            AnalogIn(mcp0, MCP.P3),
            AnalogIn(mcp0, MCP.P4),
            AnalogIn(mcp0, MCP.P5),
            AnalogIn(mcp0, MCP.P6),
            AnalogIn(mcp0, MCP.P7)
        ], 
        [
            AnalogIn(mcp1, MCP.P0),
            AnalogIn(mcp1, MCP.P1),
            AnalogIn(mcp1, MCP.P2),
            AnalogIn(mcp1, MCP.P3),
            AnalogIn(mcp1, MCP.P4),
            AnalogIn(mcp1, MCP.P5),
            AnalogIn(mcp1, MCP.P6),
            AnalogIn(mcp1, MCP.P7)
        ]]

sr0 = adafruit_74hc595.ShiftRegister74HC595(spi, cs4)
sr1 = adafruit_74hc595.ShiftRegister74HC595(spi, cs5)


LED = [
    [sr0.get_pin(n) for n in range(5)],
    [sr0.get_pin(n) for n in range(5,8)]
]
LED[1].append(sr1.get_pin(0))
LED[1].append(sr1.get_pin(1))

SCORE = [0,0]

gebruikteLDR = [[],[]]

def scanLDR(player):
    eindTijd = time.time() + random.randint(2,3)
    LDR = random.randint(0,4)
    gebruikteLDR[player].append(LDR)
    while LDR in gebruikteLDR[player]:
        LDR = random.randint(0,4)
    print('Player %i: LDR %i'%(player,LDR))
    LED[player][LDR].value = True
    while True:
        # if GPIO.input(B[player]) == False:
        #     return
        huidigeTijd = time.time()
        print('Player %i: %i'%(player,A[player][LDR].value))
        if A[player][LDR].value < 60000 or huidigeTijd > eindTijd:
            time.sleep(2)   
            LED[player][LDR].value = False
            SCORE[player] += 1
            break
    scoreBijhouden(player)
    return("klaar")

def displayGewonnen(player):
    GPIO.setmode(GPIO.BCM)
    for char in "Gewonnen!":
        matrixen[player].fill(0)
        matrixen[player].text(char, 0, 0)
        matrixen[player].show()
        time.sleep(0.5)
    time.sleep(0.5)
    matrixen[player].fill(0)

def displayScore(player, score):
    if (score < 5):
        matrixen[player].fill(0)
        matrixen[player].text(str(score), 0, 0)
        matrixen[player].show()
    else:
        raise Exception("score > 9")

def scoreBijhouden(player):
    try:
        displayScore(player, SCORE[player])
    except:
        gewonnen = threading.Thread(target=displayGewonnen, args=(player,))
        gewonnen.start()
        for i in range(5):
            for light in LED[player]:
                light.value = True
            time.sleep(0.5)
            for light in LED[player]:
                light.value = False
            time.sleep(0.5)
        gameReset(player)

def startGame(player):
    SCORE[player] = 0
    displayScore(player, SCORE[player])
    scanLDR(player)
        

def gameReset(player):
    SCORE[player] = 0
    gebruikteLDR[player] = []
    scoreBijhouden(player)

async def displayPressStart(player):
    for char in "Druk op start":
        matrixen[player].fill(0)
        matrixen[player].text(char, 0, 0)
        matrixen[player].show()
        time.sleep(0.5)

def pressStart(player):
    while True:
        if SCORE[player] > 5:
                gameReset(player)
        if GPIO.input(B[player]) == False:
            # gedaan = asyncio.run(scanLDR(player))
            gedaan = scanLDR(player)
            while gedaan != "klaar":
                pass
            eindTijd = time.time() + 10
        if SCORE[player] != 0 and time.time() > eindTijd:
            gameReset(player)
                 


def main():
    player0 = threading.Thread(target=pressStart, args=(0,))
    player1 = threading.Thread(target=pressStart, args=(1,))
    player0.start()
    player1.start()

    # asyncio.run(pressStart(0))
    # asyncio.run(pressStart(1))

if (__name__ == "__main__"):
    try:
        main()
    except Exception as error:
        print(error)
    finally:
        for matrix in matrixen:
            matrix.fill(0)
            matrix.text("-", 1, 0)
            matrix.show()
        for player in LED:
            for led in player:
                led.value = False
                
                
# GPIO.cleanup()
