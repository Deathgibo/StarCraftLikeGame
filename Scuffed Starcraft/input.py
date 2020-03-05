

class input():
    def __init__(self):
        self.leftclick = False
        self.leftclickframe = False #resets every frame
        self.leftclickletgo = False
        self.rightclick = False
        self.rightclickframe = False
        self.mouseposition = (0,0)
        self.mouseclickposition = (0,0)
        self.mousechange = (0,0)
        self.mousewheel = 0
        self.keys = [0] * 500
        pass

    def reset(self):
        self.mousewheel = 0
        self.leftclickframe = False
        self.leftclickletgo = False
        self.rightclickframe = False

class inputlocator():
    input_ref = None
    @staticmethod
    def provide(input):
        inputlocator.input_ref = input
    @staticmethod
    def getinputinfo():
        return inputlocator.input_ref
