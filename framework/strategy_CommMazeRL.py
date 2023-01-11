#!/usr/bin/env python3

#Author: Ehsan Latif

from strategy import Strategy
from network import NetworkInterface
from time import sleep
import random


class StrategyCommMazeRL(Strategy):
	mouse = None
	qTable = {}
	network = None
	alpha = 0.5
	gamma = 0.9

	def __init__(self, mouse):
		self.mouse = mouse
		self.qTable = {}
		self.network = NetworkInterface()
		self.network.initSocket()
		self.network.startReceiveThread()
		self.createQTable()

	def checkFinished(self):
		return self.mouse.isFinished()
	def createQTable(self):
        self.q_table = {(i, j): {a: 0.0 for a in self.actions} for i in range(self.mouse.mazeMap.width) for j in range(self.mouse.mazeMap.height)}

	def go(self):
		self.mouse.senseWalls()
		state = str(self.mouse.x)+'_'+str(self.mouse.y)
		sendData = {'x': self.mouse.x, 'y':self.mouse.y, 'up': not self.mouse.canGoUp(), 'down': not self.mouse.canGoDown(), 'left': not self.mouse.canGoLeft(), 'right': not self.mouse.canGoRight(),'q_value'}
		self.network.sendStringData(sendData)
		recvData = self.network.retrieveData()
		while recvData:
			otherMap = recvData['data']
			cell = self.mouse.mazeMap.getCell(otherMap['x'], otherMap['y'])
			if otherMap['up']: self.mouse.mazeMap.setCellUpAsWall(cell)
			if otherMap['down']: self.mouse.mazeMap.setCellDownAsWall(cell)
			if otherMap['left']: self.mouse.mazeMap.setCellLeftAsWall(cell)
			if otherMap['right']: self.mouse.mazeMap.setCellRightAsWall(cell)
			recvData = self.network.retrieveData()

		actionList = []
		if self.mouse.canGoUp():
			actionList.append('up')
		if self.mouse.canGoDown():
			actionList.append('down')
		if self.mouse.canGoLeft():
			actionList.append('left')
		if self.mouse.canGoRight():
			actionList.append('right')

		if state in self.qTable:
			maxQ = -99999
			maxAction = None
			for action in actionList:
				if self.qTable[state][action] > maxQ:
					maxQ = self.qTable[state][action]
					maxAction = action
		else:
			maxAction = random.choice(actionList)

		if maxAction == 'up':
			self.mouse.goUp()
		elif maxAction == 'down':
			self.mouse.goDown()
		elif maxAction == 'left':
			self.mouse.goLeft()
		elif maxAction == 'right':
			self.mouse.goRight()

		nextState = str(self.mouse.x)+'_'+str(self.mouse.y)
		if nextState not in self.qTable:
			self.qTable[nextState] = {'up': 0, 'down': 0, 'left': 0, 'right': 0}

		self.qTable[state][maxAction] = (1-self.alpha) * self.qTable[state][maxAction] + self.alpha * (self.mouse.getReward() + self.gamma * max(self.qTable[nextState].values()))
		sendData = {'max_action':maxAction, 'q_value':self.qTable[state][maxAction]}
		self.network.sendStringData(sendData)
		sleep(0.5)