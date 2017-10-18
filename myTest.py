import sys
sys.path.insert(0, '../')
from python_dbm import Context
c = Context(["x", "y"], "d")
a = (c.x < 20)
print a.upInPlace()