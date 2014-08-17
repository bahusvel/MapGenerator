__author__ = 'denislavrov'

import CONSTANTS as CON


def displaymap(map, mode=CON.BUILDING, lvl=None):
    xa, ya, za = [], [], []
    for loc in map:
        xa.append(loc[CON.X])
        ya.append(loc[CON.X])
        za.append(loc[CON.X])
    xs = max(xa) + 1
    ys = max(ya) + 1
    zs = max(za) + 1
    level = 0
    line = 0
    i = 0
    while i <= len(map) - 1:
        if lvl is None or lvl == level:
            ls = "This is level %d" % level
            if map[i][CON.Y] == 0 and map[i][CON.X] == 0:
                print('    ' + "++--" * xs + '++')
                print('    ' + '||' + ' ' * (int(2 * xs - len(ls) / 2)) + ls + ' ' * (
                    int(2 * xs - len(ls) / 2) - 1) + '||')
                print('    ' + '++--' * xs + '++')
                print('    ', end='')
                for xi in range(xs):
                    print("||%02d" % xi, end='')
                print('||')
                print('++--' + '++--' * xs + '++')
                line = 0
            if map[i][CON.X] == 0:
                print('++--+', end='')
                for wi in map[i:i + xs]:
                    if wi[CON.EXITS] & CON.FRONT:
                        print('+--+', end='')
                    else:
                        if (wi[CON.EXITS] & (CON.LEFT ^ CON.RIGHT)) == (CON.LEFT ^ CON.RIGHT):
                            print('+  +', end='')
                        elif wi[CON.EXITS] & CON.LEFT:
                            print('+   ', end='')
                        elif wi[CON.EXITS] & CON.RIGHT:
                            print('   +', end='')
                        else:
                            print('    ', end='')
                print('+\n', end='')
                print('||%02d|' % line, end='')
                line += 1
            print('|' if map[i][CON.EXITS] & CON.LEFT else ' ', end='')
            print('  ' if not map[i][mode] else '%02d' % map[i][mode], end='')
            print('|' if map[i][CON.EXITS] & CON.RIGHT else ' ', end='')
            if map[i][CON.X] == xs - 1:
                print('|\n', end='')
                print('++--+', end='')
                for wi in map[i - xs + 1:i + 1]:
                    if wi[CON.EXITS] & CON.BACK:
                        print('+--+', end='')
                    else:
                        if (wi[CON.EXITS] & (CON.LEFT ^ CON.RIGHT)) == (CON.LEFT ^ CON.RIGHT):
                            print('+  +', end='')
                        elif wi[CON.EXITS] & CON.LEFT:
                            print('+   ', end='')
                        elif wi[CON.EXITS] & CON.RIGHT:
                            print('   +', end='')
                        else:
                            print('    ', end='')
                print('+\n', end='')
            if map[i][CON.X] == xs - 1 and map[i][CON.Y] == ys - 1:
                print('++--' + '++--' * xs + '++', '\n\n')
        i += 1
        try:
            if map[i][CON.Y] == 0 and map[i][CON.X] == 0:
                level += 1
        except:
            pass