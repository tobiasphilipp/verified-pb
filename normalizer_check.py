#
#normalized:
#check it is normalized:
#just 1 variable
#no negative coefficients
#check no weights to the left are greater than right
#
#after running SWC program:
#check there are no -- because the original variables are treated already with negation (remove them)

from subprocess import PIPE, Popen
import os

bench_dir = 'bench/'
normal_dir = 'bench_normal/'
faulty = []

for entry in os.listdir(bench_dir):
    print(entry)
    normals = []
    f = open(bench_dir + entry, 'r')
    line = f.readline()
    while line.startswith('*'):
        line = f.readline()
    while len(line) > 0:
        feed = line.replace(' x','*').replace(' >= ','<').replace(' ;','')
        #answer = p.communicate('2*1 -3*2<3\n')[0]
        p = Popen(["Normalizer"], stdin=PIPE, stdout=PIPE, bufsize=1)
        answer = p.communicate(feed)[0]
        normals += answer
        line = f.readline()
    f_out = open(normal_dir + entry, 'w')
    f_out.writelines(normals)
    f.close()
    f_out.close()
    break
