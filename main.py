import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from pygame import mixer

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)

# def remap_range(value, left_min, left_max, right_min, right_max):
#     # this remaps a value from original (left) range to new (right) range
#     # Figure out how 'wide' each range is
#     left_span = left_max - left_min
#     right_span = right_max - right_min

#     # Convert the left range into a 0-1 range (int)
#     valueScaled = int(value - left_min) / int(left_span)

#     # Convert the 0-1 range into a value in the right range.
#     return int(right_min + (valueScaled * right_span))

# while True:
#     print('Raw ADC Value0: ', chan0.value)
#     print('ADC Voltage0: ' + str(chan0.voltage) + 'V')

#     print('Raw ADC Value1: ', chan1.value)
#     print('ADC Voltage1: ' + str(chan1.voltage) + 'V')

#     # we'll assume that the pot didn't move
#     # trim_pot_changed = False

#     # # read the analog pin
#     # trim_pot = chan0.value

#     # # how much has it changed since the last read?
#     # pot_adjust = abs(trim_pot - last_read)

#     # if pot_adjust > tolerance:
#     #     trim_pot_changed = True

#     # if trim_pot_changed:
#     #     # convert 16bit adc0 (0-65535) trim pot read into 0-100 volume level
#     #     set_volume = remap_range(trim_pot, 0, 65535, 0, 100)

#     #     # set OS volume playback volume
#     #     print('Volume = {volume}%' .format(volume = set_volume))
#     #     set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' \
#     #     .format(volume = set_volume)
#     #     os.system(set_vol_cmd)

#     #     # save the potentiometer reading for the next loop
#     #     last_read = trim_pot

#     # hang out and do nothing for a half second
#     time.sleep(0.5)

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

# Define filenames for stick routes
ROUTE_MAPPING_FILE = "route_mapping.txt"

# Define sleep duration
SLEEP_DURATION = 0.1

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
    
    try:
        while True:
            horizontal_position = chan1.voltage
            vertical_position = chan0.voltage
            
            new_row = get_cell(vertical_position)
            new_col = get_cell(horizontal_position)
            
            if new_row != current_row or new_col != current_col:
                current_row = new_row
                current_col = new_col
                if GRID[current_row][current_col] != "5":
                    recorded_cells.append(GRID[current_row][current_col])
                    print(recorded_cells)
            
            if GRID[current_row][current_col] == "5" and recorded_cells:
                print(recorded_cells)
                print("-".join(recorded_cells))
                route_filename = route_to_filename.get("".join(recorded_cells))
                if route_filename:
                    print("Playing audio:", route_filename)
                    play_audio(route_filename)
                recorded_cells = []
            
            time.sleep(SLEEP_DURATION)  # Adjust sleep duration as needed
            
    except KeyboardInterrupt:
        print("Exiting on keyboard interrupt")
    except:
        print("Something went wrong")

if __name__ == "__main__":
    main()
