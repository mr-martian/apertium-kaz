#!/bin/bash

tail -n +1952 ../../apertium-kaz.kaz.lexc | grep "% " | sed 's/%//g' | sed -E 's/:.*//' > multi.txt
./extract.py
./morph.py
./to_lsx.py
