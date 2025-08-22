#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用 Protobuf 解码工具 (无 .proto 文件也能解析)
支持 base64 / 二进制文件输入，输出 JSON 格式结果
"""

import base64, io, json, argparse
from datetime import datetime, timezone, timedelta


def read_varint(stream: io.BytesIO) -> int:
    """Decode a protobuf varint from the current stream position."""
    shift = 0
    result = 0
    while True:
        b = stream.read(1)
        if not b:
            raise EOFError("Unexpected EOF while reading varint")
        b = b[0]
        result |= ((b & 0x7F) << shift)
        if not (b & 0x80):
            break
        shift += 7
        if shift > 70:
            raise ValueError("Varint too long / corrupted")
    return result


def bytes_pretty(b: bytes):
    """Return a human-readable representation for raw bytes."""
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return {"base64": base64.b64encode(b).decode("ascii")}


def parse_protobuf_unknown(data: bytes):
    """
    Generic protobuf parser (no .proto schema).
    Returns a list of dicts: [{field, wire_type, value}, ...]
    """
    out = []
    stream = io.BytesIO(data)

    while True:
        key_b = stream.read(1)
        if not key_b:
            break  # EOF
        key = key_b[0]
        field_number = key >> 3
        wire_type = key & 0x7

        if wire_type == 0:      # varint
            value = read_varint(stream)
        elif wire_type == 1:    # 64-bit
            raw = stream.read(8)
            value = {"hex": raw.hex()}
        elif wire_type == 2:    # length-delimited
            length = read_varint(stream)
            raw = stream.read(length)
            value = bytes_pretty(raw)
        elif wire_type == 5:    # 32-bit
            raw = stream.read(4)
            value = {"hex": raw.hex()}
        else:
            value = None

        out.append({"field": field_number, "wire_type": wire_type, "value": value})
    return out


def ms_to_dt(ms):
    """Try to convert ms timestamp to readable UTC/JST times."""
    if isinstance(ms, int) and 10**12 <= ms <= 10**14:
        dt_utc = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
        dt_jst = dt_utc.astimezone(timezone(timedelta(hours=9)))
        return {"utc": dt_utc.isoformat(), "jst": dt_jst.isoformat()}
    return None


def decode_payload(data: bytes):
    parsed_list = parse_protobuf_unknown(data)
    raw_map = {str(item["field"]): item["value"] for item in parsed_list}

    # Example mapping guess (可按项目实际修改)
    friendly = {
        "objDevId": raw_map.get("1"),
        "type_or_code": raw_map.get("2"),
        "start_ms": raw_map.get("4"),
        "expire_ms": raw_map.get("5"),
        "flag1": raw_map.get("6"),
        "flag2": raw_map.get("7"),
        "access_key": raw_map.get("8"),
        "secret_key_part": raw_map.get("9"),
        "endpoint": raw_map.get("10"),
        "region": raw_map.get("11"),
        "bucket": raw_map.get("12"),
        "vendor": raw_map.get("13"),
    }

    friendly_times = {
        "start_time": ms_to_dt(friendly["start_ms"]),
        "expire_time": ms_to_dt(friendly["expire_ms"]),
    }

    return {
        "raw_fields": parsed_list,
        "raw_map": raw_map,
        "friendly_guess": friendly,
        "friendly_times": friendly_times,
    }


def main():
    parser = argparse.ArgumentParser(description="通用 Protobuf 解码工具 (无 .proto)")
    parser.add_argument("--base64", help="输入 base64 字符串")
    parser.add_argument("--file", help="输入二进制文件路径")
    parser.add_argument("--out", help="输出 JSON 文件路径", default=None)
    args = parser.parse_args()

    # if args.base64:
    #     data = base64.b64decode(args.base64)
    # elif args.file:
    #     with open(args.file, "rb") as f:
    #         data = f.read()
    # else:
    #     parser.error("必须提供 --base64 或 --file 参数")
    data = base64.b64decode("ChNkLThkOGI0NzY4LW5zNmFvaTY2EgExIOLSuraMMyjiqv/zgTQwATgeQhRBS0lBWk9XTEJaV0xXWENOSk03NUooeDA0T1VkSUx0YWFmS3E0VTZYeXBNY3IzWUlQb3NHUWNVME0vQ3FZeFIaczMudXMtd2VzdC0xLmFtYXpvbmF3cy5jb21aCXVzLXdlc3QtMWIJdXN2aWRlbzMwagNhd3M=")
    result = decode_payload(data)
    text = json.dumps(result, ensure_ascii=False, indent=2)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[+] 解析结果已保存到 {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
