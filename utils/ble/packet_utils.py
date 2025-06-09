# packet_utils.py

import struct
from typing import List

MAX_DATA_LENGTH = 120  # 最大数据长度


def json_to_binary_packets(json_string: str, command: int) -> List[bytes]:
    json_bytes = json_string.encode("utf-8")
    total_packages = (len(json_bytes) + MAX_DATA_LENGTH - 1) // MAX_DATA_LENGTH
    packets = []

    for i in range(total_packages):
        offset = i * MAX_DATA_LENGTH
        chunk = json_bytes[offset : offset + MAX_DATA_LENGTH]
        data_length = len(chunk)

        # 构建数据包头部
        frame_header = 0xAA55  # 示例帧头
        version = 1
        package_number = i + 1
        total_packages_byte = total_packages
        data_length_byte = data_length
        padding = 0

        header = struct.pack(
            "<H6B",
            frame_header,
            version,
            command,
            package_number,
            total_packages_byte,
            data_length_byte,
            padding,
        )

        packet = header + chunk
        packets.append(packet)

    return packets


def parse_packet(packet: bytes):
    if len(packet) < 8:
        raise ValueError("数据包长度不足8字节")

    header_bytes = packet[:8]
    (
        frame_header,
        version,
        command,
        package_number,
        total_packages,
        data_length,
        padding,
    ) = struct.unpack("<H6B", header_bytes)

    data = packet[8 : 8 + data_length]

    return {
        "frame_header": frame_header,
        "version": version,
        "command": command,
        "package_number": package_number,
        "total_packages": total_packages,
        "data_length": data_length,
        "padding": padding,
        "data": data,
    }
