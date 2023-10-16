def read_to_end(input_stream):
    data = bytearray(b'')

    for chunk in input_stream.read():
        if not chunk:
            raise EOFError()
        data.append(chunk)

    return data
