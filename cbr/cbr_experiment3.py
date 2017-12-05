from cbr import *
from dbm.udbm import *
from tioa.tioa import *
from symbolic_state.double_symbolic_state import *
from symbolic_state.location_vector import *
from tioa.automata_context import *
import time


c = Context(['x', 'y'], 'c')

t1 = TIOA(["a", "b"], "a", set(c.clocks),
          [Edge("a", None, Guard(c, (c['x'], 1000, '>')), set(), "b")], set(), set(), {})
t2 = TIOA(["c"], "c", set(c.clocks),
          [Edge("c", None, Guard(c, (c['y'], 1, '>=')), set([c['y']]), "c")], set(), set(), {"c":(c.y >= 0) & (c.y <= 1)})



autocon1 = AutomataContext([t1, t2])
autocon2 = AutomataContext([t1])

clocks = set()
for clock_name, clock in c.items():
    clocks.add(clock)


dssinit1 = DoubleSymbolicState(autocon1.ContextLocationVector(["a", "c"]), c.getTautologyFederation())
dssgoal1 = DoubleSymbolicState(autocon1.ContextLocationVector(["b", "*"]), c.getTautologyFederation())

dssinit2 = DoubleSymbolicState(autocon2.ContextLocationVector(["a"]), c.getTautologyFederation())
dssgoal2 = DoubleSymbolicState(autocon2.ContextLocationVector(["b"]), c.getTautologyFederation())


resfactor = 0
print("How many iterations should the CBR run? ")
nr = int(input())

for x in range(0, nr):
    time_start1 = time.time()
    cbr(dssinit1, dssgoal1, [t1, t2], clocks)
    time_end1 = time.time()

    time_dif1 = (time_end1 - time_start1)

    time_start2 = time.time()
    cbr(dssinit2, dssgoal2, [t1], clocks)
    time_end2 = time.time()

    time_dif2 = (time_end2 - time_start2)
    resfactor += time_dif1 / time_dif2
print("Factor between with and without, factor: " + str(resfactor / nr))
