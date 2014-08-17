__author__ = 'denislavrov'

import BaseClasses as BS
import random
import CONSTANTS as CON
import ROOM


class Mansion(BS.Building):
    def __init__(self, xs=8, ys=8, zs=3, entry_level=1):
        self.ID = 1
        self.xsize = xs
        self.ysize = ys
        self.zsize = zs
        self.range = (0, xs, 0, ys, 0, zs)
        self.entries = [(self.range[0], self.range[2], entry_level, CON.FRONT),
                        (self.range[0], self.range[3] - 1, entry_level, CON.LEFT),
                        (self.range[1] - 1, self.range[2], entry_level, CON.RIGHT),
                        (self.range[1] - 1, self.range[3] - 1, entry_level, CON.BACK)]
        self.bdata = [(x, y, z, 0, self.ID, 0, 0) for z in range(self.zsize) for y in range(self.ysize)
                      for x in range(self.xsize)]

    # write the code to generate the house here

    def gen_floor_ceil(self):
        self.bdata = list(map(lambda x: BS.modloc(x, wall=CON.UP ^ CON.DOWN), self.bdata))

    def gen_perimeter_walls(self):
        for index in self.perimeter2d():
            if self.bdata[index][1] == self.range[2]:
                self.bdata[index] = BS.modloc(self.bdata[index], wall=CON.FRONT)
            if self.bdata[index][1] == self.range[3] - 1:
                self.bdata[index] = BS.modloc(self.bdata[index], wall=CON.BACK)
            if self.bdata[index][0] == self.range[0]:
                self.bdata[index] = BS.modloc(self.bdata[index], wall=CON.LEFT)
            if self.bdata[index][0] == self.range[1] - 1:
                self.bdata[index] = BS.modloc(self.bdata[index], wall=CON.RIGHT)

    def indexof(self, loc):
        for i, x in enumerate(self.bdata):
            if x[0:3] == loc:
                return i

    def gen_entrance(self):
        self.entry = self.entries[random.randint(0, 3)]
        index = self.indexof(self.entry[0:3])
        self.bdata[index] = BS.modloc(self.bdata[index], wall=self.entry[3] ^ BS.right_exit(self.entry[3]),
                                   room=ROOM.Hallway.ID)
        self.entry_loc = self.entry[0:3]

    def generate(self):
        self.gen_floor_ceil()
        self.gen_perimeter_walls()
        self.gen_entrance()
        self.hallway = ROOM.Hallway(self)
        self.living = ROOM.LivingRoom(self, self.hallway)
        self.bedroom = ROOM.Bedroom(self, self.hallway)
        self.kitchen = ROOM.Kitchen(self, self.hallway)


class Shed(BS.Building):
    ID = 2
    xsize = 4
    ysize = 4
    zsize = 1


class Well(BS.Building):
    ID = 3
    xsize = 2
    ysize = 2
    zsize = 1
