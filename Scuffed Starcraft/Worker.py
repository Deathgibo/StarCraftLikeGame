import Entity

class Worker(Entity.Entity):

    def __init__(self, rad,imgsurf, pyrect):
        super().__init__(rad,imgsurf,pyrect)
        self.circlexpercent = .5
        self.circleypercent = .75
        self.Move(0,0)
        self.collecting = False
        self.worker = True
        #extra
