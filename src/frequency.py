from collections import Counter


def count_frequencies(text: str) -> Counter:
    return Counter(text)


def calculate_probabilities(frequencies: Counter) -> dict:
    total = sum(frequencies.values())

    return {
        char: frequency / total
        for char, frequency in frequencies.items()
    }


text = "AAAAABBBCC"

frequencies = count_frequencies(text)
probabilities = calculate_probabilities(frequencies)

print("Frecuencias:")

for char, frequency in frequencies.items():
    print(f"{char} → {frequency}")

print("\nProbabilidades:")

for char, probability in probabilities.items():
    print(f"{char} → {probability:.2%}")

    codes = {
    "A": "0",
    "B": "10",
    "C": "11"
}

encoded = ""

for char in text:
    encoded += codes[char]

print("\nTexto original:")
print(text)

print("\nTexto codificado:")
print(encoded)

print(f"\nBits utilizados: {len(encoded)}")