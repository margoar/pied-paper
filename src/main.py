from collections import Counter
import os

from huffman import bits_to_bytes, build_tree, generate_codes, encode, decode, save_compressed,load_compressed,bytes_to_bits, build_tree_from_codes

with open("examples/ejemplo.txt", "r", encoding="utf-8") as file:
    text = file.read()

frequencies = Counter(text)

root = build_tree(frequencies)

codes = generate_codes(root)

encoded = encode(text, codes)

data, padding = bits_to_bytes(encoded)

save_compressed(data, padding, codes, "ejemplo.pp")


original_size = os.path.getsize("examples/ejemplo.txt")
compressed_size = os.path.getsize("ejemplo.pp")

print("Tamaño original:", original_size, "bytes")
print("Tamaño comprimido:", compressed_size, "bytes")

data, padding, codes = load_compressed("ejemplo.pp")

bits = bytes_to_bits(data, padding)

print("Padding:", padding)

root = build_tree_from_codes(codes)

decoded = decode(bits, root)

