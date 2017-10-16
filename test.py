import sys
sys.path.insert(0, '../')
from python_dbm import Context
c = Context(["x", "y", "z"], "c") 
a = (c.x < 10) & (c.x - c.y > 1)
b = (c.x < 20)
print a <= b    # is a included in b
print a >= b    # is b included in a
print a.up() | b
print a | b
