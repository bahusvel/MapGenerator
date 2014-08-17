__author__ = 'denislavrov'
import BaseClasses as BS
import CONSTANTS as CON


class Hallway(BS.Room):
    ID = 1
    NAME = "Hallway"
    bdata = []

    def gen_hallway(self, building):
        direction = BS.op_exit(building.entry[3])
        if direction is CON.FRONT or direction is CON.BACK:
            fr = int(building.ysize/2)-1
            sr = int(building.xsize/2)
            ext = BS.right_exit(direction) ^ BS.left_exit(direction)
            ext2 = CON.FRONT ^ CON.BACK
        else:
            fr = int(building.xsize/2)
            sr = int(building.ysize/2)-1
            ext = CON.FRONT ^ CON.BACK
            ext2 = CON.LEFT ^ CON.RIGHT
        cloc = building.entry_loc
        for i in range(fr):
            loc = BS.loc_in_dir(cloc, direction, building)
            cloc = loc
            building.bdata[BS.loc_id(loc, building)] = \
                (loc[CON.X],
                 loc[CON.Y],
                 loc[CON.Z],
                 ext ^ BS.left_exit(direction) ^ direction if i == fr-1 else ext,
                 building.ID,
                 self.ID,
                 0)
        direction = BS.left_exit(direction)
        for i in range(sr):
            loc = BS.loc_in_dir(cloc, direction, building)
            cloc = loc
            building.bdata[BS.loc_id(loc, building)] = \
                (loc[CON.X],
                 loc[CON.Y],
                 loc[CON.Z],
                 ext2 ^ direction if i == sr-1 else ext2,
                 building.ID,
                 self.ID,
                 0)

    def __init__(self, building):
        self.gen_hallway(building)
        self.bdata = BS.loc_scan_for(building, self, CON.ROOM)
        self.SIZE = len(self.bdata)


class LivingRoom(BS.GenericRoom):
    ID = 2
    bdata = []
    SIZE = 10


class Bedroom(BS.GenericRoom):
    ID = 3
    bdata = []
    SIZE = 5


class Kitchen(BS.GenericRoom):
    ID = 4
    bdata = []
    SIZE = 3


