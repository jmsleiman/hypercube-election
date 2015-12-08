#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014 Joseph M. Sleiman

# This program is free software; you can redistribute it and/or
# modify it under the terms of the LGPLv2.1 or LGPLv3 license.

import random
import math
import os.path
import time
import sys

import node
import hypercube

# build instructions
# ls | xargs -I {} dot -Tpng {} -o {}.png

def main(d, largestWins):
	n = pow(2, d)
	nodeValues = range(n)
	random.shuffle(nodeValues)
	x = hypercube.HyperCube(d, nodeValues)
	results = x.election(largestWins)
	
	# details for prettifying the output
	
	now = time.localtime()
	out = "output-{0}{1}{2}-{3}{4}{5}".format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
	zeroFillFactor = int(math.floor(math.log(len(results), 10)) + 1) + len(".dot")
	
	if not os.path.exists(out):
		os.makedirs(out)
	
	for x in xrange(0, len(results)):
		location = os.path.join(out, "{0}.dot".format(x).zfill(zeroFillFactor))
		
		with open(location, "w+") as f:
			f.write(results[x])
	
if __name__ == "__main__":
	try:
		d = int(sys.argv[1])
		hl = sys.argv[2]
		
		if(hl.lower() == "high"):
			main(d, True)
		elif (hl.lower() == "low"):
			main(d, False)
		else:
			raise Exception("Election choice invalid")
	
	except ValueError:
		print "usage: main.py [int: dimension of the hypercube] [high/low: elect highest/lowest]"