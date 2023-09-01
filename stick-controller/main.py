import os
import time
import datetime
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from pygame import mixer

import db_default

from config import configs
from words import get_word_by_position

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
GRID_BORDER_SIZE = 0.1
VREF = 3.3
POSITION_LOW = VREF * 0.33
POSITION_MEDIUM = VREF * 0.66
GRID_DEAD_ZONE = VREF * GRID_BORDER_SIZE / 2

SOURCE_DIR = os.path.dirname(__file__)
WORDS_SOUND_FILES_DIR = SOURCE_DIR + "/words/"

# Define filenames for stick routes
ROUTE_MAPPING_FILE = SOURCE_DIR + "/route_mapping.txt"

STARTUP_SOUND = SOURCE_DIR + "/sfx/startup.wav"
POWERDOWN_SOUND = SOURCE_DIR + "/sfx/powerdown.wav"
ERROR_SOUND = SOURCE_DIR + "/sfx/error.wav"

def play_audio(file):
    sound = mixer.Sound(file)
    sound.play()

def get_cell(position):
    if position < POSITION_LOW - GRID_DEAD_ZONE:
        return 0
    elif position < POSITION_MEDIUM - GRID_DEAD_ZONE and position > POSITION_LOW + GRID_DEAD_ZONE:
        return 1
    elif position > POSITION_MEDIUM + GRID_DEAD_ZONE:
        return 2
    else:
        return -1

def main():
    current_row = 1
    current_col = 1
    recorded_cells = []
    wait_for_reset = False
    
    cell_update_time = datetime.datetime.now()

    print("Starting loop")
    play_audio(STARTUP_SOUND)
# loop hangs.....
    try:
        while True:
            time.sleep(float(configs["SLEEP_DURATION_S"]))
            horizontal_position = chan1.voltage
            vertical_position = chan0.voltage
            
            new_row = get_cell(vertical_position)
            new_col = get_cell(horizontal_position)
            # dead zone check
            if new_row == -1 or new_col == -1:
                print("dead zone")
                continue
            
            if new_row != current_row or new_col != current_col:
                current_row = new_row
                current_col = new_col
                cell_update_time = datetime.datetime.now()
            
            if wait_for_reset:
                if current_col == "1" and current_row == "1":
                    print("reset")
                    wait_for_reset = False

                continue

            # end word
            if (len(recorded_cells) > 0 and datetime.datetime.now() > cell_update_time + datetime.timedelta(seconds=float(configs["END_WORD_TIMEOUT_S"]))):
                print("word positions:")
                print("".join(recorded_cells))

                route_filename = get_word_by_position("".join(recorded_cells))
                if route_filename != None:
                    print("Playing audio:", route_filename)
                    play_audio(WORDS_SOUND_FILES_DIR + route_filename)
                recorded_cells = []
                wait_for_reset = True

                continue

            # record cell change
            if datetime.datetime.now() > cell_update_time + datetime.timedelta(seconds=float(configs["CELL_CHANGE_DELAY_S"])):
                # we are in the middle, our starting position
                if len(recorded_cells) == 0 and GRID[current_row][current_col] == "5":
                    continue
                # if nothing changed, don't do anything
                if len(recorded_cells) > 0 and GRID[current_row][current_col] == recorded_cells[-1]:
                    continue

                recorded_cells.append(GRID[current_row][current_col])
                cell_update_time = datetime.datetime.now()
                print("record new position:")
                print(recorded_cells)
            
    except KeyboardInterrupt:
        print("Exiting on keyboard interrupt")
        play_audio(ERROR_SOUND)
    except Exception as error:
        print("An exception occurred:", type(error).__name__, ":", error)
        play_audio(ERROR_SOUND)

if __name__ == "__main__":
    main()
