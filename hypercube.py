#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 Joseph M. Sleiman

# This program is free software; you can redistribute it and/or
# modify it under the terms of the LGPLv2.1 or LGPLv3 License.

import math
import node

class HyperCube(object):
	def __init__(self, dimension, nodeValues):
		###                                   define variables
		self.dimension = dimension
		self.listOfNodes = []
		self.messageRegistry = []
		self.dotString = ""
		
		###                                   do some setting up
		###     add in those values as nodes
		
		for value in nodeValues:
			self.listOfNodes.append(node.Node(value, self.dimension))
		
		self.setConnections(self.listOfNodes)
		
		for entry in self.listOfNodes:
			print str(entry)
		
	def setConnections(self, entry):
		'''this method splits the list of entries into smaller and
		smaller sublists until a list of 2 nodes is reached.
		
		those 2 nodes form a connection in dimension 1, and after that
		the other lists are superimposed and forms connections
		accordingly:
		
		0 1 2 3
		4 5 6 7
		
		0 and 4, 1 and 5, 2 and 6, 3 and 7 all form connections together
		in dimension 3 (as this list has 8 elements, 2^3 = 8...)
		a convenient coincidence... ;)
		'''
		
		if(len(entry) > 2):
			left, right = split_list(entry)
			self.setConnections(left)
			self.setConnections(right)
			
			for x in xrange(0, len(left)):
				left[x].attach(right[x], int(math.log(len(entry),2)))
				right[x].attach(left[x], int(math.log(len(entry),2)))
		
		if(len(entry) == 2):
			entry[0].attach(entry[1], 1)
			entry[1].attach(entry[0], 1)
	
	def toDot(self):
		text = "digraph {\n\tlayout = circo\n"
		for entry in self.listOfNodes:
			text = text + entry.toDot()
			
		text = text + "}"
		self.dotString = text
		return self.dotString
		# now we need to draw all the leader directions...
		# woohoo...
		
		
	
def split_list(a_list):
	half = len(a_list)/2
	return a_list[:half], a_list[half:]
