import heapq
from collections import Counter


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


def encode(data, codes):
    encoded = ""

    for value in data:
        encoded += codes[value]

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


def decode_bytes(encoded, root):
    if root.left is None and root.right is None:
        return bytes([root.character]) * len(encoded)

    decoded = bytearray()
    current = root

    for bit in encoded:
        if bit == "0":
            current = current.left
        else:
            current = current.right

        if current.character is not None:
            decoded.append(current.character)
            current = root

    return bytes(decoded)


def compress_bytes(data):
    frequencies = Counter(data)

    root = build_tree(frequencies)
    codes = generate_codes(root)

    encoded = encode(data, codes)

    return encoded, root


def serialize_tree_binary(node):
    if node.character is not None:
        return b"\x01" + bytes([node.character])

    return (
        b"\x00"
        + serialize_tree_binary(node.left)
        + serialize_tree_binary(node.right)
    )


def deserialize_tree_binary(data, index=0):
    marker = data[index]
    index += 1

    if marker == 1:
        character = data[index]
        index += 1

        return Node(character=character), index

    if marker == 0:
        left, index = deserialize_tree_binary(data, index)
        right, index = deserialize_tree_binary(data, index)

        node = Node()
        node.left = left
        node.right = right

        return node, index

    raise ValueError("Árbol Huffman inválido")