import math

def determine_required_bits(possible_vals: int | list):
    # recieve either list or single integer and calculate bits needed to represent it. returns a list of tuples if list, where first num is original number, and second is the number of bits needed
    if isinstance(possible_vals, list):
        return [math.ceil(math.log2(i + 1)) for i in possible_vals]
    elif isinstance(possible_vals, int):
        return math.ceil(math.log2(possible_vals + 1))
    else:
        raise ValueError("Unsupported type.")
    
def calculate_mask(num_bits):
    if num_bits <= 0:
        raise ValueError("Number of bits must be greater than zero")
    return (1 << num_bits) - 1


def convert_int_to_byte(num, byte_order='big'):
    return num.to_bytes((num.bit_length() + 7) // 8 or 1, byteorder=byte_order)


def get_bits_and_mask(value):
    bits = determine_required_bits(value)
    mask = calculate_mask(bits)
    return bits, mask
