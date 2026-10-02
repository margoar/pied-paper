from collections import Counter
import pytest
from src.huffman import (
    build_tree,
    generate_codes,
    encode,
    decode
)

from src.compressor import (
    compress_file,
    decompress_file
)

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
    output_file = tmp_path / "recuperado.txt"

    input_file.write_text(text, encoding="utf-8")

    compress_file(str(input_file), str(compressed_file))
    decompress_file(str(compressed_file), str(output_file))

    decoded = output_file.read_text(encoding="utf-8")

    assert decoded == text



def test_single_character():
    text = "AAAAAAAAAA"

    frequencies = Counter(text)
    root = build_tree(frequencies)
    codes = generate_codes(root)

    encoded = encode(text, codes)
    decoded = decode(encoded, root)

    assert decoded == text


def test_incomplete_pp_file(tmp_path):
    file = tmp_path / "incompleto.pp"
    output_file = tmp_path / "salida.txt"

    file.write_bytes(b"PP")

    with pytest.raises(
        ValueError,
        match="Archivo PiedPiper incompleto"
    ):
        decompress_file(
            str(file),
            str(output_file)
        )


def test_invalid_pp_file(tmp_path):
    file = tmp_path / "invalido.pp"
    output_file = tmp_path / "salida.txt"

    file.write_bytes(b"NO")

    with pytest.raises(
        ValueError,
        match="El archivo no es un archivo PiedPiper válido"
    ):
        decompress_file(
            str(file),
            str(output_file)
        )    