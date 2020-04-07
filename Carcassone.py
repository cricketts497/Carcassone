import pandas as pd
import numpy as np
from Tile import Tile, SIDE_TYPE_DICT_CHAR

from colorama import Fore, Style, init
init()

class Game:
    def __init__(self):
        self.start_tile = Tile(['c','r','g','r'], [[1,3]])

        #create the bag to draw tiles from
        self.tile_bag = []
        tile_types = {8:[['g','r','g','r'],[[1,3]]]}
        for number, types in tile_types.items():
                for x in range(number):
                    self.tile_bag.append(Tile(types[0], types[1]))
        self.tile_bag = list(np.random.permutation(self.tile_bag))
        
        #indexed pd.Series of placed tiles with positions
        self.placed_tiles = pd.Series({(0,0):self.start_tile})

        #list of possible positions to play around placed tiles
        self.play_positions = [(1,0),(0,-1),(-1,0),(0,1)]
        
        #delta of positions around each tile
        self.dposition = [(0,1),(1,0),(0,-1),(-1,0)]
        
    def claim_start_tile(self, side_index, player):
        self.placed_tiles.loc[(0,0)].claim(side_index, player)
        
    def draw_tile(self):
        tile = self.tile_bag.pop()
        return tile

    def place_tile(self, tile, position):
        self.placed_tiles = self.placed_tiles.append(pd.Series({position:tile}))
        self.play_positions.remove(position)
        
        #check the surrounding positions
        for dpos_index, dpos in enumerate(self.dposition):
            adjacent_pos = (position[0]+dpos[0], position[1]+dpos[1])
            #add the adjacent empty places to the list of possible placements
            if (adjacent_pos not in self.play_positions) and (adjacent_pos not in self.placed_tiles.index):
                self.play_positions.append(adjacent_pos)
            #claim the sides of the linking tiles if that side of the placed tile is claimed
            elif (adjacent_pos in self.placed_tiles.index) and (tile.claims[dpos_index] != 0):
                print((dpos_index+2)%4)
                self.placed_tiles.loc[adjacent_pos].claim((dpos_index+2)%4, tile.claims[dpos_index])
                
        
    def check_pos(self, tile, position):
        good_placement = True
        #check the tiles at the (x,y) positions around the placement position
        #in the order of the tile's side list
        #for the sides and the claims
        for side_index, dpos in enumerate(self.dposition):
            adjacent_pos = (position[0]+dpos[0], position[1]+dpos[1])
            if adjacent_pos in self.placed_tiles.index:
                adjacent_tile = self.placed_tiles.loc[adjacent_pos]
                #joined by opposite sides
                if (tile.sides[side_index] != adjacent_tile.sides[(side_index+2)%4]) or (tile.claims[side_index] != adjacent_tile.claims[(side_index+2)%4]):
                    good_placement = False
        return good_placement
        
    #print the position of the placed tiles and the playable positions
    def print_tiles(self):
        x_play_pos = [x for x,y in self.play_positions]
        y_play_pos = [y for x,y in self.play_positions]
        
        maxx = max(x_play_pos)
        minx = min(x_play_pos)
        maxy = max(y_play_pos)
        miny = min(y_play_pos)
        
        # print(minx, maxx, miny, maxy)
        
        for y_pos in range(maxy+1, miny-2, -1):
            to_print = ''
            for x_pos in range(minx-1, maxx+2, 1):
                if (x_pos, y_pos) in self.placed_tiles.index:
                    to_print += 'T'
                elif (x_pos, y_pos) in self.play_positions:
                    to_print += 'P'
                else:
                    to_print += '.'
            print(to_print)
        
    #print the tiles with sides labelled by their chars, with player claims represented by colours
    def print_edges(self):
        x_play_pos = [x for x,y in self.play_positions]
        y_play_pos = [y for x,y in self.play_positions]
        
        maxx = max(x_play_pos)
        minx = min(x_play_pos)
        maxy = max(y_play_pos)
        miny = min(y_play_pos)
        
        grid = [[[[' ' for x in range(3)] for y in range(3)] for x in range(minx, maxx+1)] for y in range(maxy, miny-1, -1)]
        
        for y_index, y_pos in enumerate(range(maxy, miny-1, -1)):
            for x_index, x_pos in enumerate(range(minx, maxx+1, 1)):
                if (x_pos, y_pos) in self.placed_tiles.index:
                    tile = self.placed_tiles.loc[(x_pos, y_pos)]
                    
                    side_y = [0,1,2,1]
                    side_x = [1,2,1,0]
                    
                    grid[y_index][x_index][1][1] = 'T'
                    for side_index, side in enumerate(tile.sides):
                        if tile.claims[side_index] == 1:
                            grid[y_index][x_index][side_y[side_index]][side_x[side_index]] = Fore.RED + SIDE_TYPE_DICT_CHAR[side] + Style.RESET_ALL
                        elif tile.claims[side_index] == 2:
                            grid[y_index][x_index][side_y[side_index]][side_x[side_index]] = Fore.CYAN + SIDE_TYPE_DICT_CHAR[side] + Style.RESET_ALL
                        else:
                            grid[y_index][x_index][side_y[side_index]][side_x[side_index]] = SIDE_TYPE_DICT_CHAR[side]
                    
        for y_index, y_pos in enumerate(range(maxy, miny-1, -1)):
            for row in range(3):
                to_print = ''
                for x_index, x_pos in enumerate(range(minx, maxx+1, 1)):
                    for col in range(3):
                        to_print += grid[y_index][x_index][row][col]
                print(to_print)
        
g = Game()
g.claim_start_tile(1,1)

tile = g.draw_tile()
tile.claim(3,2)
if g.check_pos(tile,(0,-1)):
    g.place_tile(tile, (0,-1))
    
print([tile.claims for tile in list(g.placed_tiles)])
print(g.play_positions)

g.print_tiles()
g.print_edges()

