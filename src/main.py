from collections import Counter

from huffman import bits_to_bytes, build_tree, generate_codes, encode, decode, save_compressed,load_compressed,bytes_to_bits, build_tree_from_codes

text = "AAAAABBBCC"

frequencies = Counter(text)

root = build_tree(frequencies)

codes = generate_codes(root)

encoded = encode(text, codes)

data, padding = bits_to_bytes(encoded)

save_compressed(data, padding, codes, "ejemplo.pp")

data, padding, codes = load_compressed("ejemplo.pp")

bits = bytes_to_bits(data, padding)

print("Bits recuperados:", bits)
print("Bytes:", data)
print("Padding:", padding)

root = build_tree_from_codes(codes)

decoded = decode(bits, root)

print("Descomprimido:", decoded)