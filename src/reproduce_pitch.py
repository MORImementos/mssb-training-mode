from memorylib import Dolphin
import pandas as pd
from addresses import *
from helpers import is_in_game

df = pd.read_csv("data/pitches.csv")


def choose_random_pitch(data, pitcher_id, pitch_type, pitch_duration):
    df = data[(data['pitcher_id'] == pitcher_id) & (data['pitch_type'] == pitch_type) & (data['pitch_frames'] >= pitch_duration)]
    if not df.empty:
        selected_row = df.sample(n=1)

        selected_data = selected_row.iloc[0].to_dict()
        selected_data['curve_control_values'] = [float(value) for value in
                                                 selected_data['curve_control_values'].split('+')]

        return selected_data
    else:
        return None


dolphin = Dolphin()

prev_batter = None
active_pitch = False
pitch_list = []
input_list = []
prev_frame = -1
pitch = None
current_pitch_data = {}
# todo: filter for replay

# main loop
while True:
    # check dolphin is running
    if dolphin.hook():
        # check actually in game
        if is_in_game():
            print('in game.')
            while True:
                # between half inning transitions
                if dolphin.read_int8(game_state) == 3:
                    pass
                # pitch has not started
                elif dolphin.read_int16(pitch_duration) == -1:
                    # if still on same batter, don't update batter info
                    if dolphin.read_int8(batter_id) == prev_batter:
                        pass
                    else:
                        pass

                else:
                    # if true, pitch has started
                    if dolphin.read_int16(current_pitch_frame) == dolphin.read_int16(pitch_duration):
                        # rough attempt to overwrite the ai intended mound position - will need to better refine it later
                        if dolphin.read_int16(count_up_pitch_waiting) > 30:
                            pitch = choose_random_pitch(df, dolphin.read_int8(pitcher_id),
                                                        dolphin.read_int8(pitch_type), dolphin.read_int16(pitch_duration))
                            dolphin.write_float(desired_mound_loc, pitch['mound_loc'])

                        if pitch:
                            # overwrite pitch type
                            if pitch['pitch_type'] != dolphin.read_int8(pitch_type):
                                dolphin.write_int8(pitch_type, pitch['pitch_type'])

                        # indicate ongoing pitch
                        active_pitch = True

                    # pitch is ongoing, but not complete
                    if dolphin.read_int16(current_pitch_frame) != prev_frame and active_pitch:
                        # if list is not empty, pop from array
                        if len(pitch['curve_control_values']) >= 1:
                            dolphin.write_float(curve_input, pitch['curve_control_values'].pop(0))

                    # pitch is complete
                    if dolphin.read_int16(current_pitch_frame) == 0 and dolphin.read_int16(pitch_duration) != -1:
                        # reset for next pitch
                        active_pitch = False
                        input_list = []
                        pitch_list = []
                        prev_frame = -1
                        pitch = None

    else:
        break
