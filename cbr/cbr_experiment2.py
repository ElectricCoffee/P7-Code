from cbr import *
from dbm.udbm import *
from tioa.tioa import *
from symbolic_state.double_symbolic_state import *
from symbolic_state.location_vector import *
from tioa.automata_context import *
import time


c = Context(['x', 'y'], 'c')

t1 = TIOA(["a", "b"], "a", set(c.clocks),
          [Edge("a", "", Guard(c, (c['x'], 1000, '>')), set(), "b")], {}, {}, {})
t2 = TIOA(["c", "d"], "d", set(c.clocks),
          [Edge("c", "a", Guard(c, (c['y'], 1, '>')), set(), "d"),
           Edge("d", "b", Guard(c, (c['y'], 2, '>')), set([c['y']]), "c")], {}, {}, {"c":(c.y == 0), "d":(c.y == 1)})



autocon1 = AutomataContext([t1, t2])
autocon2 = AutomataContext([t1])

clocks = set()
for clock_name, clock in c.items():
    clocks.add(clock)



dssinit = DoubleSymbolicState(autocon1.ContextLocationVector(["a", "d"]), c.getTautologyFederation())
dssgoal = DoubleSymbolicState(autocon1.ContextLocationVector(["b", "*"]), c.getTautologyFederation())

time_start1 = time.time()
cbr(dssinit, dssgoal, [t1, t2], clocks)
time_end1 = time.time()

time_dif1 = (time_end1 - time_start1) * 1000
print("CBR with tick tock, time spent: " + str(time_dif1))



dssinit = DoubleSymbolicState(autocon2.ContextLocationVector(["a"]), c.getTautologyFederation())
dssgoal = DoubleSymbolicState(autocon2.ContextLocationVector(["b"]), c.getTautologyFederation())

time_start2 = time.time()
cbr(dssinit, dssgoal, [t1], clocks)
time_end2 = time.time()

time_dif2 = (time_end2 - time_start2) * 1000
print("CBR without tick tock, time spent: " + str(time_dif2))

factor = time_dif1 / time_dif2
print("Factor between with and without, factor: " + str(factor))
