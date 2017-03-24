import os
import subprocess
from subprocess import call
import re

eq_cnt = 0

readable_str = ''

def apply_swc(filename):
    eq_file = open(filename)
    big_result = ''
    #for each constraint (sharing same Xes)
    for line in eq_file:
        lhs, rhs = line.partition("<=")[::2]
        lhs = lhs.rstrip().split(' ')
        #SWC will give the Xes by the order in constr
        ord_dict = dict(('x'+str(x[0]+1), x[1].split('*')[1]) for x in enumerate(lhs))
        #feed for SWC in the form ./SWC $num_of_vars $rhs $[coeff of constraints]
        com_line = './SWC2 ' + str(len(lhs)) + ' ' + rhs.strip() + ' ' + ' '.join([x.split('*')[0] for x in lhs])
        swc_out = subprocess.Popen(com_line.split(" "), stdout=subprocess.PIPE).communicate()[0]
        #back to original Xes + remove double negation
        pattern = re.compile(r'\b(' + '|'.join(ord_dict.keys()) + r')\b')
        big_result += pattern.sub(lambda x: ord_dict[x.group()], swc_out).replace('--','')
    return [x[:-1].rstrip() for x in big_result.split('\r\n')[:-1]]

def form_dimacs(cnfs):
    constr_num = len(cnfs)
    all_conjuncts = (' '.join(cnfs)).split(' ')
    #get the maximal X index (X is an original variable)
    max_x = max([int(conj.split('x')[1]) for conj in all_conjuncts if 'x' in conj])
    #S are then getting the numbers after the maximal X
    all_s = set('s' + conj.split('s')[1] for conj in all_conjuncts if 's' in conj)
    s_to_num = dict((str(s[0] + max_x + 1), s[1]) for s in enumerate(all_s))
    num_to_s = dict((s[1],s[0]) for s in s_to_num.items())
    pattern = re.compile(r'\b(' + '|'.join(num_to_s.keys()) + r')\b')
    #format "p cnf $num_vars $num_constrs"
    header = 'p cnf '+ str(max_x + len(all_s)) + ' ' + str(len(cnfs)) + '\n'
    dimacs_file = [header]
    for constr in cnfs:
        dimacs_file += [pattern.sub(lambda x: num_to_s[x.group()], constr).replace('x','') + ' 0\n']
    print(dimacs_file)

cnfs = apply_swc('bench_normal/tr.txt')
form_dimacs(cnfs)