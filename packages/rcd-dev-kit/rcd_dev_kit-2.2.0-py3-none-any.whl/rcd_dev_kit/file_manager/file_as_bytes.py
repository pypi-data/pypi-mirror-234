def read_file_as_bytes_array(file_path: str, buffsize: int = 8 * 1024) -> bytes:
    bytes_str = bytearray()
    with open(file_path, 'rb') as fp:
        while True:
            file_buffer = fp.read(buffsize)
            if not file_buffer:
                break
            bytes_str.extend(file_buffer)
    return bytes(bytes_str)