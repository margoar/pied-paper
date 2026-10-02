from collections import Counter

from src.huffman import build_tree, generate_codes, encode, decode


def test_compression_round_trip():
    text = "AAAAABBBCC"

    frequencies = Counter(text)
    root = build_tree(frequencies)
    codes = generate_codes(root)

    encoded = encode(text, codes)
    decoded = decode(encoded, root)

    assert decoded == text