MINI14 = "1.4GHz Mac mini"

class AppleFactory:
    class MacMini14:
        def __init__(self):
            self.memory = 4
            self.hdd = 500
            self.gpu = "Intel HD Graphics 5000"

        def __str__(self):
            info = (f"Model: {MINI14}",
                    f"Memory: {self.memory}",
                    f"Hard Disk: {self.hdd}",
                    f"Graphics Card: {self.gpu}")
            return "\n".join(info)
        
    def build_computer(self, model):
        if model == MINI14:
            return self.MacMini14()
        else:
            msg = f"I don't know how to build {model}"
            print(msg)

if __name__ == '__main__':
    afac = AppleFactory()
    mac_mini = afac.build_computer(MINI14)
    print(mac_mini)