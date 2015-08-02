#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014 Joseph M. Sleiman

# This program is free software; you can redistribute it and/or
# modify it under the terms of the MIT/X11 License.

import random
import math
import node
import hypercube

def main():
	d = 3
	n = pow(2, d)
	nodeValues = range(n)
	random.shuffle(nodeValues)
	x = hypercube.HyperCube(d, nodeValues)
	
main()
