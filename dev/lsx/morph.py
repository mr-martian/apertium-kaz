#!/usr/bin/env python3

import sys
from subprocess import *

with open('multi_analyzed.txt') as infile:
    txt = infile.read().splitlines()
with open('multi_split.txt', 'w') as outfile:
    for line in txt:
        words = line.split(':')[0].split()
        morph = []
        for w in words:
            proc = run(['apertium', '-d', '../..', 'kaz-morph'], input=w.encode('utf-8'), stdout=PIPE, stderr=DEVNULL)
            morph.append(proc.stdout.decode('utf-8'))
        outfile.write(line + '\t' + '\t'.join(morph) + '\n')
