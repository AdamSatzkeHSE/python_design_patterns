# Build a factory that creates Button and Checkbox for two themes: Light and Dark
# The client should call ui_factory("dark") and get components with matching render()
# outputs

class Button:
    pass

class Checkbox:
    pass

class UIFactory:
    def create_button(self) -> Button:
        pass

    def create_checkbox(self) -> Checkbox:
        pass

def ui_factory(theme: str) -> UIFactory:
    pass

if __name__ == "__main__":
    f = ui_factory("dark")
    print(f.create_button().render())
    print(f.create_checkbox().render())