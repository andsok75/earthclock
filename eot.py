import json
import sys
from collections import defaultdict

eot_per_year = defaultdict(list)
lines = sys.stdin.read().split('\n')
for line in lines[lines.index('$$SOE')+1:lines.index('$$EOE')]:
    a = line.split()
    year = int(a[0].split('-')[0])
    s = float(a[-1])
    m = float(a[-2])
    h = float(a[-3])
    eot = (h + (m + s/60)/60 - 12)*60
    eot_per_year[year].append(round(eot, 2))

json.dump(eot_per_year, sys.stdout, separators=(',', ':'))
