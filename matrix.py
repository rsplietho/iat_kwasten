import threading
import time
import board
import digitalio
from adafruit_max7219 import matrices

spi = board.SPI()
cs0 = digitalio.DigitalInOut(board.D20)
cs1 = digitalio.DigitalInOut(board.D21)

matrixen = [
    matrices.Matrix8x8(spi, cs0),
    matrices.Matrix8x8(spi, cs1)
    ]

def matrix(matrixString, matrix):
    while True:
        for char in matrixString:
            matrixen[matrix].fill(0)
            matrixen[matrix].text(char, 0, 0)
            matrixen[matrix].show()
            time.sleep(0.5)
        time.sleep(0.5)

def main():
    # asyncio.run(matrix("dinges", 0))
    # print('test')
    # asyncio.run(matrix("Peer", 1))
    matrix0 = threading.Thread(target=matrix, args=("dinges", 0,))
    matrix1 = threading.Thread(target=matrix, args=("peren", 1,))
    matrix0.start()
    matrix1.start()

main()