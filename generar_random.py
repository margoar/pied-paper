import os

with open("examples/random.bin", "wb") as file:
    file.write(os.urandom(10_000))