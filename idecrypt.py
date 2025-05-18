#!/bin/python3 

def load_and_process(filepath: str, output_path: str = "out.txt"):
    with open(filepath, "rb") as file:
        raw = memoryview(file.read())

    header_size = int.from_bytes(raw[:4], byteorder="little")
    payload = bytearray(raw[header_size * 4:])

    for idx in range(0, len(payload) - 1, 2):
        combined = int.from_bytes(payload[idx:idx+2], "little") ^ 0x01
        payload[idx:idx+2] = combined.to_bytes(2, "little")

    try:
        text = payload.decode("shift_jis")
    except UnicodeDecodeError:
        text = payload.decode("shift_jis", errors="replace")

    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(text)

if __name__ == "__main__":
    src = input("enter the path to the .id file: ").strip()
    dst = input("enter output file name (default: out.txt): ").strip()
    load_and_process(src, dst if dst else "out.txt")

