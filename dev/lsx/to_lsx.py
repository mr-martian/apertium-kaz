#!/usr/bin/env python3

import sys
from subprocess import *

lsx_frame = '''<?xml version="1.0" encoding="UTF-8"?>
<dictionary type="sequential">
  <alphabet>abcdefghijklmnopqrstuvwxyz</alphabet>
  <sdefs>
    %s
  </sdefs>

  <section id="main" type="standard">
    %s
  </section>
</dictionary>
'''

sdefs = set()

with open('multi_no_star.txt') as infile:
    txt = infile.read().splitlines()

def make_entry(join, parts):
    global sdefs
    ls = []
    found = False
    tags = '<' + join.split('<', 1)[-1]
    join_lem = join.split(':')[-1].split('<')[0]
    lsx_lem = join_lem.replace(' ', '<b/>')
    for p in reversed(parts):
        readings = p.split('/')[1:]
        if not readings:
            print(join)
            print(parts)
        if not found and tags in p:
            for r in readings:
                if tags in r:
                    found = True
                    lem = r.split('<')[0]
                    first_tag = r.split('<')[1].split('>')[0]
                    sdefs.add(first_tag)
                    ln = f'<p><l>{lem}<s n="{first_tag}"/></l><r>{lsx_lem}<s n="{first_tag}"/></r></p><i><t/><j/></i>'
                    ls.append(ln)
                    break
        else:
            r = readings[0]
            lem = r.split('<')[0]
            first_tag = r.split('<')[1].split('>')[0]
            sdefs.add(first_tag)
            ln = f'<p><l>{lem}<s n="{first_tag}"/><t/><j/></l><r></r></p>'
            ls.append(ln)
    if not found:
        return None
    else:
        blob = '\n      '.join(reversed(ls))
        return f'<e lm="{join_lem}">\n      {blob}\n    </e>'

ents = []
with open('multi_hard.txt', 'w') as fail_file:
    for ln in txt:
        sp = ln.strip().split('\t')
        res = make_entry(sp[0], sp[1:])
        if res:
            ents.append(res)
        else:
            fail_file.write(ln + '\n')
with open('../../apertium-kaz.kaz.lsx', 'w') as lsx_file:
    lsx_file.write(lsx_frame % ('\n    '.join('<sdef n="%s"/>' % x for x in sdefs), '\n    '.join(ents)))
