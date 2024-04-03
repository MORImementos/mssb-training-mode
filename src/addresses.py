FRAME_RATE = 60

### overall data ###
pitch_state_indicator = 0x80890AFE  # byte
in_game = 0x80892AB5  # byte
game_state = 0x80892aaa  # byte
has_control_of_pitch = 0x80890b12  # byte

### pitcher data ###
pitcher_id = 0x80890ADA  # halfword
pitcher_handedness = 0x80890B01  # byte 0 righty 1 lefty

### batter data ###
batter_id = 0x80890972  # halfword
batter_handedness = 0x8089098b  # byte 0 righty 1 lefty
batter_roster_id = 0x80890970  # halfword


### game state data ###
inning = 0x808928A0  # word
half_inning = 0x8089294D  # byte
home_score = 0x808928a4  # halfword
away_score = 0x808928ca  # halfword


### at bat data ###
strikes = 0x80892968  # word
balls = 0x8089296c  # word
outs = 0x80892970  # word
home_stars = 0x80892AD6  # byte
away_stars = 0x80892AD7  # byte
runners = 0x80892734  # halfword, maybe is byte array
chemistry_on_base = 0x80809BA  # byte

### pitch init data ###
pitcher_mound_pos_x = 0x80890A4C  # fl
# batter_pos_x = 0
# batter_pos_z = 0
# bat_pos_x = 0
# bat_pos_z = 0
# also use batter/bat pos x/z


### ai data ###
desired_mound_loc = 0x80892b18  # float
count_up_pitch_waiting = 0x80890ae0  # halfword

### pitch event data ###
pitch_duration = 0x80890AF4  # halfword
current_pitch_frame = 0x80890AF2  # halfword
curve_input = 0x80890A24  # float
pitch_type = 0x80890B21  # byte
charge_pitch_value = 0x80890aa0  # fl
controlling_pitch = 0x80890B12  # byte
ball_contact_pos_x = 0x80890934  # fl
ball_contact_pos_z = 0x8089093C  # fl
# batter_movement_input = 0
no_live_ball_indicator = 0x80890b14  # byte
batter_charge_up = 0x80890968  # fl
batter_charge_down = 0x8089096C  # fl
batter_swing = 0x8089099D  # bool byte
is_contact = 0x808909A1  # bool byte

# seems like i only need some of the following(?)
batter_pos_x = 0x80890910
batter_pos_z = 0x80890914
bat_pos_x = 0x8089095C
bat_pos_z = 0x80890964




### contact event data ###
contact_quality = 0x80890954
contact_type = 0x808909A2


# from memorylib import Dolphin
# class Address:
#     def __init__(self, addr, datatype, dolphin):
#         self.addr = addr
#         self.datatype = datatype
#         self.dolphin = dolphin
#
#     def read(self):
#         match self.datatype:
#             case 'float':
#                 return self.dolphin.read_float(self.addr)
#             case 'i8':
#                 return self.dolphin.read_int8(self.addr)
#             case 'u8':
#                 return self.dolphin.read_uint8(self.addr)
#             case 'i16':
#                 return self.dolphin.read_int16(self.addr)
#             case 'u16':
#                 return self.dolphin.read_uint16(self.addr)
#             case 'i32':
#                 return self.dolphin.read_int32(self.addr)
#             case 'u32':
#                 return self.dolphin.read_uint32(self.addr)
#     def write(self, val):
#         match self.datatype:
#             case 'float':
#                 self.dolphin.write_float(self.addr, val)
#             case 'i8':
#                 self.dolphin.write_int8(self.addr, val)
#             case 'u8':
#                 self.dolphin.write_uint8(self.addr, val)
#             case 'i16':
#                 self.dolphin.write_int16(self.addr, val)
#             case 'u16':
#                 self.dolphin.write_uint16(self.addr, val)
#             case 'i32':
#                 self.dolphin.write_int32(self.addr, val)
#             case 'u32':
#                 self.dolphin.write_uint32(self.addr, val)
