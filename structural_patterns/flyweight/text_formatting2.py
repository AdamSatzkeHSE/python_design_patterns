""" We are building a text editor
Each character on screen could have formatting like
font, size, color

If you have thousands of characters, storing all that formatting data inside every character
wastes memory

Instead, we can share common formatting settings among many characters."""

# Intrinsic state: font, size, color
# Extrinsic state: actual character 'a', 'b' and its position.

# Context class
class Character:
    def __init__(self, symbol, position, style):
        self.symbol = symbol
        self.position = position
        self.style = style

    def display(self):
        print(f"Character '{self.symbol}' at {self.position} with style {self.style}")


class CharacterStyle:
    def __init__(self, font, size, color):
        self.font = font
        self.size = size
        self.color = color

    def __str__(self):
        return f"font={self.font}, size={self.size}, color={self.color}"
    
# Flyweight Factory
class CharacterStyleFactory:
    _styles = {}

    @classmethod
    def get_style(cls, font, size, color):
        key = (font, size, color)
        if key not in cls._styles:
            cls._styles[key] = CharacterStyle(font, size, color)
            print(f"Created new CharacterStyle: {cls._styles[key]}")
        return cls._styles[key]
    
# Client Code
if __name__ == "__main__":
    factory = CharacterStyleFactory()
    chars = []

    # Shared Styles
    bold_style = factory.get_style("Arial", 12, "Black")
    italic_style = factory.get_style("Arial", 12, "Gray")

    # Characters share these styles
    chars.append(Character('H', (0, 0), bold_style))
    chars.append(Character('e', (1, 0), bold_style))
    chars.append(Character('l', (2, 0), italic_style))
    chars.append(Character('l', (3, 0), italic_style))
    chars.append(Character('o', (4, 0), bold_style))


    for c in chars:
        c.display()

    # We created only 2 style objects even though we have 5 characters
    # Each character now stores its symbol, position and reference to the shared style.