from dataclasses import dataclass
from helpers import determine_required_bits, calculate_mask


# bits required

metadata_fields = [
        ('pitcher', determine_required_bits(54)),
        ('pitcher_hand', determine_required_bits(2)),
        ('batter', determine_required_bits(54)),
        ('batter_hand', determine_required_bits(2)),
        ('inning', determine_required_bits(18)),
        ('balls', determine_required_bits(4)),
        ('strikes', determine_required_bits(3)),
        ('outs', determine_required_bits(3)),
        ('chem_links', determine_required_bits(4)),
        ('runners', [1, 1, 1]),  # each runner requires 1 bit
        ('stadium', determine_required_bits(7))
    ]


@dataclass
class PitchMetadata:
    pitcher: int # 0-53
    pitcher_hand: int # 0-1
    batter: int # 0-53
    batter_hand: int # 0-1
    inning: int # 0-18
    balls: int # 0-3
    strikes: int # 0-2
    outs: int # 0-2
    chem_links: int # 0-3
    runners: list  # 3 numbers, 0 for no runner, 1 for runner
    stadium: int # 0-6

    def __post_init__(self):
        pass # validate data to within a range


def pack_metadata(d: PitchMetadata, fields):
    """Pack metadata class into binary"""
    packed = 0
    shift_amount = 0
    for field_name, bits in reversed(fields):
        value = getattr(d, field_name)
        if isinstance(bits, list):
            for i, bit in enumerate(bits):
                packed |= (value[i] & calculate_mask(bit)) << shift_amount
                shift_amount += bit
        else:
            packed |= (value & calculate_mask(bits)) << shift_amount
            shift_amount += bits

    return packed


def unpack_metadata(d: PitchMetadata, fields):
    """Unpack metadata for parsing"""
    shift_amount = 0
    metadata_values = {}
    for field_name, bits in reversed(fields):
        if isinstance(bits, list):
            values = []
            for bit in bits:
                value = (packed >> shift_amount) & calculate_mask(bit)
                values.append(value)
                shift_amount += bit
            metadata_values[field_name] = values
        else:
            value = (packed >> shift_amount) & calculate_mask(bits)
            metadata_values[field_name] = value
            shift_amount += bits

    return PitchMetadata(**metadata_values)

if __name__ == "__main__":
    d = PitchMetadata(5, 1, 9, 1, 9, 4, 2, 2, 2, [1,0,1], 4)

    packed = pack_metadata(d, metadata_fields)
    print(f"Packed: {packed:08b}")
    print(f"Packed (hex): {packed:010x}")

    unpacked_metadata = unpack_metadata(packed, metadata_fields)
    print(f"Unpacked Metadata: {unpacked_metadata}")
    print(f"Original Metadata: {d}")
