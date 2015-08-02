#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 Joseph M. Sleiman

# This program is free software; you can redistribute it and/or
# modify it under the terms of the LGPLv2.1 or LGPLv3 License.

class Node(object):
	def __init__(self, value, dimension):
		self.value = value
		self.rank = 0
		self.connections = [None]*dimension
		self.dotLabel = ""
	
	def processMessage(self, msg):
		pass
	
	def createMessage(self, context):
		pass
	
	def attach(self, node, dimension):
		self.connections[dimension-1] = node
	
	def __str__(self):
		return "Object Node:\n\tValue: {0}\n\tRank: {1}\n\tConnections: {2}\n\tAddress: {3}".format(self.value, self.rank, self.connections, hex(id(self)))
		
	def toDot(self):
		self.base10DigitsInEnglish = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
		v = self.value
		label = ""
		while(v > 9):
			label = label + self.base10DigitsInEnglish[(v % 10)]
			v = v / 10
		# self.dotLabel = label
		return '{0}[\n\tlabel="{1}"]'.format(self.dotLabel, self.value)
	]
	
