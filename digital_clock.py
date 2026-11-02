import time
import os
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_digit_pattern(digit):
    patterns = {
        '0': [
            " █████ ",
            "█     █",
            "█     █",
            "█     █",
            "█     █",
            "█     █",
            " █████ "
        ],
        '1': [
            "  ███  ",
            " ████  ",
            "   ██  ",
            "   ██  ",
            "   ██  ",
            "   ██  ",
            " ██████"
        ],
        '2': [
            "██████ ",
            "      █",
            "      █",
            " █████ ",
            "█      ",
            "█      ",
            "███████"
        ],
        '3': [
            "██████ ",
            "      █",
            "      █",
            "██████ ",
            "      █",
            "      █",
            "██████ "
        ],
        '4': [
            "█    █ ",
            "█    █ ",
            "█    █ ",
            "██████ ",
            "     █ ",
            "     █ ",
            "     █ "
        ],
        '5': [
            "███████",
            "█      ",
            "█      ",
            "██████ ",
            "      █",
            "      █",
            "██████ "
        ],
        '6': [
            " █████ ",
            "█      ",
            "█      ",
            "██████ ",
            "█     █",
            "█     █",
            " █████ "
        ],
        '7': [
            "███████",
            "      █",
            "      █",
            "      █",
            "      █",
            "      █",
            "      █"
        ],
        '8': [
            " █████ ",
            "█     █",
            "█     █",
            " █████ ",
            "█     █",
            "█     █",
            " █████ "
        ],
        '9': [
            " █████ ",
            "█     █",
            "█     █",
            " ██████",
            "      █",
            "      █",
            " █████ "
        ],
        ':': [
            "       ",
            "   ██  ",
            "   ██  ",
            "       ",
            "   ██  ",
            "   ██  ",
            "       "
        ]
    }
    return patterns.get(digit, ["       "] * 7)

def display_time(time_string):
    digit_patterns = [get_digit_pattern(c) for c in time_string]
    for row in range(7):
        output_line = ""
        for pattern in digit_patterns:
            output_line += pattern[row] + "  "  # add spacing between digits
        print("  " + output_line)

def run_clock():
    while True:
        clear_screen()
        now = datetime.now()
        time_display = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
        print("\n" * 4)
        display_time(time_display)
        # Display date
        month_day_year = now.strftime("%B %d %Y").upper()
        weekday = now.strftime("%A").upper()
        date_info = f"{month_day_year}      {weekday}"
        print(f"\n{date_info.center(60)}")
        time.sleep(1)

if __name__ == "__main__":
    run_clock()
