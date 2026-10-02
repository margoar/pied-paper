from .compressor import compress_file, decompress_file

input_file = "examples/ejemplo.txt"

compressed_file = "ejemplo.pp"

output_file = "examples/recuperado.txt"


compress_file(input_file, compressed_file)
decompress_file(compressed_file, output_file)


with open(input_file, "rb") as file:
    original = file.read()

with open(compressed_file, "rb") as file:
    compressed = file.read()

with open(output_file, "rb") as file:
    recovered = file.read()


original_size = len(original)
compressed_size = len(compressed)

compression_percentage = (
    (1 - compressed_size / original_size) * 100
)


print("Archivos idénticos:", original == recovered)
print("Tamaño original:", original_size, "bytes")
print("Tamaño comprimido:", compressed_size, "bytes")
print(f"Compresión: {compression_percentage:.2f}%")