from collections import Counter

from huffman import build_tree, generate_codes, encode, decode

text = "AAAAABBBCC"

frequencies = Counter(text)

root = build_tree(frequencies)

codes = generate_codes(root)

encoded = encode(text, codes)

print("Texto:", text)
print("Códigos:", codes)
print("Comprimido:", encoded)
print("Bits:", len(encoded))

decoded = decode(encoded, root)

print("Descomprimido:", decoded)