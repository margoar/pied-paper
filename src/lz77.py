def compress(data, window_size=4096, lookahead_size=255):
    result = []

    i = 0

    while i < len(data):
        start = max(0, i - window_size)

        window = data[start:i]
        lookahead = data[i:i + lookahead_size]

        best_distance = 0
        best_length = 0

        for j in range(len(window)):
            length = 0

            while (
                length < len(lookahead)
                and j + length < len(window)
                and window[j + length] == lookahead[length]
            ):
                length += 1

            if length > best_length:
                best_length = length
                best_distance = len(window) - j

        if best_length >= 3:
            result.append(
                ("match", best_distance, best_length)
            )

            i += best_length
        else:
            result.append(
                ("literal", data[i])
            )

            i += 1

    return result


def decompress(tokens):
    result = bytearray()

    for token in tokens:
        if token[0] == "literal":
            result.append(token[1])
            continue

        _, distance, length = token

        start = len(result) - distance

        for i in range(length):
            result.append(result[start + i])

    return bytes(result)

def compress_file(input_filename):
    with open(input_filename, "rb") as file:
        data = file.read()

    return compress(data)


def decompress_file(tokens, output_filename):
    data = decompress(tokens)

    with open(output_filename, "wb") as file:
        file.write(data)

def serialize_tokens(tokens):
    data = bytearray()

    for token in tokens:
        if token[0] == "literal":
            data.append(0)
            data.append(token[1])

        else:
            _, distance, length = token

            data.append(1)
            data.extend(distance.to_bytes(2, "big"))
            data.append(length)

    return bytes(data)


def deserialize_tokens(data):
    tokens = []
    i = 0

    while i < len(data):
        token_type = data[i]
        i += 1

        if token_type == 0:
            value = data[i]
            i += 1

            tokens.append(("literal", value))

        elif token_type == 1:
            distance = int.from_bytes(
                data[i:i + 2],
                "big"
            )
            i += 2

            length = data[i]
            i += 1

            tokens.append(
                ("match", distance, length)
            )

        else:
            raise ValueError("Token LZ77 inválido")

    return tokens