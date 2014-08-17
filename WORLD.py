__author__ = 'denislavrov'

import BUILDING
import BaseClasses as BS
import CONSTANTS as CON
import HELPER as HELP
import random


class World(BS.Parent, BS.Square):

    def insert_building(self, child, cdata, loc):
        crange = (loc[CON.X], loc[CON.X] + child.xsize - 1, loc[CON.Y], loc[CON.Y] + child.ysize - 1, loc[CON.Z],
                  loc[CON.Z] + child.zsize - 1)
        if self.loc_range_in_range(crange, self.range):
            i = 0
            for x, loc in enumerate(self.bdata):
                if BS.loc_in_range((loc[CON.X], loc[CON.Y], loc[CON.Z]), crange):
                    self.bdata[x] = (loc[CON.X], loc[CON.Y], loc[CON.Z], cdata[i][CON.EXITS], cdata[i][CON.BUILDING],
                                     cdata[i][CON.ROOM], cdata[i][CON.OBJECT])
                    i += 1

    def alloc_map(self, xs, ys, zs):
        self.bdata = [(x, y, z, 0, 0, 0, 0) for z in range(zs) for y in range(ys) for x in range(xs)]

    def rnd_build_loc(self, building):
        x = random.randint(1, self.range[1]-building.range[1]-1)
        y = random.randint(1, self.range[3]-building.range[3]-1)
        z = random.randint(0, self.range[5]-building.range[5])
        return x, y, z

    def __init__(self, xs=16, ys=16, zs=3):
        self.xsize = xs
        self.ysize = ys
        self.zsize = zs
        self.range = (0, xs, 0, ys, 0, zs)
        self.alloc_map(xs, ys, zs)
        self.mansion = BUILDING.Mansion()
        self.mansion.generate()
        self.insert_building(self.mansion, self.mansion.bdata, self.rnd_build_loc(self.mansion))

world = World()
HELP.displaymap(world.bdata, mode=CON.ROOM, lvl=1)





