import os

from huffman import compress, decompress


with open("examples/ejemplo.txt", "r", encoding="utf-8") as file:
    text = file.read()


compress(text, "ejemplo.pp")

compressed_size = os.path.getsize("ejemplo.pp")

print("Tamaño original:", len(text.encode("utf-8")), "bytes")
print("Tamaño .pp:", compressed_size, "bytes")

decoded = decompress("ejemplo.pp")

print("Descompresión correcta:", decoded == text)