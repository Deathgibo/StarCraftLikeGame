import math

class mathfuncs():

    @staticmethod
    def Dot(a, b):
        return a[0]*b[0] + a[1]*b[1]

    @staticmethod
    def Magnitude(vec):
        return math.sqrt(vec[0]**2 + vec[1]**2)

    @staticmethod
    def circlesegcollision(radius, cx,cy, p1x,p1y,p2x,p2y):   #uses ray to sphere collision
        c = (cx,cy)
        e = (p1x,p1y)
        d = (p2x - p1x,p2y - p1y)
        negd = (-d[0],-d[1])
        emc = (e[0]-c[0],e[1]-c[1])
        det = (mathfuncs.Dot(d,emc)**2) - (mathfuncs.Dot(d,d))*(mathfuncs.Dot(emc,emc) - radius**2)
        if det < 0:
            return False
        tpos = (mathfuncs.Dot(negd,emc) + math.sqrt(det))/mathfuncs.Dot(d,d)
        tneg = (mathfuncs.Dot(negd,emc) - math.sqrt(det))/mathfuncs.Dot(d,d)
        if (tpos > 1 or tpos < 0) and (tneg > 1 or tneg < 0):
            return False
        return True

    @staticmethod
    def circlecirclecollision(c1, c2):
        length = mathfuncs.Magnitude((c1[0] - c2[0],c1[1] - c2[1]))
        if length < (c1[2] + c2[2]):
            return True
        return False
