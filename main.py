import os
import time
import datetime
from tkinter import E
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from pygame import mixer

from config import configs

print("configs:")
print(configs)

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)

mixer.init()

# Define grid layout and cell numbers
GRID = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"]
]

# Define stick position thresholds
VREF = 3.3
POSITION_LOW = VREF * 0.33
POSITION_MEDIUM = VREF * 0.66

SOURCE_DIR = os.path.dirname(__file__)

# Define filenames for stick routes
ROUTE_MAPPING_FILE = SOURCE_DIR + "/route_mapping.txt"

STARTUP_SOUND = SOURCE_DIR + "/sfx/startup.wav"
POWERDOWN_SOUND = SOURCE_DIR + "/sfx/powerdown.wav"
ERROR_SOUND = SOURCE_DIR + "/sfx/error.wav"

def read_route_mapping(filename):
    route_mapping = {}
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split()
            route = [str(cell) for cell in parts[:-1]]
            filename = parts[-1]
            route_mapping["".join(route)] = filename
    return route_mapping

# Load the route-to-filename mapping from the file
route_to_filename = read_route_mapping(ROUTE_MAPPING_FILE)
print(route_to_filename)

def play_audio(file):
    sound = mixer.Sound(file)
    sound.play()

def get_cell(position):
    if position < POSITION_LOW:
        return 0
    elif position < POSITION_MEDIUM:
        return 1
    else:
        return 2

def main():
    current_row = 1
    current_col = 1
    recorded_cells = []
    
    cell_update_time = datetime.datetime.now()

    print("Starting loop")
    play_audio(STARTUP_SOUND)

    try:
        while True:
            horizontal_position = chan1.voltage
            vertical_position = chan0.voltage
            
            new_row = get_cell(vertical_position)
            new_col = get_cell(horizontal_position)
            
            if new_row != current_row or new_col != current_col:
                current_row = new_row
                current_col = new_col
                cell_update_time = datetime.datetime.now()

            if datetime.datetime.now() > cell_update_time + datetime.timedelta(milliseconds=float(configs["CELL_CHANGE_DELAY"])):
                # we are in the middle, our starting position
                if len(recorded_cells) == 0 and GRID[current_row][current_col] == "5":
                    continue
                # if nothing changed, don't do anything
                if len(recorded_cells) > 0 and GRID[current_row][current_col] == recorded_cells[-1]:
                    continue

                recorded_cells.append(GRID[current_row][current_col])
                print(recorded_cells)
            
            if GRID[current_row][current_col] == "5" and recorded_cells:
                print(recorded_cells)
                print("-".join(recorded_cells))
                route_filename = route_to_filename.get("".join(recorded_cells))
                if route_filename:
                    print("Playing audio:", route_filename)
                    play_audio(SOURCE_DIR + "/" + route_filename)
                recorded_cells = []
            
            time.sleep(float(configs["SLEEP_DURATION"]))
            
    except KeyboardInterrupt:
        print("Exiting on keyboard interrupt")
        play_audio(ERROR_SOUND)
    except Exception as error:
        print("An exception occurred:", type(error).__name__, ":", error)
        play_audio(ERROR_SOUND)

if __name__ == "__main__":
    main()
