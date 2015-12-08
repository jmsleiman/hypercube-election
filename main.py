#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014 Joseph M. Sleiman

# This program is free software; you can redistribute it and/or
# modify it under the terms of the LGPLv2.1 or LGPLv3 license.

import random
import math
import os.path
import time

import node
import hypercube

# build instructions
# ls | xargs -I {} dot -Tpng {} -o {}.png

def main():
	d = 4
	n = pow(2, d)
	nodeValues = range(n)
	random.shuffle(nodeValues)
	x = hypercube.HyperCube(d, nodeValues)
	results = x.electSmallest()
	
	
	now = time.localtime()
	out = "output-{0}{1}{2}{3}{4}{5}".format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
	
	
	if not os.path.exists(out):
		os.makedirs(out)
	
	for x in xrange(0, len(results)):
		location = os.path.join(out, "{0}.dot".format(x))
		
		with open(location, "w+") as f:
			f.write(results[x])
	
	
main()
