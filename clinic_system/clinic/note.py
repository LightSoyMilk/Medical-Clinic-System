from datetime import datetime
class Note:
    def __init__(self, code: int, text: str): # Change this later Ben!
        self.code = code 
        self.text = text 
        self.timestamp = datetime.now() # Do this later Ben!

    def __str__(self):
        return f"The note's code is {self.code}: {self.text} , created at {self.timestamp}"
    
    def __eq__(self, other):
        return self.code == other.code and self.text == other.text
    
    def get_code(self):
        return self.code
    
    def get_text(self):
        return self.text