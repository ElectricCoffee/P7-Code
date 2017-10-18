import sys
sys.path.insert(0, '../')
from python_dbm import Context
c = Context(["x", "y", "z"], "d")
a = (c.x == 1).updateValue(c.x)
d = (c.x == 1).resetValue(c.x, 0)
print a
print b
print d