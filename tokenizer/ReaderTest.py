from .Reader import *

r = Reader('12345667890-1234567890-')
p = PosReader(r)
while p.hasNext() :
    print(p.nextPos())