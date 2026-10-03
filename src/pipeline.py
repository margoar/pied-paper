from .lz77 import (
    compress,
    serialize_tokens,
    deserialize_tokens,
    decompress
)

from .huffman import (
    compress_bytes,
    decode_bytes
)

from .pp_format import (
    bits_to_bytes,
    bytes_to_bits
)


def compress_data(data):
    tokens = compress(data)

    serialized = serialize_tokens(tokens)

    encoded, root = compress_bytes(serialized)

    compressed_data, padding = bits_to_bytes(encoded)

    return compressed_data, padding, root


def decompress_data(compressed_data, padding, root):
    bits = bytes_to_bits(
        compressed_data,
        padding
    )

    serialized = decode_bytes(
        bits,
        root
    )

    tokens = deserialize_tokens(
        serialized
    )

    return decompress(tokens)