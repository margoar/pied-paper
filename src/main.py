from collections import Counter
from huffman import compress, decompress, build_tree, generate_codes, encode


with open("examples/ejemplo.txt", "r", encoding="utf-8") as file:
    text = file.read()



frequencies = Counter(text)

root = build_tree(frequencies)
codes = generate_codes(root)

encoded = encode(text, codes)

print("Caracteres:", len(text))
print("Bits originales:", len(text) * 8)
print("Bits Huffman:", len(encoded))
compress(text, "ejemplo.pp")




decoded = decompress("ejemplo.pp")


print("Descompresión correcta:", decoded == text)

