import time
from datetime import datetime
import os

# Custom seven-segment style digits
segments = {
    '0': [" __ ",
          "|  |",
          "|__|"],
    '1': ["    ",
          "   |",
          "   |"],
    '2': [" __ ",
          " __|",
          "|__ "],
    '3': [" __ ",
          " __|",
          " __|"],
    '4': ["    ",
          "|__|",
          "   |"],
    '5': [" __ ",
          "|__ ",
          " __|"],
    '6': [" __ ",
          "|__ ",
          "|__|"],
    '7': [" __ ",
          "   |",
          "   |"],
    '8': [" __ ",
          "|__|",
          "|__|"],
    '9': [" __ ",
          "|__|",
          " __|"],
    ':': ["    ",
          "  • ",
          "  • "]
}

def displaytime(hhmmss):
    lines = ["", "", ""]
    for char in hhmmss:
        for i in range(3):
            lines[i] += segments[char][i] + ""
    return lines

def refreshterminal():
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)

while True:
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    clock_lines = displaytime(time_str)
    refreshterminal()

    print("|--------------------------------------|")
    print("|            Digital Clock             |")
    print("|--------------------------------------|")
    for line in clock_lines:
        print(f"|  {line}    |")
    print("|--------------------------------------|")

    time.sleep(1)
