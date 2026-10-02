import json

from collections import Counter

from huffman import (
    build_tree,
    generate_codes,
    encode,
    compress,
    decompress,
    serialize_tree,
    serialize_tree_binary,
    deserialize_tree_binary
)


with open("examples/ejemplo.txt", "r", encoding="utf-8") as file:
    text = file.read()


# Construimos el árbol para comparar sus representaciones
frequencies = Counter(text)

root = build_tree(frequencies)
codes = generate_codes(root)

encoded = encode(text, codes)


# Probamos la serialización binaria del árbol
tree = serialize_tree(root)

tree_binary = serialize_tree_binary(root)

restored_root, _ = deserialize_tree_binary(tree_binary)

restored_codes = generate_codes(restored_root)


print("Árbol binario reconstruido:", restored_codes == codes)
print("Tamaño árbol JSON:", len(json.dumps(tree).encode("utf-8")))
print("Tamaño árbol binario:", len(tree_binary))


# Probamos el compresor real
compress(text, "ejemplo.pp")

compressed_size = __import__("os").path.getsize("ejemplo.pp")

print("Tamaño original:", len(text.encode("utf-8")), "bytes")
print("Tamaño .pp:", compressed_size, "bytes")

decoded = decompress("ejemplo.pp")

print("Descompresión correcta:", decoded == text)