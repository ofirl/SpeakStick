import sys

sys.path.append("/opt/SpeakStick")  # Adds higher directory to python modules path.

import monitoring.logs_config

monitoring.logs_config.init_logger("stick-controller")

import logging
import os
import time
import threading
import datetime
import math
import busio
import digitalio
import board
import pygame
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

import websocket_server
import db_default
import globals

from config import configs
from words import get_word_by_position

logging.info("configs dump", extra={"configs": configs})

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

VREF = 3.3

SOURCE_DIR = os.path.dirname(__file__)
WORDS_SOUND_FILES_DIR = SOURCE_DIR + "/words/"

# Define filenames for stick routes
ROUTE_MAPPING_FILE = SOURCE_DIR + "/route_mapping.txt"

STARTUP_SOUND = SOURCE_DIR + "/sfx/startup.wav"
POWERDOWN_SOUND = SOURCE_DIR + "/sfx/powerdown.wav"
ERROR_SOUND = SOURCE_DIR + "/sfx/error.wav"

SLEEPING = False


def play_audio(file):
    if (not os.path.exists(file) or not os.path.isfile(file)) and file != ERROR_SOUND:
        play_audio(ERROR_SOUND)
        return

    sound = pygame.mixer.Sound(file)
    sound.set_volume(0)
    sound.play()


side_length = float(configs["MIDDLE_CELL_OCTAGON_SIDE_LENGTH"])

# Calculate the radius from the center to a vertex
radius = side_length / math.sqrt(2 - math.sqrt(2))

# Calculate the angles corresponding to the octagon vertices
angles = [i * (2 * math.pi / 8) for i in range(8)]

# Define the center coordinates of the octagon
center_x, center_y = 0.5, 0.5


def is_inside_octagon(x, y):
    # Check if the point is to the left of all lines formed by consecutive vertices
    for i in range(8):
        x1 = radius * math.cos(angles[i])
        y1 = radius * math.sin(angles[i])
        x2 = radius * math.cos(angles[(i + 1) % 8])
        y2 = radius * math.sin(angles[(i + 1) % 8])

        if (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1) <= 0:
            return False

    return True


def get_cell_number(xAbs, yAbs):
    x = xAbs / VREF
    y = yAbs / VREF

    # Check if the coordinates are within the octagon
    if is_inside_octagon(x - center_x, y - center_y):
        # if abs(x - center_x) + abs(y - center_y) <= 0.33:
        return "5"  # Center cell

    # Determine the quadrant
    if x <= center_x - 0.15:
        if y <= center_y - 0.15:
            return "1"  # Bottom-left cell
        elif y >= center_y + 0.15:
            return "7"  # Top-left cell
        else:
            return "4"  # Middle-left cell
    elif x >= center_x + 0.15:
        if y <= center_y - 0.15:
            return "3"  # Bottom-right cell
        elif y >= center_y + 0.15:
            return "9"  # Top-right cell
        else:
            return "6"  # Middle-right cell
    else:
        if y <= center_y - 0.15:
            return "2"  # Bottom-middle cell
        elif y >= center_y + 0.15:
            return "8"  # Top-middle cell
        else:
            return "5"  # center cell


def send_stick_event(event):
    globals.stick_events.put_nowait(event)


def main():
    global SLEEPING

    recorded_cells = []
    wait_for_reset = False

    cell_update_time = datetime.datetime.now()

    logging.info("Starting loop")
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

            new_current_cell = get_cell_number(horizontal_position, vertical_position)

            if new_current_cell != globals.current_cell:
                cell_update_time = datetime.datetime.now()

                if SLEEPING:
                    SLEEPING = False

            globals.current_cell = new_current_cell

            if wait_for_reset:
                if globals.current_cell == "5":
                    wait_for_reset = False

                continue

            # end word
            if len(
                recorded_cells
            ) > 0 and datetime.datetime.now() > cell_update_time + datetime.timedelta(
                seconds=float(configs["END_WORD_TIMEOUT_S"])
            ):
                logging.debug(
                    "word ended", extra={"positions": "".join(recorded_cells)}
                )
                send_stick_event(
                    {"type": "wordEnded", "value": "".join(recorded_cells)}
                )

                # ignore the last position if it's 5
                if recorded_cells[-1] == "5":
                    recorded_cells = recorded_cells[:-1]

                # get file to play
                route_filename = get_word_by_position("".join(recorded_cells))
                if route_filename is not None:
                    logging.info("Playing audio", extra={"file": route_filename})
                    send_stick_event({"type": "playingWord", "value": route_filename})
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
                and globals.current_cell == "5"
            ):
                # we are in the middle, our starting position
                if len(recorded_cells) == 0 and globals.current_cell == "5":
                    continue
                # if nothing changed, don't do anything
                if (
                    len(recorded_cells) > 0
                    and globals.current_cell == recorded_cells[-1]
                ):
                    continue

                # cell changed
                recorded_cells.append(globals.current_cell)
                send_stick_event({"type": "cellChange", "value": globals.current_cell})
                cell_update_time = datetime.datetime.now()
                logging.debug(
                    "recorded new position", extra={"recorded_cells": recorded_cells}
                )

    except KeyboardInterrupt:
        logging.info("Exiting on keyboard interrupt")
        play_audio(ERROR_SOUND)
    except Exception as error:
        logging.exception("An exception occurred")
        play_audio(ERROR_SOUND)


if __name__ == "__main__":
    websocketServerThread = threading.Thread(
        target=websocket_server.startWebSocketServer, args=(websocketPort,)
    )
    websocketServerThread.start()

    main()
