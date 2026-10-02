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

        heapq.heappush(
            heap,
            (frequency, counter, node)
        )

        counter += 1

    return heap

def build_tree(frequencies):
    heap = build_initial_heap(frequencies)
    counter = len(heap)

    while len(heap) > 1:
        _, _, left = heapq.heappop(heap)
        _, _, right = heapq.heappop(heap)

        parent = Node(
            frequency=left.frequency + right.frequency
        )

        parent.left = left
        parent.right = right

        heapq.heappush(
            heap,
            (parent.frequency, counter, parent)
        )

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

def print_tree(node, prefix=""):
    if node is None:
        return

    if node.character is not None:
        print(f"{prefix}{node.character} ({node.frequency})")
    else:
        print(f"{prefix}* ({node.frequency})")

    print_tree(node.left, prefix + "  ")
    print_tree(node.right, prefix + "  ")


frequencies = {
    "A": 5,
    "B": 3,
    "C": 2
}

root = build_tree(frequencies)

print_tree(root)


codes = generate_codes(root)

print("\nCódigos:")

for character, code in codes.items():
    print(f"{character} → {code}")