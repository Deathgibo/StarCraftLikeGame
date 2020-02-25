
##Playerinfo = playerinfoLog()
##playerinfolocator.provide(Playerinfo)
##Playerinfo.giveresources(20)
##playerinfolocator.getplayerinfo().resources

class playerinfo():
    def __init__(self):
        self.resources = 5
        self.supply = 0

    def giveresources(self, resource):
        self.resources = self.resources + resource

    def update(self):
        self.resources = self.resources + 1

class playerinfoLog():
    def __init__(self):
        self.resources = 5
        self.supply = 0
        print("initialized")

    def giveresources(self, resource):
        print("resources given to player")
        self.resources = self.resources + resource

    def update(self):
        self.resources = self.resources + 1
        print("updated")

class playerinfolocator():#make null exceptions
    playerinfo_ref = None
    @staticmethod
    def provide(playerinfo):
        playerinfolocator.playerinfo_ref = playerinfo
    @staticmethod
    def getplayerinfo():
        return playerinfolocator.playerinfo_ref
