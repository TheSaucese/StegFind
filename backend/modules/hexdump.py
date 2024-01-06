def hexdump(file_path, bytes_per_line=16):
    hexdump_str = ""
    with open(file_path, 'rb') as file:
        offset = 0
        while True:
            chunk = file.read(bytes_per_line)
            if not chunk:
                break

            # Convert chunk to hex and pad it to ensure even length
            hex_chunk = ' '.join(f"{byte:02x}" for byte in chunk).ljust(bytes_per_line * 3)

            # Convert non-printable chars to '.', and decode bytes to ASCII for printable chars
            ascii_text = ''.join(chr(byte) if 32 <= byte < 127 else '.' for byte in chunk)

            # Append formatted line to hexdump_str
            hexdump_str += f"{offset:08x}  {hex_chunk} |{ascii_text}|\n"

            offset += bytes_per_line

    return hexdump_str
