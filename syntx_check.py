#input:
#check the header is correct

import os

bench_dir = 'bench/'

for entry in os.listdir(bench_dir):
    f = open(bench_dir + entry, 'r')
    head = f.readline().split('#')
    nvar = int(head[1].split('=')[-1].strip())
    nconstr = int(head[2].split('=')[-1].strip())
    line = f.readline()
    while line.find('*') != -1:
        line = f.readline()
    real_ncons = 0
    x_max = 0
    while len(line) > 0:
        real_ncons += 1
        var_nums = [int(x[1:]) for x in line.split(' ') if x.find('x') != -1]
        x_max = max(x_max, *var_nums)
        line = f.readline()
    assert x_max == nvar
    assert nconstr == real_ncons


