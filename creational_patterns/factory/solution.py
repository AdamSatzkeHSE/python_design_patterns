class Button:
    def render(self):
        pass

class Checkbox:
    def render(self):
        pass

class LightButton(Button):
    def render(self):
        return "LightButton"
    
class DarkButton(Button):
    def render(self):
        return "DarkButton"
    
class LightCheckbox(Checkbox):
    def render(self):
        return "LightCheckbox"
    
class DarkCheckbox(Checkbox):
    def render(self):
        return "DarkCheckbox"
    
class UIFactory:
    def create_button(self) -> Button:
        pass
    def create_checkbox(self) -> Checkbox:
        pass

class LightFactory(UIFactory):
    def create_button(self):
        return LightButton()
    
    def create_checkbox(self):
        return LightCheckbox()
    
class DarkFactory(UIFactory):
    def create_button(self): 
        return DarkButton()
    def create_checkbox(self): 
        return DarkCheckbox()

def ui_factory(theme: str) -> UIFactory:
    return LightFactory() if theme.lower()=="light" else DarkFactory()


if __name__ == "__main__":
    f = ui_factory("dark")
    print(f.create_button().render())
    print(f.create_checkbox().render())