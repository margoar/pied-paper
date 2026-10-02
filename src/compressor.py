from .huffman import (
    compress_bytes,
    decode_bytes
)

from .pp_format import (
    bits_to_bytes,
    bytes_to_bits,
    save_compressed,
    load_compressed
)


def compress_file(input_filename, output_filename):
    with open(input_filename, "rb") as file:
        data = file.read()

    encoded, root = compress_bytes(data)

    compressed_data, padding = bits_to_bytes(encoded)

    save_compressed(
        compressed_data,
        padding,
        root,
        output_filename
    )


def decompress_file(input_filename, output_filename):
    data, padding, root = load_compressed(input_filename)

    bits = bytes_to_bits(data, padding)

    decoded = decode_bytes(bits, root)

    with open(output_filename, "wb") as file:
        file.write(decoded)