#!/usr/bin/env python3

import sys
from subprocess import *

dix_frame = '''<?xml version="1.0" encoding="UTF-8"?>
<dictionary>
<alphabet>xyz</alphabet>
<sdefs><sdef n="n"/></sdefs>
<section id="main" type="standard">
%s
</section>
</dictionary>
'''


def process_word(word):
    prt = word.strip().split()
    ent1 = '<e><p><l>' + '<b/>'.join(prt) + '</l><r>blah</r></p></e>'
    ent2 = '<e><p><l>' + prt[0] + '<g><b/>' + '<b/>'.join(prt[1:]) + '</g></l><r>blah</r></p></e>'
    with open('temp.dix', 'w') as file:
        file.write(dix_frame % (ent1+ent2))
    run(['lt-comp', 'lr', 'temp.dix', 'temp.bin'], stdout=DEVNULL, stderr=DEVNULL)
    run(['lt-trim', '../../kaz.automorf.bin', 'temp.bin', 'temp2.bin'], stdout=DEVNULL, stderr=DEVNULL)
    run(['lt-print', '-H', 'temp2.bin', 'temp.att'], stdout=DEVNULL, stderr=DEVNULL)
    run(['hfst-txt2fst', 'temp.att', '-o', 'temp.hfst'], stdout=DEVNULL, stderr=DEVNULL)
    proc = run(['hfst-expand', '-n', '1', 'temp.hfst'], stdout=PIPE, stderr=DEVNULL)
    return proc.stdout.decode('utf-8')

with open('multi.txt') as infile:
    txt = infile.read()
with open('multi_analyzed.txt', 'w') as outfile:
    for word in txt.splitlines():
        if '<' not in word:
            outfile.write(process_word(word).strip() + '\n')
