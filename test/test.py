import sys
sys.path.insert(0, '../')
from udbm import Context
c = Context(["x", "y", "z"], "d") 
a = (c.x < 10) & (c.x - c.y > 1)
b = (c.x < 20)
print a <= b    # is a included in b
print a >= b    # is b included in a
print a.up() | b
print a | b
