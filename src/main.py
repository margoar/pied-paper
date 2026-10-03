from .compressor import compress_file, decompress_file


input_file = "examples/ejemplo.txt"
compressed_file = "ejemplo.pp"
output_file = "examples/recuperado.txt"


compress_file(input_file, compressed_file)
decompress_file(compressed_file, output_file)


with open(input_file, "rb") as file:
    original = file.read()

with open(output_file, "rb") as file:
    recovered = file.read()


print(f"Original: {len(original)} bytes")
print(f"Recuperado: {len(recovered)} bytes")
print(f"Correcto: {original == recovered}")