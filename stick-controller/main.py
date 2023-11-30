import os
import time
import threading
import datetime
import busio
import digitalio
import board
import pygame
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

import websocket_server
import db_default

from config import configs
from words import get_word_by_position

print("configs:")
print(configs)

websocketPort = 8092

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)

pygame.mixer.init()

# Define grid layout and cell numbers
GRID = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

# Define stick position thresholds
GRID_BORDER_SIZE = float(configs["GRID_BORDER_SIZE"])
VREF = 3.3
POSITION_LOW = VREF * 0.33
POSITION_MEDIUM = VREF * 0.66
GRID_DEAD_ZONE = VREF * GRID_BORDER_SIZE / 2

print("Grid configuration:")
print("GRID_DEAD_ZONE: ", GRID_DEAD_ZONE)
print("POSITION_LOW: ", POSITION_LOW)
print("POSITION_MEDIUM: ", POSITION_MEDIUM)

SOURCE_DIR = os.path.dirname(__file__)
WORDS_SOUND_FILES_DIR = SOURCE_DIR + "/words/"

# Define filenames for stick routes
ROUTE_MAPPING_FILE = SOURCE_DIR + "/route_mapping.txt"

STARTUP_SOUND = SOURCE_DIR + "/sfx/startup.wav"
POWERDOWN_SOUND = SOURCE_DIR + "/sfx/powerdown.wav"
ERROR_SOUND = SOURCE_DIR + "/sfx/error.wav"

SLEEPING = False


def play_audio(file):
    sound = pygame.mixer.Sound(file)
    sound.set_volume(1)
    sound.play()


def get_cell(position):
    if position < POSITION_LOW - GRID_DEAD_ZONE:
        return 0
    elif (
        position < POSITION_MEDIUM - GRID_DEAD_ZONE
        and position > POSITION_LOW + GRID_DEAD_ZONE
    ):
        return 1
    elif position > POSITION_MEDIUM + GRID_DEAD_ZONE:
        return 2
    else:
        return -1


current_cell = 5


def getCurrentCell():
    return current_cell


def main():
    global SLEEPING
    global current_cell

    current_row = 1
    current_col = 1

    recorded_cells = []
    wait_for_reset = False

    cell_update_time = datetime.datetime.now()

    print("Starting loop")
    play_audio(STARTUP_SOUND)

    try:
        while True:
            if SLEEPING == True:
                sleepDuration = float(configs["STICK_CHECK_INTERVAL_SLEEP_MODE_S"])
            else:
                sleepDuration = float(configs["STICK_CHECK_INTERVAL_S"])
            time.sleep(sleepDuration)

            if (
                not SLEEPING
                and datetime.datetime.now()
                > cell_update_time
                + datetime.timedelta(minutes=float(configs["SLEEP_TIMEOUT_M"]))
            ):
                SLEEPING = True

            horizontal_position = chan1.voltage
            vertical_position = chan0.voltage

            new_row = get_cell(vertical_position)
            new_col = get_cell(horizontal_position)

            # dead zone check
            if new_row == -1 or new_col == -1:
                continue

            if new_row != current_row or new_col != current_col:
                current_row = new_row
                current_col = new_col
                cell_update_time = datetime.datetime.now()

                if SLEEPING:
                    SLEEPING = False

            current_cell = GRID[current_row][current_col]

            if wait_for_reset:
                if current_cell == "5":
                    wait_for_reset = False

                continue

            # end word
            if len(
                recorded_cells
            ) > 0 and datetime.datetime.now() > cell_update_time + datetime.timedelta(
                seconds=float(configs["END_WORD_TIMEOUT_S"])
            ):
                print("word positions:")
                print("".join(recorded_cells))

                # ignore the last position if it's 5
                if recorded_cells[-1] == "5":
                    recorded_cells = recorded_cells[:-1]

                # get file to play
                route_filename = get_word_by_position("".join(recorded_cells))
                if route_filename is not None:
                    print("Playing audio:", route_filename)
                    play_audio(WORDS_SOUND_FILES_DIR + route_filename)

                # reset state
                recorded_cells = []
                wait_for_reset = True

                continue

            # record cell change
            if datetime.datetime.now() > cell_update_time + datetime.timedelta(
                seconds=float(configs["CELL_CHANGE_DELAY_S"])
            ) or (
                # 5 is a special case, we want to be able to go over it quickly so it has it's own delay
                datetime.datetime.now()
                > cell_update_time
                + datetime.timedelta(
                    seconds=float(configs["MIDDLE_CELL_CHANGE_DELAY_S"])
                )
                and current_cell == "5"
            ):
                # we are in the middle, our starting position
                if len(recorded_cells) == 0 and current_cell == "5":
                    continue
                # if nothing changed, don't do anything
                if len(recorded_cells) > 0 and current_cell == recorded_cells[-1]:
                    continue

                # cell changed
                recorded_cells.append(current_cell)
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
    websocketServerThread = threading.Thread(
        target=websocket_server.startWebSocketServer, args=(websocketPort,)
    )
    websocketServerThread.start()

    main()
