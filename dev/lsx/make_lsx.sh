#!/bin/bash

tail -n +1952 ../../apertium-kaz.kaz.lexc | grep "% " | sed 's/%//g' | sed -E 's/:.*//' > multi.txt
./extract.py
./morph.py
grep "*" multi_split.txt > multi_star.txt
grep -v "*" multi_split.txt > multi_no_star.txt
./to_lsx.py
