#!/usr/bin/env python3
"""
Grab equivalent bytes from BMP file
"""

import sys
import render

x = int(sys.argv[2])//8
y = int(sys.argv[3])//8

rangecount = int(sys.argv[4])

try:
	off = int(sys.argv[5])
except:
	off = 0

data = render.getbytes(sys.argv[1])

pre_offset = [render.render(data[y+(i%2)][x+(i//2)]) for i in range(rangecount)]

for i in pre_offset:
	for j in i:
		for w, k in enumerate(j):
			if k:
				j[w] = ((k-1+off)%3)+1

print('\n'.join(render.unrender(i) for i in pre_offset))
