#!/bin/python3

from micrograd.engine import *
from micrograd.nn import *


def dump(m, filename="params.py"):
    nout = []
    for l in range(len(m.layers)):
        if l == 0:
            nin = len(m.layers[l].neurons[0].w)
        nout.append(len(m.layers[l].neurons))

    with open(filename, "w") as f:
        f.write("from micrograd.engine import *")
        f.write("\n")
        f.write("from micrograd.nn import *")
        f.write("\n")
        f.write("\n")
        f.write("parameters = ")
        f.write(
            str(['Value(data=' + str(v.data) + ')' for v in m.parameters()]).replace("'", ""))
        f.write("\n")
        f.write("\n")
        f.write("def model():\n")
        f.write("\tmodel = MLP(" + str(nin) + ", " + str(nout) + ")\n")
        f.write("\tfor p, q in zip(model.parameters(), parameters):\n")
        f.write("\t\tp.data = q.data\n")
        f.write("\treturn model\n")
        f.write("\n")

