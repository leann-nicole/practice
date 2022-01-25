# A* PATHFINDING ALGORITHM

from math import sqrt

class Point:
    def __init__(self, *args):
        self.H = 0
        self.x = args[0]
        self.y = args[1]
        if len(args) == 4:
            self.Parent = args[2]
            if(args[2] == None): self.G = 0
            else:
                if(args[2].x != self.x and args[2].y != self.y): self.G = args[2].G + 14
                else: self.G = args[2].G + 10
                
            self.H = int(10 * sqrt(abs(args[3].x - self.x)**2 + abs(args[3].y - self.y)**2))
            self.F = self.G + self.H
    def __repr__(self):
        return repr('(' + str(self.x) + ',' + str(self.y) + ')')
    def __gt__(self, other):
        if(self.F == other.F): return self.H < other.H
        else: return self.F < other.F
