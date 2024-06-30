from helpers import determine_required_bits, calculate_mask
import json
from typing import Dict, Any


""" format to allow for packing / unpacking:
- List of tuples (ordered by occurrence in bytes from high to low, where
    - first item in tuple is key in the json file
    - second is the maximum value to account; this is done so that the number of bits needed can be calculated
- Lists can be passed, but currently other objects cannot be passed as the second item. It is possible that I could add class support
"""
metadata_fields = [
        ('pitcher', 54),
        ('pitcher_hand', 2),
        ('batter', 54),
        ('batter_hand', 2),
        ('inning', 18),
        ('balls', 4),
        ('strikes', 3),
        ('outs', 3),
        ('chem_links', 4),
        ('runners', [1, 1, 1]),  # each runner requires 1 bit
        ('stadium', 7)
    ]


def json_to_packed_binary(d, fields):
    # load json file
    with open(d, 'r') as f:
        data = json.load(f)
    return data


def pack_data(data: Dict[str, Any], fields):
    packed = 0
    shift_amount = 0

    # for field_name, max_val in reversed(fields):
    for field_name, max_val in fields:

        value = data[field_name]
        bits = determine_required_bits(max_val)

        if isinstance(bits, list):
            for i, bit in enumerate(bits):
                packed |= (value[i] & calculate_mask(bit)) << shift_amount
                shift_amount += bit
        else:
            packed |= (value & calculate_mask(bits)) << shift_amount
            shift_amount += bits

    return packed

def unpack_data(packed_data: bytes, fields):
    packed = int.from_bytes(packed_data.to_bytes((packed_data.bit_length() + 7) // 8, byteorder='big'), byteorder='big')
    shift_amount = 0
    unpacked_data = {}

    # for field_name, max_val in reversed(fields):
    for field_name, max_val in fields:

        bits = determine_required_bits(max_val)        
        if isinstance(bits, list):
            values = []
            for bit in bits:
                value = (packed >> shift_amount) & calculate_mask(bit)
                values.append(value)
                shift_amount += bit
            unpacked_data[field_name] = values
        else:
            value = (packed >> shift_amount) & calculate_mask(bits)
            unpacked_data[field_name] = value
            shift_amount += bits

    return unpacked_data

if __name__ == "__main__":

    d = json_to_packed_binary('metadata.json', metadata_fields)
    print(d)
    packed = pack_data(d, metadata_fields)
    unpacked = unpack_data(packed, metadata_fields)
    print(unpacked)