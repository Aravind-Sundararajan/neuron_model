from neuron import h, gui
from matplotlib import pyplot

soma = h.Section(name='soma')
h.psection()
soma.insert('pas')
print("type(soma) = {}".format(type(soma)))
print("type(soma(0.5)) ={}".format(type(soma(0.5))))
mech = soma(0.5).pas
print(dir(mech))
asyn = h.AlphaSynapse(soma(0.5))
print("asyn.e = {}".format(asyn.e))
print("asyn.gmax = {}".format(asyn.gmax))
print("asyn.onset = {}".format(asyn.onset))
print("asyn.tau = {}".format(asyn.tau))
asyn.onset = 20
asyn.gmax = 1
h.psection()
v_vec = h.Vector()             # Membrane potential vector
t_vec = h.Vector()             # Time stamp vector
v_vec.record(soma(0.5)._ref_v)
t_vec.record(h._ref_t)
h.tstop = 40.0
h.run()

#plotting
pyplot.figure(figsize=(8,4)) # Default figsize is (8,6)
pyplot.plot(t_vec, v_vec)
pyplot.xlabel('time (ms)')
pyplot.ylabel('mV')
pyplot.show()
