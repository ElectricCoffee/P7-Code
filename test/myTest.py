import sys
sys.path.insert(0, '../')
from udbm import Context
c = Context(["x", "y", "z"], "d")
a = (c.x == 1).updateValue(c.x, 2)
d = (c.x == 1).resetValue(c.x)
print a
print d
