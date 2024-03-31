import os
import csv
from addresses import *
from memorylib import Dolphin

def append_data_to_csv(file_path, **kwargs) -> None:
    """Writes data to csv file."""

    # define header labels and check if file already exists
    default_headers = ['batter_id', 'batter_hand', 'pitcher_id', 'pitcher_hand', 'mound_loc', 'pitch_type', 'pitch_frames', 'curve_control_values']
    headers = default_headers + [key for key in kwargs.keys() if key not in default_headers]
    file_exists = os.path.isfile(file_path) and os.path.getsize(file_path) > 0

    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # If the file doesn't exist, write the header
        if not file_exists:
            writer.writeheader()

        row = {header: kwargs.get(header, '') for header in headers}

        # list of values is passed as a string joined by '+'. Makes transfer easier, and data is re-formatted when loaded
        # curve_control_values_str = '+'.join(map(str, input_list))
        if 'curve_control_values' in row and isinstance(row['curve_control_values'], list):
            row['curve_control_values'] = '+'.join(map(str, row['curve_control_values']))

        writer.writerow(row)

def load_data_from_csv(file_path):
    """Load data from csv file and split/reformat list data"""
    data = {}
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Skip header row
            for row in reader:
                pitcher_id = str(row[3])
                # split list into the original values
                curve_control_values = row[1].split('+')
                if pitcher_id not in data:
                    data[pitcher_id] = []
                data[pitcher_id].append(curve_control_values)
    except FileNotFoundError:
        print("File not found. Please make sure the file path is correct.")
    return data


def is_in_game():
    return dolphin.read_int8(in_game)