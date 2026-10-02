from .huffman import (
    serialize_tree_binary,
    deserialize_tree_binary
)


def bits_to_bytes(bits):
    padding = (8 - len(bits) % 8) % 8
    bits += "0" * padding

    data = bytearray()

    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        data.append(int(byte, 2))

    return bytes(data), padding


def bytes_to_bits(data, padding):
    bits = ""

    for byte in data:
        bits += format(byte, "08b")

    if padding:
        bits = bits[:-padding]

    return bits



def save_compressed(data, padding, root, filename, compression_type):
    tree_data = b""

    if compression_type == 1:
        tree_data = serialize_tree_binary(root)

    tree_size = len(tree_data)

    with open(filename, "wb") as file:
        file.write(b"PP")
        file.write(bytes([1]))
        file.write(bytes([compression_type]))

        file.write(tree_size.to_bytes(4, "big"))
        file.write(bytes([padding]))

        file.write(tree_data)
        file.write(data)

def load_compressed(filename):
    with open(filename, "rb") as file:
        magic = file.read(2)

        if magic != b"PP":
            raise ValueError(
                "El archivo no es un archivo PiedPiper válido"
            )

        version = file.read(1)[0]

        if version != 1:
            raise ValueError(
                f"Versión no soportada: {version}"
            )

        compression_type = file.read(1)[0]

        tree_size = int.from_bytes(
            file.read(4),
            "big"
        )

        padding = file.read(1)[0]

        tree_data = file.read(tree_size)
        data = file.read()

    root = None

    if compression_type == 1:
        root, _ = deserialize_tree_binary(tree_data)

    return data, padding, root, compression_type