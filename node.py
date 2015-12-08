#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 Joseph M. Sleiman

# This program is free software; you can redistribute it and/or
# modify it under the terms of the LGPLv2.1 or LGPLv3 License.

import structlog
import random

log = structlog.get_logger()

class Node(object):
	def __init__(self, value, dimension):
		self.value = value
		self.rank = 0
		self.connections = [None]*dimension
		self.connectionsDelay = [random.randint(0,9)]*dimension
		self.dotLabel = self.value
		self.dotString = ""
		self.master = None
		self.masterEdge = -1
		self.bestScore = -1
		self.isDefeated = False
	
	def processMessage(self, msg, highWins):
		log.msg("duel", attacker=msg.value, defender=self.value)
		if(self.isDefeated):
			log.msg("forwarding challenge...", attacker=msg.value, defender=self.value, master=self.master.value)
			return self.forwardChallenge(msg)
		else:
			if(msg.rank > self.rank):
				return msg
			
			if(highWins):
				if(msg.value > self.value):
					self.setMaster(msg.source)
					log.msg("defeated", me=self.value, message=msg.value, master=self.master.value, master_edge=self.masterEdge)
					
					return None
					
				else:
					self.rank += 1
					log.msg("deflected", me=self.value, rank=self.rank)
					
					return self.createChallenge(self.rank)
				
			else:
				if(msg.value < self.value):
					self.setMaster(msg.source)
					log.msg("defeated", me=self.value, message=msg.value, master=self.master.value	, master_edge=self.masterEdge)
					
					return None
					
				else:
					self.rank += 1
					log.msg("deflected", me=self.value, rank=self.rank)
					
					return self.createChallenge(self.rank)
		
	
	def createChallenge(self, dimension):
		if(dimension == -1):
			return Message(self, self.connections[self.rank], self.rank, self.value, self.connectionsDelay[self.rank])
		elif(dimension > len(self.connections)):
			return None
		else:
			return Message(self, self.connections[dimension-1], self.rank, self.value, self.connectionsDelay[dimension-1])
	
	def setMaster(self, master):
		self.master = master
		self.masterEdge = self.rank
		self.isDefeated = True
	
	def forwardChallenge(self, msg):
		return Message(msg.source, self.master, msg.rank, msg.value, self.connectionsDelay[self.masterEdge])
	
	def attach(self, node, dimension):
		self.connections[dimension-1] = node
	
	def getNeighbour(self, dimension):
		return self.connections[dimension-1]
	
	def getDelay(self, dimension):
		return self.connectionsDelay[dimension-1]
	
	def __str__(self):
		return "Object Node:\n\tValue: {0}\n\tRank: {1}\n\tConnections: {2}\n\tAddress: {3}".format(self.value, self.rank, self.connections, hex(id(self)))
		
	def toDot(self):
		# dunno some kind of wordfinder??
		'''
		self.base10DigitsInEnglish = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
		v = self.value
		label = ""
		while(v > 9):
			label = label + self.base10DigitsInEnglish[(v % 10)]
			v = v / 10
		'''
		colourList = ['"#707030"', '"#00ee00"', '"#009000"', '"#00eeee"', '"#00a0a0"', '"#0000ff', '"#000080', '"#ff00ff', '"#900090', '"#ff0000"', '"#800000"', '"#ffff00"']
		
		style = "circle"
		if(self.isDefeated):
			style = "rectangle"
		
		self.dotString = '\t{0}[label="{1}", shape="{2}"]\n'.format(self.dotLabel, self.value, style)
		i = 0
		for n in self.connections:
			self.dotString = self.dotString + "\t\t{0} -> {1} [color={2}] \n".format(self.dotLabel, n.dotLabel, colourList[i])
			i += 1
		# ok but we also need to consider all the connections
		
		if(self.isDefeated):
			self.dotString = self.dotString + '\t\t{0} -> {1} [color="red"]\n'.format(self.dotLabel, self.master.dotLabel)
		
		return self.dotString
	
	
class Message(object):
	def __init__(self, source, destination, rank, value, delay):
		self.source = source
		self.destination = destination
		self.rank = rank
		self.value = value
		self.delay = delay
	
	def __str__(self):
		return "<Source: [{0}]\tDestination: [{1}]\tRank: {2}\tValue: {3}\tDelay: {4}>".format(self.source.value, self.destination.value, self.rank, self.value, self.delay)