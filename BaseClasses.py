__author__ = 'denislavrov'

import CONSTANTS as CON
import random
import functools


class Parent:
    ID = None
    entry_loc = None
    bdata = []

class Square:
    xsize = None
    ysize = None
    zsize = None
    range = None

    def loc_range_in_range(self, rng1, rng2):
        if rng1[0] >= rng2[0] and rng1[2] >= rng2[2] and rng1[4] >= rng2[4]:
            if rng1[1] < rng2[1] and rng1[3] < rng2[3] and rng1[5] < rng2[5]:
                return True
        return False


class Building(Parent, Square):
    entry_loc = None
    bdata = []

    def perimeter2d(self, level=None):
        retbuffer = []
        for i, loc in enumerate(self.bdata):
            if level is None:
                if loc[CON.X] == self.range[0] or loc[CON.X] == self.range[1] - 1 or loc[CON.Y] == self.range[2] or \
                                loc[CON.Y] == self.range[3] - 1:
                    retbuffer.append(i)
            else:
                if (loc[CON.X] == self.range[0] or loc[CON.X] == self.range[1] - 1 or loc[CON.Y] == self.range[2] or
                            loc[CON.Y] == self.range[3] - 1) and loc[CON.Z] == level:
                    retbuffer.append(i)
        return retbuffer


class Room(Parent):
    ID = None
    NAME = None
    SIZE = None
    BUILDING = None
    entry_loc = None
    bdata = []


class GenericRoom(Room):
    def opendoor(self, building, oroom):
        for loc in loc_array_untrim(loc_near_loc(self.entry_loc, building), building):
            if loc[CON.ROOM] == oroom.ID:
                door = loc_to_loc(self.entry_loc, loc)
                building.bdata[loc_id(loc, building)] = modloc(loc, wall=door)
                self.bdata[loc_id(self.entry_loc, self)] = modloc(self.bdata[loc_id(self.entry_loc, self)],
                                                                  wall=op_exit(door))

    def gen_room_walls(self, building):
        for index, loc in enumerate(self.bdata):
            self.bdata[index] = modloc(loc, wall=CON.ALLWALLS, mode='or')
        for index, loc in enumerate(self.bdata):
            for nloc in loc_array_untrim(loc_near_loc(loc, building, level=loc[CON.Z]), building):
                if nloc[CON.ROOM] == self.ID:
                    self.bdata[index] = modloc(self.bdata[index], wall=loc_to_loc(nloc, loc))

    def room_loc_alloc(self, building, roomloc):
        room_bdata = [modloc(roomloc, room=self.ID)]
        while len(room_bdata) < self.SIZE:
            skip = 0
            locbuffer = []
            for rloc in room_bdata:
                for loc in loc_array_untrim(loc_near_loc(rloc, building, level=rloc[CON.Z]), building):
                    if loc[CON.ROOM] is CON.EMPTYSPACE and loc[CON.BUILDING] is building.ID and loc_trim(loc) \
                            not in loc_array_trim(room_bdata):
                        locbuffer.append(loc)
            if not locbuffer:
                return None
            #weightedloc = locbuffer   loc_weighting(self, locbuffer, building)
            if skip == 0:
                room_bdata.append(modloc(locbuffer[random.randint(0, len(locbuffer) - 1)], room=self.ID))

        return room_bdata

    def room_ins(self, building):
        for loc in self.bdata:
            for index, bloc in enumerate(building.bdata):
                if bloc[0:3] == loc[0:3]:
                    building.bdata[index] = loc

    def room_prealloc(self, building):
        for loc in self.bdata:
            for index, bloc in enumerate(building.bdata):
                if bloc[0:3] == loc[0:3]:
                    building.bdata[index] = modloc(building.bdata[index], room=self.ID)

    def gen_room(self, building, oroom):
        per = loc_filter_free(loc_array_untrim(loc_perimeter(oroom.bdata, building), building))
        for loc in per:
            room = self.room_loc_alloc(building, loc)
            if room is not None:
                self.bdata = room
                self.entry_loc = loc
                break
        if not self.bdata:
            raise NotEnoughSpace(self)

        self.room_prealloc(building)
        for loc in loc_find_orphans(building):
            self.bdata.append(modloc(loc, room=self.ID))
            self.SIZE += 1
        self.room_prealloc(building)
        self.gen_room_walls(building)
        self.opendoor(building, oroom)

    def __init__(self, building, entranceroom):
        self.NAME = parse_class_name(self)
        self.gen_room(building, entranceroom)
        self.room_ins(building)


class Obj:
    ID = None
    NAME = None
    Description = None


class NotEnoughSpace(Exception):
    def __init__(self, room):
        self.value = room

    def __str__(self):
        return 'Room = %s, Allocation Size = %d' % (self.value.NAME, self.value.SIZE)


def loc_weighting(room, locarray, building):
    weight_table = {
        'room_around': 3,
        'hallway_around': 1,
        'potential_orphan': 1,

    }

    retbuffer = []
    for loc in list(set(locarray)):
        locaround = loc_array_untrim(loc_near_loc(loc, building, CON.Z), building)
        locweigh = 1
        naround = len(loc_filter(locaround, CON.ROOM, room.ID))
        if naround > 1:
            locweigh = naround * weight_table.get('room_around')
        if len(loc_filter(locaround, CON.ROOM, 1)):
            locweigh = 1 * weight_table.get('hallway_around')
        if not loc_filter_free(locaround):
            locweigh = weight_table.get('potential_orphan')

        for i in range(locweigh):
            retbuffer.append(loc)
    return retbuffer


def un_camel(x): return functools.reduce(lambda a, b: a + ((b.upper() == b and (len(a) and a[-1].upper() != a[-1])) and
                                                           (' ' + b) or b), x, '')


def parse_class_name(self_class):
    return un_camel(self_class.__class__.__name__)


def loc_appendix(loc, room, building):
    count = 0
    locarray = loc_untrim(loc_near_loc(loc, building, level=loc[CON.Z]), building)
    for l in locarray:
        if l[CON.ROOM] == room.ID:
            count += 1
    return count


def loc_in_range(loc, rng):
    if loc[CON.X] >= rng[0] and loc[CON.Y] >= rng[2] and loc[CON.Z] >= rng[4]:
        if loc[CON.X] <= rng[1] and loc[CON.Y] <= rng[3] and loc[CON.Z] <= rng[5]:
            return True
    return False


def loc_filter_free(locarray):
    retbuffer = []
    for loc in locarray:
        if loc[CON.ROOM] == 0:
            retbuffer.append(loc)
    return retbuffer


def loc_filter(locarray, type, value):
    retbuffer = []
    for loc in locarray:
        if loc[type] == value:
            retbuffer.append(loc)
    return retbuffer


def loc_in_dir(loc, dir, parent):
    x = loc[CON.X]
    y = loc[CON.Y]
    z = loc[CON.Z]
    if dir == CON.UP:
        z += 1
    elif dir == CON.DOWN:
        z -= 1
    elif dir == CON.LEFT:
        x -= 1
    elif dir == CON.RIGHT:
        x += 1
    elif dir == CON.FRONT:
        y -= 1
    elif dir == CON.BACK:
        y += 1
    else:
        return None
    if loc_in_range((x, y, z), parent.range):
        return x, y, z
    else:
        return None


def loc_perimeter(locarray, parent):
    retbuffer = []
    for loc in locarray:
        for nloc in loc_near_loc(loc, parent, level=loc[CON.Z]):
            retbuffer.append(nloc)
    return list(set(retbuffer) - set(loc_array_trim(locarray)))


def loc_id(loc, parent):
    for i, v in enumerate(parent.bdata):
        if loc[0:3] == v[0:3]:
            return i
    return None


def loc_near_loc(loc, parent, level=None):
    retbuffer = []
    for direction in CON.DIRECTIONS:
        nl = loc_in_dir(loc, direction, parent)
        if (nl is not None) and (nl[CON.Z] == level) or (nl is not None) and (level is None):
            retbuffer.append(nl)
    return retbuffer


def loc_near_loc_id(loc, parent, level=None):
    retbuffer = []
    for i in loc_near_loc(loc, parent, level=level):
        retbuffer.append(loc_id(i, parent))
    return retbuffer


def loc_array_to_id(locarray, parent):
    retbuffer = []
    for loc in locarray:
        retbuffer.append(loc_id(loc, parent))
    return retbuffer


def loc_scan_for(parent, child, mode):
    retbuffer = []
    for loc in parent.bdata:
        if loc[mode] == child.ID:
            retbuffer.append(loc)
    return retbuffer


def loc_array_trim(locarray):
    retbuffer = []
    for loc in locarray:
        retbuffer.append(loc[0:3])
    return retbuffer


def loc_array_untrim(locarray, parent):
    retbuffer = []
    for loc in locarray:
        for ploc in parent.bdata:
            if ploc[0:3] == loc[0:3]:
                retbuffer.append(ploc)
    return retbuffer


def loc_untrim(loc, parent):
    for ploc in parent.bdata:
        if ploc[0:3] == loc[0:3]:
            return ploc


def loc_trim(loc):
    return loc[0:3]


def loc_to_loc(loc1, loc2):
    if loc1[CON.X] < loc2[CON.X]:
        return CON.LEFT
    elif loc1[CON.X] > loc2[CON.X]:
        return CON.RIGHT
    elif loc1[CON.Y] > loc2[CON.Y]:
        return CON.BACK
    elif loc1[CON.Y] < loc2[CON.Y]:
        return CON.FRONT
    elif loc1[CON.Z] > loc2[CON.Z]:
        return CON.UP
    elif loc1[CON.Z] < loc2[CON.Z]:
        return CON.DOWN


def loc_find_orphans(building):
    retbuffer = []
    for loc in loc_scan_for(building, CON.EmptySpace, CON.ROOM):
        if not len(loc_filter_free(loc_array_untrim(loc_near_loc(loc, building, level=loc[CON.Z]), building))):
            retbuffer.append(loc)
    return retbuffer


def op_exit(ext):
    if ext == CON.UP:
        return CON.DOWN
    elif ext == CON.DOWN:
        return CON.UP
    elif ext == CON.LEFT:
        return CON.RIGHT
    elif ext == CON.RIGHT:
        return CON.LEFT
    elif ext == CON.FRONT:
        return CON.BACK
    elif ext == CON.BACK:
        return CON.FRONT


def left_exit(ext):
    if ext == CON.LEFT:
        return CON.BACK
    elif ext == CON.RIGHT:
        return CON.FRONT
    elif ext == CON.FRONT:
        return CON.LEFT
    elif ext == CON.BACK:
        return CON.RIGHT


def right_exit(ext):
    return op_exit(left_exit(ext))


def modloc(loc, wall=0b000000, building=None, room=None, obj=None, mode='xor'):
    if building is None:
        building = loc[CON.BUILDING]
    if room is None:
        room = loc[CON.ROOM]
    if obj is None:
        obj = loc[CON.OBJECT]

    return loc[CON.X], loc[CON.Y], loc[CON.Z], loc[CON.EXITS] ^ wall if mode == 'xor' else loc[CON.EXITS] | wall, \
           building, room, obj








