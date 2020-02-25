

class input():
    def __init__(self):
        self.leftclick = False
        self.rightclick = False
        self.mouseposition = (0,0)
        self.mousechange = (0,0)
        self.keys = [0] * 500
        pass


class inputlocator():
    input_ref = None
    @staticmethod
    def provide(input):
        inputlocator.input_ref = input
    @staticmethod
    def getinputinfo():
        return inputlocator.input_ref
