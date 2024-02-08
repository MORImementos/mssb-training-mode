import dolphin_memory_engine as dme
import memory_engine as me
import sys
import time
import csv
import os
import random
from addresses import *


def append_data_to_csv(file_path, pitcher_id, input_list: list) -> None:
    """Writes data to csv file."""

    # define header labels and check if file already exists
    header = ['pitcher_id', 'curve_control_values']
    file_exists = os.path.isfile(file_path) and os.path.getsize(file_path) > 0

    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # if file doesn't exist, the header will need to be written
        if not file_exists:
            writer.writerow(header)

        # list of values is passed as a string joined by '+'. Makes transfer easier, and data is re-formatted when loaded
        curve_control_values_str = '+'.join(map(str, input_list))
        row = [pitcher_id, curve_control_values_str]
        writer.writerow(row)


def load_data_from_csv(file_path):
    """Load data from csv file and split/reformat list data"""
    data = {}
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Skip header row
            for row in reader:
                pitcher_id = str(row[0])
                # split list into the original values
                curve_control_values = row[1].split('+')
                if pitcher_id not in data:
                    data[pitcher_id] = []
                data[pitcher_id].append(curve_control_values)
    except FileNotFoundError:
        print("File not found. Please make sure the file path is correct.")
    return data


def choose_random_pitch(data, pitcher_id):
    """Choose a random pitch from file matching pitcher id."""
    if str(pitcher_id) in data:
        return random.choice(data[str(pitcher_id)])
    else:
        print(f"No data found for pitcher ID {pitcher_id}.")
        return None


frame_rate = 60
file_path = 'pitch_data.csv'

# load file outside of loop to reduce number of file operations
data = load_data_from_csv(file_path)

# Initialize variables
input_list = []
pitch_state = "waiting"  # waiting/active/ended

while True:
    start_time = time.time()

    # counts down from pitch duration to 0. Is 0 when waiting
    active_pitch_frame = me.read_half_word(current_frame_of_pitch)

    # -1 when not pitching. When pitch is initiated, displays total frame count of the pitch
    pitch_duration = me.read_half_word(total_pitch_frames)
    curve_control = me.read_float(curve_input)
    pitcher_char_id = me.read_half_word(pitcher_char_id)
    pitch_type = me.read_byte(type_of_pitch)
    state = me.read_byte(pitch_state_indicator)
    mound_pos = me.read_float(pitcher_mound_pos_x)

    # need to handle when the ball is actually hit - what to do about the unfilled frames etc

    # Detect the start of a pitch
    if pitch_duration != -1 and pitch_state == "waiting" and pitch_duration == active_pitch_frame:
        pitch_state = "active"
        # used to track the index of the pitch input from the file
        pitch_index = 0

        # select random pitch to force
        random_pitch = choose_random_pitch(data, pitcher_char_id)

        input_list = []  # Reset the list for the new pitch

    # If a pitch is active, either append curve control values to list or write values
    if pitch_state == "active":
        # todo: better way to swap between reading and writing
        if random_pitch is not None:
            me.write_float(curve_input, float(random_pitch[pitch_index]))
        input_list.append(curve_control)
        pitch_index += 1
        # if 0 pitch is over
        if active_pitch_frame == 0:
            pitch_state = "ended"

    # Handle the end of a pitch
    if pitch_state == "ended":
        print(f"Pitch complete ({len(input_list)}f) curve control values:", input_list)
        # save input_list to a file here
        append_data_to_csv(file_path, pitcher_char_id, input_list)

        pitch_state = "waiting"  # Reset state to wait for the next pitch
        input_list = []  # Prepare for the next pitch

    # Handle pitch_duration reset to -1, indicating no active pitch. State == 4 is pitch has ended
    if pitch_duration == -1 and pitch_state != "waiting" and state == 4:
        pitch_state = "waiting"

    # Frame rate control to avoid overloading the CPU / we only need 60 fps anyway
    frame_time = time.time() - start_time
    delay = max(1 / frame_rate - frame_time, 0)
    time.sleep(delay)