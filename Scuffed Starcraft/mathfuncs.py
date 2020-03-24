import math


class mathfuncs():

    @staticmethod
    def Dot(a, b):
        return a[0] * b[0] + a[1] * b[1]

    @staticmethod
    def Magnitude(vec):
        return math.sqrt(vec[0] ** 2 + vec[1] ** 2)

    @staticmethod
    def Magnitudenosquare(vec):
        return vec[0] ** 2 + vec[1] ** 2

    @staticmethod
    def pointrectcollision(point, rect):  # rect starts at topleft
        if point[0] < rect[0] or point[0] > rect[0] + rect[2]:
            return False
        if point[1] > rect[1] or point[1] < rect[1] - rect[3]:
            return False
        return True

    @staticmethod
    def pointcirclecollision(point, circle):
        if pow(point[0] - circle[0], 2) + pow(point[1] - circle[1], 2) < pow(circle[2], 2):
            return True
        return False

    @staticmethod
    def rectrectcollision(rect1, rect2):
        # use pygame.Rect.contains()
        pass

    @staticmethod
    def rectcirclecollision(bx, by, bw, bh, cx, cy, cr):
        leftx = bx
        rightx = bx + bw
        if bw < 0:
            leftx = bx + bw
            rightx = bx
        topy = by
        bottomy = by + bh
        if bh < 0:
            topy = by + bh
            bottomy = by

        closestx = 0
        closesty = 0

        if cx < leftx:
            closestx = leftx
        elif cx > rightx:
            closestx = rightx
        else:
            closestx = cx

        if cy > bottomy:
            closesty = bottomy
        elif cy < topy:
            closesty = topy
        else:
            closesty = cy

        distance = (cx - closestx, cy - closesty)

        if (mathfuncs.Magnitudenosquare(distance) < cr ** 2):  # dont sqrt it
            return True
        return False

    @staticmethod
    def boxincircle(bx, by, bw, bh, cx, cy, cr):
        dx = max(cx - bx, bx + bw - cx);
        dy = max(cy - by + bh, by - cy);
        return cr * cr >= dx * dx + dy * dy

    @staticmethod
    def rectcirclecollisionspecial(bx, by, bw, bh, cx, cy, cr):
        leftx = bx
        rightx = bx + bw
        if bw < 0:
            leftx = bx + bw
            rightx = bx
        topy = by
        bottomy = by + bh
        if bh < 0:
            topy = by + bh
            bottomy = by

        closestx = 0
        closesty = 0
        inside = True
        if cx < leftx:
            inside = False
            closestx = leftx
        elif cx > rightx:
            inside = False
            closestx = rightx
        else:
            closestx = cx

        if cy > bottomy:
            inside = False
            closesty = bottomy
        elif cy < topy:
            inside = False
            closesty = topy
        else:
            closesty = cy

        distance = (cx - closestx, cy - closesty)
        mag = mathfuncs.Magnitudenosquare(distance)
        r = cr ** 2
        if inside and mag >= r:
            inside = True
        else:
            inside = False
        if (mag < r):  # dont sqrt it
            return (True, inside)
        return (False, False)

    @staticmethod
    def circlesegcollision(radius, cx, cy, p1x, p1y, p2x, p2y):  # uses ray to sphere collision
        c = (cx, cy)
        e = (p1x, p1y)
        d = (p2x - p1x, p2y - p1y)
        negd = (-d[0], -d[1])
        emc = (e[0] - c[0], e[1] - c[1])
        det = (mathfuncs.Dot(d, emc) ** 2) - (mathfuncs.Dot(d, d)) * (mathfuncs.Dot(emc, emc) - radius ** 2)
        if det < 0:
            return False
        tpos = (mathfuncs.Dot(negd, emc) + math.sqrt(det)) / mathfuncs.Dot(d, d)
        tneg = (mathfuncs.Dot(negd, emc) - math.sqrt(det)) / mathfuncs.Dot(d, d)
        if (tpos > 1 or tpos < 0) and (tneg > 1 or tneg < 0):
            return False
        return True

    @staticmethod
    def circlecirclecollision(c1, c2):
        length = mathfuncs.Magnitude((c1[0] - c2[0], c1[1] - c2[1]))
        if length < (c1[2] + c2[2]):
            return True
        return False
