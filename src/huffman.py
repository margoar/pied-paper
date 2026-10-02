import heapq


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
        codes[node.character] = code
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