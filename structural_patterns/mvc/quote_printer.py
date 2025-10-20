""" quote_printer.py
The user enters a number and sees the quote related to that number
The quotes are stored in a quotes tuple. This is the data that normally exists
in a database, and only the model has access to it.
"""
quotes = (
    "A man is not complete until he is married. Then he is finished",
    "As I said before, I never repeat myself.",
    "Behind a successful man is an exhausted woman.",
    "Black holes really suck.",
    "Facts are stubborn things."
)

""" Model """
class QuoteModel:
    def get_quote(self, n):
        try:
            value = quotes[n]
        except IndexError as ex:
            value = "Not found"
        return value

""" The view """
class QuoteTerminalView:
    def show(self, quote):
        print(f"And the quote is: {quote}")

    def error(self, msg):
        print(f"Error: {msg}")
    
    def select_quote(self):
        return input("Which quote number would you like to see? ")
    
""" The controller """

class QuoteTerminalController:
    def __init__(self):
        self.model = QuoteModel()
        self.view = QuoteTerminalView()

    def run(self):
        valid_input = False
        while not valid_input:
            try:
                n = self.view.select_quote()
                n = int(n)
                valid_input = True
            except ValueError as err:
                self.view.error(f"Incorrect index '{n}'")
            quote = self.model.get_quote(n)
            self.view.show(quote)

""" The main function initializes and fires the controller as shown in the following code.
"""

def main():
    controller = QuoteTerminalController()
    while True:
        controller.run()

main()
    