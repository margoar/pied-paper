from huffman import compress_file, decompress_file


compress_file(
    "examples/ejemplo.txt",
    "ejemplo.pp"
)

decompress_file(
    "ejemplo.pp",
    "examples/recuperado.txt"
)


with open("examples/ejemplo.txt", "rb") as file:
    original = file.read()

with open("examples/recuperado.txt", "rb") as file:
    recovered = file.read()


print("Archivos idénticos:", original == recovered)