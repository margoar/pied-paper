import heapq
import json
from collections import Counter
from logging import root

class Node:
    def __init__(self, character=None, frequency=0):
        self.character = character
        self.frequency = frequency
        self.left = None
        self.right = None

def build_initial_heap(frequencies):
    heap = []
    counter = 0

    for character, frequency in frequencies.items():
        node = Node(character, frequency)

        heapq.heappush(heap, (frequency, counter, node))
        counter += 1
    return heap

def build_tree(frequencies):
    heap = build_initial_heap(frequencies)
    counter = len(heap)
    while len(heap) > 1:
        _, _, left = heapq.heappop(heap)
        _, _, right = heapq.heappop(heap)

        parent = Node(frequency=left.frequency + right.frequency)
        parent.left = left
        parent.right = right

        heapq.heappush(heap, (parent.frequency, counter, parent))
        counter += 1
    return heapq.heappop(heap)[2]

def generate_codes(node, code="", codes=None):
    if codes is None:
        codes = {}

    if node.character is not None:
        codes[node.character] = code or "0"
        return codes

    generate_codes(node.left, code + "0", codes)
    generate_codes(node.right, code + "1", codes)

    return codes

def encode(text, codes):
    encoded = ""

    for character in text:
        encoded += codes[character]
    return encoded

def decode(encoded, root):
    if root.left is None and root.right is None:
        return root.character * len(encoded)

    decoded = ""
    current = root

    for bit in encoded:
        if bit == "0":
            current = current.left
        else:
            current = current.right

        if current.character is not None:
            decoded += current.character
            current = root
    return decoded

def bits_to_bytes(bits):
    padding = (8 - len(bits) % 8) % 8
    bits += "0" * padding

    data = bytearray()

    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        data.append(int(byte, 2))

    return bytes(data), padding

def save_compressed(data, padding, root, filename):
    tree_data = serialize_tree_binary(root)
    tree_size = len(tree_data)

    with open(filename, "wb") as file:
        file.write(b"PP")
        file.write(bytes([1]))

        file.write(tree_size.to_bytes(4, "big"))
        file.write(bytes([padding]))

        file.write(tree_data)
        file.write(data)    

def bytes_to_bits(data, padding):
    bits = ""

    for byte in data:
        bits += format(byte, "08b")

    if padding:
        bits = bits[:-padding]

    return bits

def load_compressed(filename):
    with open(filename, "rb") as file:
        magic = file.read(2)

        if magic != b"PP":
            raise ValueError("El archivo no es un archivo PiedPiper válido")

        version = file.read(1)[0]

        if version != 1:
            raise ValueError(f"Versión no soportada: {version}")

        tree_size = int.from_bytes(file.read(4), "big")
        padding = file.read(1)[0]

        tree_data = file.read(tree_size)
        data = file.read()

        root, _ = deserialize_tree_binary(tree_data)

    return data, padding, root


def build_tree_from_codes(codes):
    root = Node()
    for character, code in codes.items():
        current = root

        for bit in code:
            if bit == "0":
                if current.left is None:
                    current.left = Node()
                current = current.left
            else:
                if current.right is None:
                    current.right = Node()
                current = current.right
        current.character = character
    return root

def compress(text, filename):
    frequencies = Counter(text)

    root = build_tree(frequencies)
    codes = generate_codes(root)

    encoded = encode(text, codes)

    data, padding = bits_to_bytes(encoded)

    save_compressed(data, padding, root, filename)

def decompress(filename):
    data, padding, root = load_compressed(filename)

    bits = bytes_to_bits(data, padding)

    return decode(bits, root)

def serialize_tree(node):
    if node.character is not None:
        return {
            "type": "leaf",
            "character": node.character
        }

    return {
        "type": "node",
        "left": serialize_tree(node.left),
        "right": serialize_tree(node.right)
    }

def deserialize_tree(data):
    if data["type"] == "leaf":
        return Node(character=data["character"])

    node = Node()

    node.left = deserialize_tree(data["left"])
    node.right = deserialize_tree(data["right"])

    return node

def serialize_tree_binary(node):
    if node.character is not None:
        character_bytes = node.character.encode("utf-8")

        return (
            b"\x01"
            + bytes([len(character_bytes)])
            + character_bytes
        )

    return (
        b"\x00"
        + serialize_tree_binary(node.left)
        + serialize_tree_binary(node.right)
    )

def deserialize_tree_binary(data, index=0):
    marker = data[index]
    index += 1

    if marker == 1:
        length = data[index]
        index += 1

        character = data[index:index + length].decode("utf-8")
        index += length

        return Node(character=character), index

    if marker == 0:
        left, index = deserialize_tree_binary(data, index)
        right, index = deserialize_tree_binary(data, index)

        node = Node()
        node.left = left
        node.right = right

        return node, index

    raise ValueError("Árbol Huffman inválido")

def compress_text(text):
    frequencies = Counter(text)

    root = build_tree(frequencies)
    encoded = encode(text, generate_codes(root))

    return encoded, root

def decompress_text(encoded, root):
    return decode(encoded, root)