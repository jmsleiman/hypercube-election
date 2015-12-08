#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 Joseph M. Sleiman

# This program is free software; you can redistribute it and/or
# modify it under the terms of the LGPLv2.1 or LGPLv3 License.

import random

import structlog
log = structlog.get_logger()

class Node(object):
	def __init__(self, value, dimension):
		self.value = value
		self.rank = 0
		self.connections = [None]*dimension
		self.connectionsDelay = [random.randint(0,9)]*dimension
		self.dotLabel = self.value
		self.dotString = ""
		self.queen = None
		self.queenEdge = -1
		self.bestScore = -1
		self.isDefeated = False
	
	def processMessage(self, msg, highWins):
		log.msg("duel", attacker=msg.value, defender=self.value)
		if(self.isDefeated):
			log.msg("forwarding challenge...", attacker=msg.value, defender=self.value, queen=self.queen.value)
			return self.forwardChallenge(msg)
		else:
			if(msg.rank > self.rank):
				return msg
			
			if(highWins):
				if(msg.value > self.value):
					self.setQueen(msg.source)
					log.msg("defeated", me=self.value, message=msg.value, queen=self.queen.value, queen_edge=self.queenEdge)
					
					return None
					
				else:
					self.rank += 1
					log.msg("deflected", me=self.value, rank=self.rank)
					
					return self.createChallenge(self.rank)
				
			else:
				if(msg.value < self.value):
					self.setQueen(msg.source)
					log.msg("defeated", me=self.value, message=msg.value, queen=self.queen.value	, queen_edge=self.queenEdge)
					
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
	
	def setQueen(self, queen):
		self.queen = queen
		self.queenEdge = self.rank
		self.isDefeated = True
	
	def forwardChallenge(self, msg):
		return Message(msg.source, self.queen, msg.rank, msg.value, self.connectionsDelay[self.queenEdge])
	
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
		colourList =  ['"#000000"', '"#FFFF00"', '"#1CE6FF"', '"#FF34FF"', '"#FF4A46"', '"#008941"', '"#006FA6"', '"#A30059"',
'"#FFDBE5"', '"#7A4900"', '"#0000A6"', '"#63FFAC"', '"#B79762"', '"#004D43"', '"#8FB0FF"', '"#997D87"',
'"#5A0007"', '"#809693"', '"#FEFFE6"', '"#1B4400"', '"#4FC601"', '"#3B5DFF"', '"#4A3B53"', '"#FF2F80"',
'"#61615A"', '"#BA0900"', '"#6B7900"', '"#00C2A0"', '"#FFAA92"', '"#FF90C9"', '"#B903AA"', '"#D16100"',
'"#DDEFFF"', '"#000035"', '"#7B4F4B"', '"#A1C299"', '"#300018"', '"#0AA6D8"', '"#013349"', '"#00846F"',
'"#372101"', '"#FFB500"', '"#C2FFED"', '"#A079BF"', '"#CC0744"', '"#C0B9B2"', '"#C2FF99"', '"#001E09"',
'"#00489C"', '"#6F0062"', '"#0CBD66"', '"#EEC3FF"', '"#456D75"', '"#B77B68"', '"#7A87A1"', '"#788D66"',
'"#885578"', '"#FAD09F"', '"#FF8A9A"', '"#D157A0"', '"#BEC459"', '"#456648"', '"#0086ED"', '"#886F4C"',
'"#34362D"', '"#B4A8BD"', '"#00A6AA"', '"#452C2C"', '"#636375"', '"#A3C8C9"', '"#FF913F"', '"#938A81"',
'"#575329"', '"#00FECF"', '"#B05B6F"', '"#8CD0FF"', '"#3B9700"', '"#04F757"', '"#C8A1A1"', '"#1E6E00"',
'"#7900D7"', '"#A77500"', '"#6367A9"', '"#A05837"', '"#6B002C"', '"#772600"', '"#D790FF"', '"#9B9700"',
'"#549E79"', '"#FFF69F"', '"#201625"', '"#72418F"', '"#BC23FF"', '"#99ADC0"', '"#3A2465"', '"#922329"',
'"#5B4534"', '"#FDE8DC"', '"#404E55"', '"#0089A3"', '"#CB7E98"', '"#A4E804"', '"#324E72"', '"#6A3A4C"']
		
		style = "circle"
		if(self.isDefeated):
			style = "rectangle"
		
		
		self.dotString = '\t{0}[label="{1} ({3})", shape="{2}"]\n'.format(self.dotLabel, self.value, style, self.rank)
		i = 0
		for n in self.connections:
			if(i == self.queenEdge):
				self.dotString = self.dotString + "\t\t{0} -> {1} [color={2}, arrowhead=odiamond] \n".format(self.dotLabel, n.dotLabel, colourList[i])
			else:
				self.dotString = self.dotString + "\t\t{0} -> {1} [color={2}] \n".format(self.dotLabel, n.dotLabel, colourList[i])
			i += 1
		# ok but we also need to consider all the connections
		
		return self.dotString
	
	
class Message(object):
	def __init__(self, source, destination, rank, value, delay):
		self.source = source
		self.destination = destination
		self.rank = rank
		self.value = value
		self.delay = delay
	
	def toDot(self):
		return '\t\t{0} -> {1} [color="black", style=dashed]\n'.format(self.source.dotLabel, self.destination.dotLabel)
	
	def __str__(self):
		return "<Source: [{0}]\tDestination: [{1}]\tRank: {2}\tValue: {3}\tDelay: {4}>".format(self.source.value, self.destination.value, self.rank, self.value, self.delay)