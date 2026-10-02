from huffman import compress, decompress

with open("examples/ejemplo.txt", "r", encoding="utf-8") as file:
    text = file.read()

compress(text, "ejemplo.pp")

decoded = decompress("ejemplo.pp")


print("Descompresión correcta:", decoded == text)