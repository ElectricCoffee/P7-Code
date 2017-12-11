from cbr import *
from dbm.udbm import *
from tioa.tioa import *
from symbolic_state.double_symbolic_state import *
from symbolic_state.location_vector import *
from tioa.automata_context import *
import time


c = Context(['x', 'y'], 'c')

t1 = TIOA(["a", "b"], "a", set(c.clocks),
          [Edge("a", None, Guard(c, (c['x'], 1, '<=')), set(), "b")], set(), set(), {})
t2 = TIOA(["c"], "c", set(c.clocks),
          [Edge("c", None, Guard(c, (c['y'], 1, '>=')), set([c['y']]), "c")], set(), set(), {"c":(c.y >= 0) & (c.y <= 1)})



autocon1 = AutomataContext([t2, t1])
autocon2 = AutomataContext([t1])

clocks = set()
for clock_name, clock in c.items():
    clocks.add(clock)


dssinit1 = DoubleSymbolicState(autocon1.ContextLocationVector(["c", "a"]), c.getTautologyFederation())
dssgoal1 = DoubleSymbolicState(autocon1.ContextLocationVector(["c", "b"]), ((c.y > 1000) & (c.x <= 1)))

dssinit2 = DoubleSymbolicState(autocon2.ContextLocationVector(["a"]), c.getTautologyFederation())
dssgoal2 = DoubleSymbolicState(autocon2.ContextLocationVector(["b"]), ((c.y > 1000)))



print("How many iterations should the CBR run? ")
nr = int(input())
time_dif1 = 0
time_dif2 = 0

for x in range(0, nr):
    time_start1 = time.clock()
    cbr(dssinit1, dssgoal1, [t2, t1], clocks)
    time_end1 = time.clock()

    time_dif1 += (time_end1 - time_start1)

    time_start2 = time.clock()
    cbr(dssinit2, dssgoal2, [t1], clocks)
    time_end2 = time.clock()

    time_dif2 += (time_end2 - time_start2)

print("Factor between with and without, factor: " + str(time_dif1 / time_dif2))
print("Difference between with and without, diff: " + str((time_dif1 - time_dif2)/nr))
