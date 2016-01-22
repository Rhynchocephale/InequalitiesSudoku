# -*- coding: utf-8 -*-

import itertools
#from time import sleep
import numpy as np
from random import randint
import multiprocessing as mp
import Queue
import threading

numbers = '123456789'
setOfNumbers = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

subsquares = [[0, 0], [0, 3], [0, 6], [3, 0], [3, 3], [3, 6], [6, 0], [6, 3], [6, 6]]
adjacentCases = {(0, 0): [[0, 1], [1, 0]], (0, 1): [[0, 0], [0, 2], [1, 1]], (0, 2): [[0, 1], [1, 2]],
(1, 0): [[0, 0], [1, 1], [2, 0]], (1, 1): [[1, 0], [0, 1], [2, 1], [1, 2]], (1, 2): [[1, 1], [2, 0], [2, 2]],
(2, 0): [[1, 0], [2, 1]], (2, 1): [[1, 1], [2, 0], [2, 2]], (2, 2): [[2, 1], [1, 2]]}

#Olivia
ineqHori = [[1, 0, 1, 0, 0, 0], [1, 0, 0, 1, 0, 0], [1, 1, 1, 0, 0, 1], [0, 1, 0, 1, 0, 1], [0, 0, 1, 1, 0, 1], [1, 1, 0, 1, 1, 0], [0, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 1, 0, 0, 1, 1]]
ineqVert = [[1, 1, 0, 0, 0, 1, 1, 1, 1], [0, 0, 1, 0, 1, 1, 1, 0, 1], [1, 1, 0, 0, 1, 0, 0, 0, 1], [0, 0, 1, 1, 0, 1, 0, 1, 0], [1, 1, 1, 0, 0, 1, 0, 1, 0], [0, 0, 0, 1, 1, 0, 1, 1, 1]]

#Clement

#inequalities, line by line. 0 for <, 1 for >
#ineqHori = [[0, 1, 0, 0, 0, 1], [1, 0, 0, 1, 1, 1], [0, 1, 1, 1, 0, 1], [1, 1, 1, 1, 0, 1], [1, 0, 0, 1, 0, 1], [1, 1, 0, 0, 1, 0], [1, 0, 1, 0, 1, 0], [1, 1, 0, 1, 1, 0], [0, 1, 0, 1, 0, 0]]
#line by line, 0 for ^, 1 for v
#ineqVert = [[1, 1, 0, 0, 0, 1, 0, 1, 1], [1, 0, 1, 0, 1, 1, 1, 0, 0], [0, 1, 0, 1, 1, 0, 0, 0, 1], [1, 0, 0, 1, 1, 0, 1, 1, 0], [1, 1, 1, 0, 0, 1, 1, 1, 0], [1, 0, 0, 1, 1, 1, 1, 0, 1]]

clues = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [4, 1, 9, 5, 7, 6, 2, 3, 8], [8, 6, 2, 9, 3, 4, 1, 7, 5], [2, 7, 6, 4, 9, 1, 5, 8, 3], [1, 4, 8, 7, 5, 3, 6, 9, 2], [9, 5, 3, 6, 8, 2, 7, 1, 4], [7, 8, 4, 1, 2, 9, 3, 5, 8], [3, 2, 1, 8, 6, 5, 9, 4, 7], [6, 9, 5, 3, 4, 7, 8, 2, 1]]
unclues = [[set() for x in range(9)] for x in range(9)]
emptyValue_unclues = set([0]) #setOfNumbers


def addUnclue(row, col, val):
	global unclues
	global clues
	
	if unclues[row][col] != emptyValue_unclues:
		unclues[row][col].add(val)
		if len(unclues[row][col]) == 8:
			clues[row][col] = list(setOfNumbers-unclues[row][col])[0]
			unclues[row][col] = emptyValue_unclues
			
	return 0

def countUnclues()
	global unclues
	
	num = 0
	
	for row in range(9):
		for col in range(9):
			if unclues[row][col] != emptyValue_unclues:
				num += len(unclues[row][col])
			else:
				num += 9
	
	return num

#to add: if two numbers can only be in two cases (in a subsquare, row/col), nothing else there
#puts emptyValue_unclues in unclues if clues not zero
def initUnclues():
	global unclues
	
	for row in range(9):
		for col in range(9):
			if clues[row][col]:
				unclues[row][col] = emptyValue_unclues
				
	return 0


def uncluesRowCol():
	global unclues
		
	#if X is present in clues[a][b], adds X to unclues[:][b] and unclues[a][:]
	for xClues in range(9):
		for yClues in range(9):
			if clues[xClues][yClues]:
				for rowCol in range(9):
					if unclues[xClues][rowCol] != emptyValue_unclues:
						addUnclue(xClues, rowCol, clues[xClues][yClues])
					if unclues[rowCol][yClues] != emptyValue_unclues:
						addUnclue(rowCol, yClues, clues[xClues][yClues])
	
	#checks if unclues makes it only possible for one number to be in a single row/column in a subsquare
	for subsquare in subsquares:
		for num in range(1,10):
			setOfRows = set()
			setOfCols = set()
			for row in [x+subsquare[0] for x in range(3)]:
				for col in [x+subsquare[1] for x in range(3)]:
					if unclues[row][col] != emptyValue_unclues and not num in unclues[row][col]:
						setOfRows.add(row)
						setOfCols.add(col)
			if len(setOfRows) == 1:
				row = list(setOfRows)[0]
				for x in [x for x in range(9) if not x in [x+subsquare[1] for x in range(3)]]:
					if unclues[row][x] != emptyValue_unclues:
						addUnclue(row, x, num)
			if len(setOfCols) == 1:
				col = list(setOfCols)[0]
				for x in [x for x in range(9) if not x in [x+subsquare[0] for x in range(3)]]:
					if unclues[x][col] != emptyValue_unclues:
						addUnclues(x, col, num)
	
	return 0
	
def uncluesSquare():
	
	for subsquare in subsquares:
		for row in [x + subsquare[0] for x in range(3)]:
			for col in [x + subsquare[1] for x in range(3)]:
				#if contains a number, not possible to have it anywhere else on the subsquare
				if clues[row][col]:
					for row2 in [x + subsquare[0] for x in range(3)]:
						for col2 in [x + subsquare[1] for x in range(3)]:
							if unclues[row2][col2] != emptyValue_unclues:
								addUnclue(row2, col2, clues[row][col])
	
	return 0
		
def uncluesIneq():
	global unclues
	
	for subsquare in subsquares:
		found = 1
		while found > 0:
			found = 0
			i = 0
			for relativeRow in range(3):
				absoluteRow = relativeRow + subsquare[0]
				for relativeCol in range(3):					
					absoluteCol = relativeCol + subsquare[1]
					if unclues[absoluteRow][absoluteCol] == emptyValue_unclues:
						continue
					
					smallerThan = set()
					greaterThan = set()
					for relativeAdjacentCase in adjacentCases[(relativeRow, relativeCol)]:
						absoluteAdjacentRow = relativeAdjacentCase[0] + subsquare[0]
						absoluteAdjacentCol = relativeAdjacentCase[1] + subsquare[1]
						#if case > adjacent 
						if getIneq(absoluteRow, absoluteCol, absoluteAdjacentRow, absoluteAdjacentCol):
							#get smallest number that is neither in unclues nor in greaterThan
							#ADDED CASE OF ALREADY KNOWN CLUE
							if unclues[absoluteAdjacentRow][absoluteAdjacentCol] != emptyValue_unclues:
								greaterThan.add(min((setOfNumbers-unclues[absoluteAdjacentRow][absoluteAdjacentCol])-greaterThan))
							else:
								greaterThan.add(clues[absoluteAdjacentRow][absoluteAdjacentCol])
						else:
							if unclues[absoluteAdjacentRow][absoluteAdjacentCol] != emptyValue_unclues:
								'''print('setOfNumbers: ')
								print(setOfNumbers)
								print('unclues['+str(absoluteAdjacentRow)+']['+str(absoluteAdjacentCol)+']:')
								'''
								print(unclues[absoluteAdjacentRow][absoluteAdjacentCol])
								print(absoluteAdjacentRow, absoluteAdjacentCol)
								'''
								print('smallerThan:')
								print(smallerThan)
								print('------')'''
								#print(unclues[absoluteRow][absoluteCol])
								smallerThan.add(max((setOfNumbers-unclues[absoluteAdjacentRow][absoluteAdjacentCol])-smallerThan))
							else:
								smallerThan.add(clues[absoluteAdjacentRow][absoluteAdjacentCol])
					if greaterThan:
						for x in range(1,max(greaterThan)+1):
							if unclues[absoluteRow][absoluteCol] != emptyValue_unclues:
								addUnclue(absoluteRow, absoluteCol, x)
					if smallerThan:
						for x in range(min(smallerThan),10):
							if unclues[absoluteRow][absoluteCol] != emptyValue_unclues:
								addUnclue(absoluteRow, absoluteCol, x)
	return 0

#checks if only one possibility for number in row/col
def cluesRowCol():
	global clues
	global unclues
	found = 0
	
	for num in range(1,10):

		for row in range(9):
			listOfCols = []
			for col in range(9):
				if unclues[row][col] != emptyValue_unclues and not num in unclues[row][col]:
					listOfCols.append(col)
			if len(listOfCols) == 1:
				clues[row][listOfCols[0]] = num
				unclues[row][listOfCols[0]] = emptyValue_unclues
				fillUnclues()
				found += 1
		
		for col in range(9):
			listOfRows = []
			for row in range(9):
				if unclues[row][col] != emptyValue_unclues and not num in unclues[row][col]:
					listOfRows.append(row)
			if len(listOfRows) == 1:
				clues[listOfRows[0]][col] = num
				unclues[listOfRows[0]][col] = emptyValue_unclues
				fillUnclues()
				found += 1
	
	return found
	
#checks if only one possibility for a number in a subsquare
def cluesSquare():
	global clues
	global unclues
	
	found = 0
	
	for num in range(1,10):
		for subsquare in subsquares:
			possibilities = []
			for row in [x + subsquare[0] for x in range(3)]:
				for col in [x + subsquare[1] for x in range(3)]:
					if unclues[row][col] != emptyValue_unclues and not num in unclues[row][col]:
						possibilities.append([row,col])
			if len(possibilities) == 1:
				clues[possibilities[0]][possibilities[1]] = num
				unclues[possibilities[0]][possibilities[1]] = emptyValue_unclues
				fillUnclues()
				found += 1
	
	return found

def unclues2clues():
	
	found = 0
	
	for row in range(9):
		for col in range(9):
			length = len(unclues[row][col])
			if length == 8:
				clues[row][col] = list(setOfNumbers-unclues[row][col])[0]
				unclues[row][col] = emptyValue_unclues
				found += 1	
			elif length > 8:
				for i in range(10^3):
					print("ERROR: unclues containing all numbers in square "+str(row+1)+", "+str(col+1))
					
	return found
	
def fillUnclues():
	hasChanged = True
	initUnclues()
	uncluesFound = 0
	
	while hasChanged:	
		uncluesRowCol()
		uncluesSquare()
		uncluesIneq()
		
		cluesRowCol()
		cluesSquare()
		unclues2clues()
		
		previousUncluesFound = uncluesFound
		uncluesFound = countUnclues()
		hasChanged = uncluesFound - previousUncluesFound
	
		print('FOUND: '+str(hasChanged))
	
	return 0

def randomGrid():
	grid = [[0 for x in range(9)] for x in range(9)]
	for subsquare in subsquares:
		randomizeSquare(grid, subsquare)
	return np.array(grid)

def grid2string(grid):
	gridString = ''
	for row in range(len(grid)):
		for col in range(len(grid[row])):
			gridString += str(grid[row][col])
		gridString += '\n'
	return gridString

def checkLines(grid):
	transposed = grid.transpose()
	for line in range(9):
		if ''.join(sorted(''.join(transposed[line]))) != numbers or ''.join(sorted(''.join(grid[line]))) != numbers:
			#print('num: '+numbers)
			#print('col: '+''.join(sorted(''.join(transposed[line]))))
			#print('row: '+''.join(sorted(''.join(grid[line]))))
			return False
	return True
	
def checkSquares(grid):
	for subsquare in subsquares:
		square = grid[subsquare[0]:subsquare[0]+3, subsquare[1]:subsquare[1]+3]
		listOfNumbers = ''
		listOfNumbers = ''.join(sorted([listOfNumbers + square[x, y] for x in range(3) for y in range(3)]))
		if listOfNumbers != numbers:
			return False
	return True

def checkValid(grid):
	return checkLines(grid)
				
def solveFull():
	retries = 0

	while(True):
		swapped = 1
		iterations = 0
		totalSwaps = -1
		
		if retries%10000 == 0:
			grid = randomGrid()
			subsquaresList = set(range(9))
		
		for i in range(3):
			newPos = randint(0, 8) #risque duplicata
			subsquaresList.add(newPos) #set, pas list, donc pas de duplicata, donc sava
			subsquare = subsquares[newPos]
			grid = randomizeSquare(grid, subsquare)
		
		while(swapped > 0):
			swapped = 0
				
			for pos in subsquaresList:
				pack = solveSquare(grid, pos)
				grid = pack[0]
				swaps = pack[1]
				if not swaps:
					subsquaresList = set([p for p in subsquaresList if p != pos])
				swapped += swaps
						
			iterations += 1
			totalSwaps += swapped
			
			if iterations > 20:
				#print(visuGrid(grid))
				#sleep(50)
				break
		
		print('Retries: '+str(retries)+', Iterations: '+str(iterations)+', Total swaps: '+str(totalSwaps))
		retries += 1

		if(checkValid(grid)):
			f = open('/home/clement/SOLUTION.txt', 'w')
			f.write(visuGrid(grid))
			f.close()
			return 0
			
def randomizeSquare(grid, subsquare):
	
	isOk = False
	
	while not isOk:
		isOk = True
		
		#finding out what and where clues are
		listOfClues = ''
		for row in [x + subsquare[0] for x in range(3)]:
			for col in [x + subsquare[1] for x in range(3)]:
				if clues[row][col]:
					grid[row][col] = clues[row][col]
					listOfClues += str(clues[row][col])
		
		numbersMinusHints = [a for a in numbers if a not in listOfClues]
		
		#filling the not-already-known places with numbers
		square = ''.join(np.random.permutation(list(numbersMinusHints)))
		i = 0
		for row in [x + subsquare[0] for x in range(3)]:
			for col in [x + subsquare[1] for x in range(3)]:
				if not clues[row][col]:
					grid[row][col] = square[i]
					i += 1
					
		#checking against unclues
		for row in [x + subsquare[0] for x in range(3)]:
			if isOk:
				for col in [x + subsquare[1] for x in range(3)]:
					if unclues[row][col] != emptyValue_unclues and grid[row][col] in unclues[row][col]:
						isOk = False
						break
	return grid
	
def solveSquare(grid, pos):
	subsquare = subsquares[pos]
	swapped = 0
	
	for row in [x + subsquare[0] for x in range(3)]:
		for col in [x + subsquare[1] for x in range(2)]:
			if (grid[row][col] > grid[row][col+1]) != getIneq(row, col, row, col+1) and not clues[row][col] and not clues[row][col+1] and not grid[row][col] in unclues[row][col+1] and not grid[row][col+1] in unclues[row][col]:
				doIt = randint(0, 1)
				if doIt:
					swapped += 1
					tmp = grid[row][col]
					grid[row][col] = grid[row][col+1]
					grid[row][col+1] = tmp
				#print('Hori: '+str(grid[row][col])+(' < ', ' > ')[ineqHori[row][2*subsquare[0]/3+i]]+str(grid[row][col+1]))
	
	for col in [x + subsquare[1] for x in range(3)]:		
		for row in [x + subsquare[0] for x in range(2)]:
			if (grid[row][col] > grid[row+1][col]) != getIneq(row, col, row+1, col) and not clues[row][col] and not clues[row+1][col] and not grid[row][col] in unclues[row+1][col] and not grid[row+1][col] in unclues[row][col]:
				doIt = randint(0, 1)
				if doIt:
					swapped += 1
					tmp = grid[row][col]
					grid[row][col] = grid[row+1][col]
					grid[row+1][col] = tmp
				#print('Vert: '+str(grid[row][col])+(' < ', ' > ')[ineqVert[2*subsquare[1]/3+i][col]]+str(grid[row+1][col]))
				
	return (grid, swapped)

def visuGrid(grid):
	mystr = ''
	i = 0
	for row in range(9):
		#line of numbers and ineqHori
		mystr += str(grid[row][0])+('<', '>')[ineqHori[row][0]]+str(grid[row][1])+('<', '>')[ineqHori[row][1]]+str(grid[row][2])+'|'
		mystr += str(grid[row][3])+('<', '>')[ineqHori[row][2]]+str(grid[row][4])+('<', '>')[ineqHori[row][3]]+str(grid[row][5])+'|'
		mystr += str(grid[row][6])+('<', '>')[ineqHori[row][4]]+str(grid[row][7])+('<', '>')[ineqHori[row][5]]+str(grid[row][8])+'\n'
		if(row%3 != 2):
			#line of ineqVert
			mystr += ('^', 'v')[ineqVert[i][0]]+' '+('^', 'v')[ineqVert[i][1]]+' '+('^', 'v')[ineqVert[i][2]]+'|'
			mystr += ('^', 'v')[ineqVert[i][3]]+' '+('^', 'v')[ineqVert[i][4]]+' '+('^', 'v')[ineqVert[i][5]]+'|'
			mystr += ('^', 'v')[ineqVert[i][6]]+' '+('^', 'v')[ineqVert[i][7]]+' '+('^', 'v')[ineqVert[i][8]]+'\n'
			i += 1	
		else:
			if row != 8:
				mystr += '-----------------\n'

	return mystr
	
#checks if a 3x3 square has a unique solution by trying to solve it 1000 times, and checking each time if the solution is similar to the previous one
def checkUniqueSquare(miniIneqHori, miniIneqVert, miniClues, miniUnclues):
	
	notTheFirstTime = False
	
	for i in range(1000):
		
		#---FILLING THE MINIGRID
		isOk = False
	
		while not isOk:
			isOk = True
			
			miniGrid = [[0 for x in range(3)] for x in range(3)]
			
			#finding out what and where clues are
			listOfClues = ''
			for row in range(3):
				for col in range(3):
					if miniClues[row][col]:
						miniGrid[row][col] = miniClues[row][col]
						listOfClues += str(miniClues[row][col])
			
			numbersMinusHints = [a for a in numbers if a not in listOfClues]
			
			#filling the not-already-known places with numbers
			square = ''.join(np.random.permutation(list(numbersMinusHints)))
			i = 0
			for row in range(3):
				for col in range(3):
					if not miniClues[row][col]:
						miniGrid[row][col] = square[i]
						i += 1
						
			#checking against unclues
			for row in range(3):
				if isOk:
					for col in range(3):
						if miniUnclues[row][col] != emptyValue_unclues and miniGrid[row][col] in miniUnclues[row][col]:
							isOk = False
							break
		#---

		swapped = 1
		iterations = 0
		
		while swapped > 0 and iterations < 20:
			
			iterations += 1
			swapped = 0
			for row in range(3):
				i = 0
				for col in range(2):
					if (miniGrid[row][col] > miniGrid[row][col+1]) != miniIneqHori[row][i] and not miniClues[row][col] and not miniClues[row][col+1] and not miniGrid[row][col] in miniUnclues[row][col+1] and not miniGrid[row][col+1] in miniUnclues[row][col]:
						doIt = randint(0, 1)
						if doIt:
							swapped += 1
							tmp = miniGrid[row][col]
							miniGrid[row][col] = miniGrid[row][col+1]
							miniGrid[row][col+1] = tmp
					i += 1
			
			for col in range(3):		
				i = 0	
				for row in range(2):
					if (miniGrid[row][col] > miniGrid[row+1][col]) != ineqVert[i][col] and not miniClues[row][col] and not miniClues[row+1][col] and not miniGrid[row][col] in miniUnclues[row+1][col] and not miniGrid[row+1][col] in miniUnclues[row][col]:
						doIt = randint(0, 1)
						if doIt:
							swapped += 1
							tmp = miniGrid[row][col]
							miniGrid[row][col] = miniGrid[row+1][col]
							miniGrid[row+1][col] = tmp
					i += 1
			
		if iterations < 20 and notTheFirstTime:
			oldSol = newSol
			newSol = grid2string(miniGrid)
			
			if oldSol != newSol:
				#print(oldSol)
				#print(newSol)
				#print('-----')
				return False
		else:
			newSol = grid2string(miniGrid)
			notTheFirstTime = True
				
	return miniGrid
	
def checkUniqueGrid():
	global clues
	
	for subsquare in subsquares:
		miniIneqHori = [[ineqHori[x + subsquare[0]][y + 2*subsquare[1]/3] for y in range(2)] for x in range(3)] #a tester
		miniIneqVert = [[ineqVert[x + 2*subsquare[0]/3][y + subsquare[1]] for y in range(3)] for x in range(2)] #a tester
		miniClues = [[clues[x+subsquare[0]][y+subsquare[1]] for x in range(3)] for y in range(3)] #a tester
		miniUnclues = [[unclues[x+subsquare[0]][y+subsquare[1]] for x in range(3)] for y in range(3)] #a tester
				
		unique = checkUniqueSquare(miniIneqHori, miniIneqVert, miniClues, miniUnclues)
		if unique:
			#for i in range(10000):
				#print("YEAH!")
			for x in range(3):
				for y in range(3):
					clues[x + subsquare[0]][y + subsquare[1]] = unique[x][y]
			
	return 0

#return True if the inequality between cell1 and cell2 is respected. To gain computation time, does not throw error if cells are not adjacent.
def getIneq(row1, col1, row2, col2):
	if row1 == row2: #if different columns, use ineqHori
		#we have to turn the ineq around if col1 > col2
		minCol = min(col1, col2)
		return ineqHori[row1][2*minCol/3+minCol%3] == (col2 > col1)
		
	if col1 == col2: #if different rows, use ineqVert
		#we have to turn the ineq around if row1 > row2
		minRow = min(row1, row2)
		return ineqVert[2*minRow/3+minRow%3][col1] == (row2 > row1)
			
if __name__ == '__main__':
	fillUnclues()
	#checkUniqueGrid()
		
	#uncluesRowCol()
	solveFull()
	
	'''pool = mp.Pool(processes=32)
	result = [pool.apply(solveFull) for x in range(8)]

	q = Queue.Queue()

	for x in range(4):
		t = threading.Thread(target=solveFull)
		t.daemon = True
		t.start()

	s = q.get()
	print s'''

	
#grid = [['9', '1', '8', '3', '2', '6', '7', '5', '4'], ['3', '4', '6', '5', '1', '7', '9', '2', '8'], ['7', '2', '5', '8', '9', '4', '1', '3', '6'], ['1', '5', '3', '2', '4', '8', '6', '9', '7'], ['8', '9', '4', '6', '7', '5', '3', '1', '2'], ['2', '6', '7', '9', '3', '1', '4', '8', '5'], ['5', '3', '9', '4', '6', '2', '8', '7', '1'], ['6', '8', '1', '7', '5', '9', '2', '4', '3'], ['4', '7', '2', '1', '8', '3', '5', '6', '9']]
#print(checkValid(np.array(grid)))
