from collections import Counter
from src.huffman import build_tree, decompress, generate_codes, encode, decode,compress

def test_compression_round_trip():
    text = "AAAAABBBCC"

    frequencies = Counter(text)
    root = build_tree(frequencies)
    codes = generate_codes(root)

    encoded = encode(text, codes)
    decoded = decode(encoded, root)

    assert decoded == text

def test_compression_with_repeated_text():
    text = "AAAAABBBBBCCCCCDDDDDEEEEE" * 100

    frequencies = Counter(text)
    root = build_tree(frequencies)
    codes = generate_codes(root)

    encoded = encode(text, codes)
    decoded = decode(encoded, root)

    assert decoded == text
    assert len(encoded) < len(text) * 8

def test_compression_with_normal_text():
    text = "Hola, este es un texto de prueba."

    frequencies = Counter(text)
    root = build_tree(frequencies)
    codes = generate_codes(root)

    encoded = encode(text, codes)
    decoded = decode(encoded, root)

    assert decoded == text

def test_compress_and_decompress_file(tmp_path):
    text = "Pied Piper " * 100

    input_file = tmp_path / "entrada.txt"
    compressed_file = tmp_path / "archivo.pp"

    input_file.write_text(text, encoding="utf-8")

    compress(text, str(compressed_file))

    decoded = decompress(str(compressed_file))

    assert decoded == text

def test_single_character():
    text = "AAAAAAAAAA"

    frequencies = Counter(text)
    root = build_tree(frequencies)
    codes = generate_codes(root)

    encoded = encode(text, codes)
    decoded = decode(encoded, root)

    assert decoded == text





