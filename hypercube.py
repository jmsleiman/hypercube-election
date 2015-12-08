#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 Joseph M. Sleiman

# This program is free software; you can redistribute it and/or
# modify it under the terms of the LGPLv2.1 or LGPLv3 License.

import math
import node
import structlog

log = structlog.get_logger()

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
	
	def electSmallest(self):
		'''
		In this scenario, the nodes must find the smallest node among them, and name it their leader.
		Strategy:
			- Each node must message its neighbour on the i edge:
				message contains:
					rank
					value
			- When an active node receives a message:
				- If the message received is from a smaller rank, there's been a catastrophic bug.
				- If the message received is from an equal rank:
					- If the receiver has a higher value, it increments its rank
					- If the receiver has a lower value, it points the master variable to the edge that sent the message, and goes dormant
				- If the message received is from a higher rank:
					- The node pushes it to a queue and comes back to it when it's ready (ie when the rank matches)
			- When a passive node receives a message:
				- If the message contains a rank lower than the rank of your master, switch alliances
		'''
		
		messageMatrix = []
		
		for node in self.listOfNodes:
			messageMatrix.append(node.createChallenge(0))
		
		clock = 0
		victor = None
		dots = []
		
		while(victor == None):
			dots.append(self.toDot())
			clock = clock + 1
			messagesToProcess = []
			messagesToQueue = []
			
			while( len(messageMatrix) > 0):
				if(messageMatrix[0].delay <= 0):
					messagesToProcess.append(messageMatrix.pop(0))
				else:
					messagesToQueue.append(messageMatrix.pop(0))
			
			# now it's time to process messages
			while(len(messagesToProcess) > 0):
				msg = messagesToProcess.pop(0)
				
				# however, how do we account for a redirected challenge?
				# and how do we account for a success, defeat?
				toBeContinued = msg.destination.processMessage(msg, False)
				if(toBeContinued != None):
					messageMatrix.append(toBeContinued)
				
				
			# now it's time to requeue those messages
			for msg in messagesToQueue:
				messageMatrix.append(msg)
			
			for msg in messageMatrix:
				msg.delay -= 1
			
			for node in self.listOfNodes:
				if node.rank == self.dimension:
					print "Winner! {0}".format(node)
					victor = node
					break
			
		
		return dots
	
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
