from .huffman import (
    compress_bytes,
    decode_bytes,
    serialize_tree_binary,
)
from .pipeline import compress_data, decompress_data
from .pp_format import (
    COMPRESSION_LZ77_HUFFMAN,
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

def get_compression_stats(input_filename, output_filename):
    with open(input_filename, "rb") as file:
        original_size = len(file.read())

    with open(output_filename, "rb") as file:
        compressed_size = len(file.read())

    savings = (
        (1 - compressed_size / original_size) * 100
    )

    return {
        "original_size": original_size,
        "compressed_size": compressed_size,
        "savings": savings
    }

def get_format_stats(filename):
    with open(filename, "rb") as file:
        magic = file.read(2)
        version = file.read(1)
        compression_type = file.read(1)

        tree_size = int.from_bytes(
            file.read(4),
            "big"
        )

        padding = file.read(1)

        tree_data = file.read(tree_size)
        data = file.read()

    return {
        "header_size": 9,
        "tree_size": len(tree_data),
        "data_size": len(data),
        "total_size": (
            9
            + len(tree_data)
            + len(data)
        ),
        "compression_type": compression_type[0],
        "padding": padding[0]
    }

def compress_file_lz77(input_filename, output_filename):
    with open(input_filename, "rb") as file:
        data = file.read()

    compressed_data, padding, root = compress_data(data)

    save_compressed(
        compressed_data,
        padding,
        root,
        output_filename,
        compression_type=COMPRESSION_LZ77_HUFFMAN
    )

def decompress_file_lz77(input_filename, output_filename):
    data, padding, root, compression_type = load_compressed(
        input_filename
    )

    if compression_type != COMPRESSION_LZ77_HUFFMAN:
        raise ValueError(
            "El archivo no usa LZ77 + Huffman"
        )

    decoded = decompress_data(
        data,
        padding,
        root
    )

    with open(output_filename, "wb") as file:
        file.write(decoded)