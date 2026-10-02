def to_binary(value: int) -> str:
    return format(value, "08b")


print(to_binary(65))

def show_binary(text: str) -> None:
    for char in text:
        value = ord(char)
        binary = format(value, "08b")

        print(f"{char} → {value} → {binary}")


show_binary("ABC")