from memorylib import Dolphin
import time
import random
from helpers import append_data_to_csv, load_data_from_csv
from addresses import *
def choose_random_pitch(data, pitcher_id):
    """Choose a random pitch from file matching pitcher id."""
    if str(pitcher_id) in data:
        return random.choice(data[str(pitcher_id)])
    else:
        print(f"No data found for pitcher ID {pitcher_id}.")
        return None


dolphin = Dolphin()


def is_in_game():
    return dolphin.read_int8(in_game)


prev_batter = None
active_pitch = False
pitch_list = []
input_list = []
prev_frame = -1
# data_dict = {
#     'inning_data': {
#         'half_inning': None,
#         'inning': None,
#     },
#     'at_bat_data': {
#         'chem_links_ob': None,
#         'runner_base_state': [0, 0, 0],
#     },
#     'pitch_data': {
#         'balls': None,
#         'strikes': None,
#         'outs': None,
#     },
#     'batting_team_score': None,
#     'pitching_team_score': None,
# }

bat_id, bat_hand, pitch_id, pitch_hand, pitch_pos_x, p_type = None, None, None, None, None, None

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
                    if dolphin.read_int16(batter_id) == prev_batter:
                        pass
                    else:
                        # assign vars
                        bat_id = dolphin.read_int16(batter_id)
                        bat_hand = dolphin.read_int8(batter_handedness)

                        # update batter so you don't get duplicates
                        prev_batter = dolphin.read_int16(batter_id)
                else:
                    # if true, pitch has started
                    if dolphin.read_int16(current_pitch_frame) == dolphin.read_int16(pitch_duration):
                        # assign vars
                        pitch_id = dolphin.read_int16(pitcher_id)
                        pitch_hand = dolphin.read_int8(pitcher_handedness)
                        pitch_pos_x = dolphin.read_float(pitcher_mound_pos_x)
                        p_type = dolphin.read_int8(pitch_type)
                        batter_x = dolphin.read_float(batter_pos_x)
                        batter_z = dolphin.read_float(batter_pos_z)
                        active_pitch = True

                    # pitch is ongoing, but not complete
                    if dolphin.read_int16(current_pitch_frame) != prev_frame and active_pitch:
                        # each frame of pitch, add to list
                        input_list.append(dolphin.read_float(curve_input))
                        prev_frame = dolphin.read_int16(current_pitch_frame)

                    # pitch is complete
                    if dolphin.read_int16(current_pitch_frame) == 0 and dolphin.read_int16(pitch_duration) != -1:
                        if active_pitch:
                            # in case for some reason all values aren't added, append 0.0s to list til right length
                            if len(input_list) != dolphin.read_int16(pitch_duration) + 1:
                                while len(input_list) != dolphin.read_int16(pitch_duration) + 1:
                                    input_list.append(0.0)

                            append_data_to_csv(
                                file_path='data/pitches.csv',
                                batter_id=bat_id,
                                batter_hand=bat_hand,
                                pitcher_id=pitch_id,
                                pitcher_hand=pitch_hand,  # Assuming 'right' or 'left'
                                mound_loc=pitch_pos_x,
                                pitch_type=p_type,
                                pitch_frames=len(input_list),  # If you need to record the number of frames
                                curve_control_values=input_list
                            )
                        active_pitch = False
                        input_list = []
                        pitch_list = []
                        prev_frame = -1



                # limit rate to game frame rate
                # frame_time = time.time() - start_time
                # delay = max(1 / FRAME_RATE - frame_time, 0)
                # time.sleep(delay)
    else:
        break