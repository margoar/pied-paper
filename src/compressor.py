from .huffman import (
    compress_bytes,
    decode_bytes,
    serialize_tree_binary
)

from .pp_format import (
    bits_to_bytes,
    bytes_to_bits,
    save_compressed,
    load_compressed,
    COMPRESSION_NONE,
    COMPRESSION_HUFFMAN
)


def compress_file(input_filename, output_filename):
    with open(input_filename, "rb") as file:
        data = file.read()

    encoded, root = compress_bytes(data)

    compressed_data, padding = bits_to_bytes(encoded)

    tree_data = serialize_tree_binary(root)

    huffman_size = (
        2 +  # magic
        1 +  # versión
        1 +  # tipo
        4 +  # tamaño árbol
        1 +  # padding
        len(tree_data) +
        len(compressed_data)
    )

    original_size = (
        2 +  # magic
        1 +  # versión
        1 +  # tipo
        4 +  # tamaño árbol
        1 +  # padding
        len(data)
    )

    if huffman_size < original_size:
        save_compressed(
            compressed_data,
            padding,
            root,
            output_filename,
            compression_type=COMPRESSION_HUFFMAN
        )
    else:
        save_compressed(
            data,
            0,
            root,
            output_filename,
            compression_type=COMPRESSION_NONE
        )

def decompress_file(input_filename, output_filename):
    data, padding, root, compression_type = load_compressed(
        input_filename
    )

    if compression_type == COMPRESSION_NONE:
        decoded = data
    else:
        bits = bytes_to_bits(data, padding)
        decoded = decode_bytes(bits, root)

    with open(output_filename, "wb") as file:
        file.write(decoded)