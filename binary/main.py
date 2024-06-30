from dataclasses import dataclass, asdict
from helpers import calculate_mask, determine_required_bits
import struct
import json

"""
Structure of the file:
some byte prefix
gameid
player name
player name
PitchMetadata
PitchData:
    Mound location
    Pitch Type
    Pitch length
    PitchData (input)

This currently assumes that finding and using the -1, 0, 1 pitch inputs will be doable. Otherwise, it might require the larger storage. Or, to save storage, I could lookup the curve control values for a given character and convert that way.
"""


pitch_fields = [
    ('pitch_type', determine_required_bits(5)),
    ('pitch_length', determine_required_bits(70)),
]


@dataclass
class PitchData:
    mound_location: float
    pitch_type: int
    pitch_length: int
    pitch_input: list


def encode_pitch_input(value):
    encoded_value = 0
    for i, v in enumerate(value):
        if v == 0:
            encoded_value |= (0b00 << (2 * i))
        elif v == 1:
            encoded_value |= (0b01 << (2 * i))
        elif v == -1:
            encoded_value |= (0b11 << (2 * i))
        else:
            raise ValueError("Invalid pitch input value.")
    return encoded_value
    

def decode_pitch_input(bits, length):
    decoded_values = []
    for i in range(length):
        value = (bits >> (2 * i)) & 0b11
        if value == 0b00:
            decoded_values.append(0)
        elif value == 0b01:
            decoded_values.append(1)
        elif value == 0b11:
            decoded_values.append(-1)
        else:
            raise ValueError("Invalid bits for pitch input.")
    return decoded_values


def pack_data(d: PitchData, fields):
    """Pack pitch data class into binary"""
    packed = 0
    shift_amount = 0
    for field_name, bits in reversed(fields):
        value = getattr(d, field_name)
        packed |= (value & calculate_mask(bits)) << shift_amount
        shift_amount += bits
    pitch_input_encoded = encode_pitch_input(d.pitch_input)
    packed |= (pitch_input_encoded & calculate_mask(2 * d.pitch_length)) << shift_amount
    shift_amount += 2 * d.pitch_length

    mound_location_packed = struct.pack('f', d.mound_location)
    packed_bytes = packed.to_bytes((shift_amount + 7) // 8, byteorder='big')
    return mound_location_packed + packed_bytes

def unpack_data(packed_data: bytes, fields):
    """Unpack pitch data to a readable form"""
    mound_location = struct.unpack('f', packed_data[:4])[0]
    packed = int.from_bytes(packed_data[4:], byteorder='big')
    shift_amount = 0
    unpacked_data = {'mound_location': mound_location}

    for field_name, bits in reversed(fields):
        value = (packed >> shift_amount) & calculate_mask(bits)
        unpacked_data[field_name] = value
        shift_amount += bits

    pitch_length = unpacked_data['pitch_length']
    pitch_input_bits = (packed >> shift_amount) & calculate_mask(2 * pitch_length)
    unpacked_data['pitch_input'] = decode_pitch_input(pitch_input_bits, pitch_length)

    return PitchData(**unpacked_data)


def packed_binary_to_json(packed_data, fields):
    unpacked_data = unpack_data(packed_data, fields)
    return json.dumps(unpacked_data, indent=2)


if __name__ == "__main__":
   # in theory these two shouldn't exist in pitch data and should be safe, but should reevaluate later
    pitch_file_prefix = 99
    pitch_data_prefix = 98
    
    p_input = [1, 0, -1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, -1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    pitch_data = PitchData(2.3, 2, len(p_input), p_input)

    packed = pack_data(pitch_data, pitch_fields)
    print(f"Packed: {packed.hex()}")

    with open("pitch_data.bin", "wb") as f:
        f.write(packed)

    with open("pitch_data.bin", "rb") as f:
        packed_from_file = f.read()

    unpacked = unpack_data(packed_from_file, pitch_fields)
    print(f"Unpacked: {unpacked}")

    unpacked_dict = asdict(unpacked)
    unpacked_json = json.dumps(unpacked_dict, indent=2)
    print(f"Unpacked JSON: {unpacked_json}")

    with open("unpacked_pitch.json", "w") as f:
        f.write(unpacked_json)