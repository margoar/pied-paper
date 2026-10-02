from huffman import compress_bytes, decompress_bytes


with open("examples/ejemplo.txt", "rb") as file:
    data = file.read()


encoded, root = compress_bytes(data)

decoded = decompress_bytes(encoded, root)

print("Bytes originales:", len(data))
print("Bits Huffman:", len(encoded))
print("Descompresión correcta:", decoded == data)