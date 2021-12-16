

import dataclasses
import operator
from functools import reduce
from typing import *

def hex2bits(hex: str) -> str:
    return ''.join([HEX_MAP[char] for char in hex])


def read_hex() -> Dict[str, str]:
    with open('day16/hex_map.txt', 'r') as inputfile:
        return dict([tuple(line.strip('\n').split(' = ')) for line in inputfile.readlines()])


HEX_MAP = read_hex()


@dataclasses.dataclass
class Packet:
    version: int
    ptype: int

    def get_value(self) -> int:
        raise NotImplementedError
    

@dataclasses.dataclass
class Literal(Packet):
    value: int

    def get_value(self) -> int:
        return self.value


@dataclasses.dataclass
class Operator(Packet):
    info_bit: str
    packets: List[Packet]

    def get_value(self) -> int:
        match(self.ptype):
            case 0: func = operator.add
            case 1: func = operator.mul
            case 2: func = min
            case 3: func = max
            case 5: func = lambda acc, val: int(acc > val)
            case 6: func = lambda acc, val: int(acc < val)
            case 7: func = lambda acc, val: int(acc == val)
        return reduce(func, map(lambda p: p.get_value(), self.packets))


def parse_header(bits, i):
    return int(bits[i:i+3], 2), int(bits[i+3:i+6], 2), i+6

def parse_literal(bits, i):
    keepgoing = True
    value = ''
    while keepgoing:
        next_bits = bits[i:i+5]
        keepgoing = next_bits[0] == '1'
        value += next_bits[1:]
        i += 5
    return int(value, 2), i

def parse_info_bit(bits, i):
    return bits[i], i+1

def parse_operator_0(bits, i):
    content_length = int(bits[i:i+15], 2)
    i += 15
    return parse_bits(bits, i, max=i+content_length)

def parse_operator_1(bits, i):
    content_count = int(bits[i:i+11], 2)
    i += 11
    return parse_bits(bits, i, max_count=content_count)

def parse_bits(bits, i=0, max=None, max_count=None):
    parsed_packets = []
    while i < len(bits) and bits[i:] != '0'*len(bits[i:]):
        if (max is not None and i >= max):
            return parsed_packets, i
        if (max_count is not None and len(parsed_packets) == max_count):
            return parsed_packets, i
        version, ptype, i = parse_header(bits, i)
        if ptype == 4:
            value, i = parse_literal(bits, i)
            parsed_packets.append(Literal(version=version, ptype=ptype, value=value))
        else:
            info_bit, i = parse_info_bit(bits, i)
            if info_bit == '0':
                packets, i = parse_operator_0(bits, i)
            else:
                packets, i = parse_operator_1(bits, i)
            parsed_packets.append(Operator(version=version, ptype=ptype, packets=packets, info_bit=info_bit))
    return parsed_packets, i


def compute_total_version(packet):
    if isinstance(packet, Literal):
        return packet.version
    return packet.version + sum([compute_total_version(p) for p in packet.packets])


def run1(hex: str, expected: int) -> None:
    print(hex)
    packet = parse_bits(hex2bits(hex))[0][0]
    total = compute_total_version(packet)
    print(f'Total is {total}')
    assert total == expected

def run2(hex: str, expected: int) -> None:
    print(hex)
    packet = parse_bits(hex2bits(hex))[0][0]
    value = packet.get_value()
    print(f'Packet value is {value}')
    assert value == expected

def read_input(input_path: str) -> str:
    with open(f'day16/{input_path}', 'r') as inputfile:
        return inputfile.read().strip('\n')


if __name__ == '__main__':
    run1('8A004A801A8002F478', 16)
    run1('620080001611562C8802118E34', 12)
    run1('C0015000016115A2E0802F182340', 23)
    run1('A0016C880162017C3686B18A3D4780', 31)
    hex = read_input('input.txt')
    run1(hex, 981)

    run2('C200B40A82', 3)
    run2('04005AC33890', 54)
    run2('880086C3E88112', 7)
    run2('CE00C43D881120', 9)
    run2('D8005AC2A8F0', 1)
    run2('F600BC2D8F', 0)
    run2('9C005AC2F8F0', 0)
    run2('9C0141080250320F1802104A08', 1)
    run2(hex, 981)
