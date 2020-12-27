from itertools import repeat
from math import ceil

TABLE = "ABCDEFGHIJKLMNOPQRSTUWVXYZabcdefghijklmnopqrstuwvxyz0123456789-_"
REV_TABLE = dict(enumerate(list(TABLE)))
PICKUP_SIZES = list(repeat(36, 100))
PICKUP_SIZES_2 = list(repeat(37, 100))
ELEVATOR_SIZES = list(repeat(20, 20))
ELEVATOR_SIZES.append(21)


def compute_checksum(checksum_size, layout_number):
    if checksum_size == 0:
        return 0
    s = 0
    while layout_number > 0:
        quotient, remainder = divmod(layout_number, 1 << checksum_size)
        s = (s + remainder) % (1 << checksum_size)
        layout_number = quotient
    return s


def encode_layout(pickup_layout, elevator_layout=None):
    if elevator_layout is None:
        elevator_string = "qzoCAr2fwehJmRjM"
    else:
        elevator_string = encode_layout_inner(ELEVATOR_SIZES, 91, 5, elevator_layout)

    if 36 not in pickup_layout:
        pickup_string = encode_layout_inner(PICKUP_SIZES, 517, 5, pickup_layout)
    else:
        pickup_string = encode_layout_inner(PICKUP_SIZES_2, 521, 1, pickup_layout)

    if elevator_string != "qzoCAr2fwehJmRjM":
        return elevator_string + "." + pickup_string
    else:
        return pickup_string


def encode_layout_inner(sizes, layout_data_size, checksum_size, layout):
    num = 0
    for i, item_type in enumerate(layout):
        num = (num * sizes[i]) + item_type

    checksum = compute_checksum(checksum_size, num)
    num += (checksum << layout_data_size)
    even_bits = []
    odd_bits = []
    all_bits = list(str(bin(num))[2:])
    for i, bit in enumerate(all_bits):
        if i % 2:
            odd_bits.append(bit)
        else:
            even_bits.append(bit)

    odd_bits.reverse()
    all_bits = []

    for i in range(0, len(even_bits)):
        all_bits.append(even_bits[i])
        all_bits.append(odd_bits[i])

    num = int("".join(all_bits), 2)

    s = ""
    for i in range(0, ceil(layout_data_size / 6)):
        q, r = divmod(num, 64)
        num = q
        s += TABLE[r]

    return s


def item_list_to_layout_string(item_list):
    items = []
    for item in item_list:
        items.append(RANDOMPRIME_ITEM_INDEX[item])
    return encode_layout(items)


RANDOMPRIME_ITEM_INDEX = {
    "Missile Launcher": 0,
    "Missile Expansion": 0,
    "Energy Tank": 1,
    "Thermal Visor": 2,
    "X-Ray Visor": 3,
    "Varia Suit": 4,
    "Gravity Suit": 5,
    "Phazon Suit": 6,
    "Morph Ball": 7,
    "Boost Ball": 8,
    "Spider Ball": 9,
    "Morph Ball Bombs": 10,
    "Power Bomb Expansion": 11,
    "Power Bomb": 12,
    "Charge Beam": 13,
    "Space Jump Boots": 14,
    "Grapple Beam": 15,
    "Super Missile": 16,
    "Wavebuster": 17,
    "Ice Spreader": 18,
    "Flamethrower": 19,
    "Wave Beam": 20,
    "Ice Beam": 21,
    "Plasma Beam": 22,
    "Artifact of Lifegiver": 23,
    "Artifact of Wild": 24,
    "Artifact of World": 25,
    "Artifact of Sun": 26,
    "Artifact of Elder": 27,
    "Artifact of Spirit": 28,
    "Artifact of Truth": 29,
    "Artifact of Chozo": 30,
    "Artifact of Warrior": 31,
    "Artifact of Newborn": 32,
    "Artifact of Nature": 33,
    "Artifact of Strength": 34,
    "Nothing": 35,
    "Scan Visor": 36,
}


# test compute_checksum

def _test_layout_encode():
    pickup_layout = [
        "0",
        "0",
        "0",
        "1",
        "0",
        "7",
        "0",
        "0",
        "0",
        "1",
        "0",
        "0",
        "11",
        "17",
        "23",
        "0",
        "0",
        "1",
        "0",
        "0",
        "4",
        "24",
        "0",
        "13",
        "0",
        "0",
        "0",
        "0",
        "10",
        "0",
        "1",
        "1",
        "0",
        "25",
        "21",
        "0",
        "0",
        "26",
        "11",
        "0",
        "0",
        "20",
        "1",
        "8",
        "9",
        "0",
        "0",
        "16",
        "1",
        "27",
        "2",
        "0",
        "1",
        "0",
        "5",
        "0",
        "28",
        "11",
        "0",
        "14",
        "0",
        "0",
        "0",
        "29",
        "0",
        "0",
        "1",
        "0",
        "1",
        "0",
        "0",
        "3",
        "30",
        "0",
        "0",
        "15",
        "19",
        "31",
        "0",
        "0",
        "1",
        "0",
        "1",
        "6",
        "12",
        "0",
        "0",
        "0",
        "32",
        "0",
        "33",
        "0",
        "0",
        "1",
        "34",
        "18",
        "0",
        "11",
        "22",
        "1"
    ]

    elevator_layout = [
      "6",
      "14",
      "8",
      "10",
      "15",
      "18",
      "0",
      "19",
      "2",
      "16",
      "3",
      "12",
      "11",
      "17",
      "1",
      "4",
      "9",
      "13",
      "5",
      "7",
      "20"
    ]
    pickup_layout = [int(i) for i in pickup_layout]
    elevator_layout = [int(i) for i in elevator_layout]
    print(encode_layout(pickup_layout, elevator_layout))


_test_layout_encode()


