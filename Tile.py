#sides: list with [N,E,S,W] and 0=>grass, 1=>road, 2=>city
MAX_SIDE_TYPE = 2
SIDE_TYPE_DICT = {0:'grass', 1:'road', 2:'city'}
SIDE_TYPE_DICT_CHAR = {0:'g', 1:'r', 2:'c'}
INVERSE_SIDE_TYPE_DICT = {'grass':0, 'road':1, 'city':2}
INVERSE_SIDE_TYPE_DICT_CHAR = {'g':0, 'r':1, 'c':2}

class Tile:
    def __init__(self, sides=[], links=[]):
        self.sides = []
        if len(sides) == 4:
            for side in sides:
                if isinstance(side, int) and side < MAX_SIDE_TYPE:
                    self.sides.append(side)
                else:
                    try:
                        self.sides.append(INVERSE_SIDE_TYPE_DICT[side])
                    except KeyError:
                        self.sides.append(INVERSE_SIDE_TYPE_DICT_CHAR[side])
                        
        self.links = links
        self.claims = [0,0,0,0]
                
    #n = number of 90 degree rotations
    def rotate(self,n=1,clockwise=True):
        if not clockwise:
            n *= -1
        self.sides = self.sides[n:] + self.sides[:n]
        
    def claim(self, side_index, player):
        #check the side and any linked sides are not claimed
        can_claim = (self.claims[side_index] == 0) 
        linked_sides = []
        for link in self.links:
            if side_index in link:
                for s in link:
                    linked_sides.append(s)
                    if self.claims[s] != 0:
                        can_claim = False
        
        #claim the side and any linked sides
        if can_claim:
            self.claims[side_index] = player
            for s in linked_sides:
                self.claims[s] = player
                            
            
        