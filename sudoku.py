import itertools
from time import sleep
import numpy as np
from random import randint
from copy import deepcopy

numbers = '123456789'
subsquares = [[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]
#inequalities, line by line. 0 for <, 1 for >
ineqHori = [[0,1,0,0,0,1],[1,0,0,1,1,1],[0,1,1,1,0,1],[1,1,1,1,0,1],[1,0,0,1,0,1],[1,1,0,0,1,0],[1,0,1,0,1,0],[1,1,0,1,1,0],[0,1,0,1,0,0]]
#line by line, 0 for ^, 1 for v
ineqVert = [[1,1,0,0,0,1,0,1,1],[1,0,1,0,1,1,1,0,1],[0,1,0,1,1,0,0,0,1],[1,0,0,1,1,0,1,1,0],[1,1,1,0,0,1,1,1,0],[1,0,0,1,1,1,1,0,1]]

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
	for line in range(9):
		if ''.join(sorted(''.join(grid.transpose()[line]))) != numbers or ''.join(sorted(''.join(grid[line]))) != numbers:
			return False
	return True
	
def checkSquares(grid):
	for subsquare in subsquares:
		square = grid[subsquare[0]:subsquare[0]+3,subsquare[1]:subsquare[1]+3]
		listOfNumbers = ''
		listOfNumbers = ''.join(sorted([listOfNumbers + square[x, y] for x in range(3) for y in range(3)]))
		if listOfNumbers != numbers:
			return False
	return True

def checkValid(grid):
	lines = checkLines(grid)
	if lines != 10:
		return False
	squares = checkSquares(grid)
	if squares != 10:
		return False
	return True
		
	
def swapNumbers():
	grid = randomGrid()
	subsquaresList = set(range(9))

	retries = 0

	while(True):
		swapped = 1
		iterations = 0
		totalSwaps = -1
		
		for i in range(2):
			newPos = randint(0,8) #risque duplicata
			subsquaresList.add(newPos) #set, pas list, donc pas de duplicata, donc sava
			subsquare = subsquares[newPos]
			grid = randomizeSquare(grid, subsquare)
		
		while(swapped > 0):
			swapped = 0
				
			for pos in subsquaresList:
				pack = solveSquare(grid, pos)
				grid = pack[0]
				swaps = pack[1]
				if(swaps == 0):
					subsquaresList = set([p for p in subsquaresList if p != pos])
				swapped += swaps
						
			iterations += 1
			totalSwaps += swapped
			if iterations > 10:
				print(visuGrid(grid))
				sleep(50)
				break
		
		print('Retries: '+str(retries)+', Iterations: '+str(iterations)+', Total swaps: '+str(totalSwaps))
		retries += 1

		if(checkValid(grid)):
			print(grid2string(grid))
			return 0
			
def randomizeSquare(grid,subsquare):
	square = ''.join(np.random.permutation(list(numbers)))
	i = 0
	for row in [x + subsquare[0] for x in range(3)]:
		for col in [x + subsquare[1] for x in range(3)]:
			grid[row][col] = square[i]
			i += 1
	return grid
	
def solveSquare(grid, pos):
	subsquare = subsquares[pos]
	swapped = 0
	
	for row in [x + subsquare[0] for x in range(3)]:
		i = 0
		for col in [x + subsquare[1] for x in range(2)]:
			if (grid[row][col] > grid[row][col+1]) != ineqHori[row][2*subsquare[0]/3+i]:
				swapped += 1
				tmp = grid[row][col]
				grid[row][col] = grid[row][col+1]
				grid[row][col+1] = tmp
				#print('Hori: '+str(grid[row][col])+(' < ',' > ')[ineqHori[row][2*subsquare[0]/3+i]]+str(grid[row][col+1]))
			i += 1
	
	for col in [x + subsquare[1] for x in range(3)]:		
		i = 0	
		for row in [x + subsquare[0] for x in range(2)]:
			if (grid[row][col] > grid[row+1][col]) != ineqVert[2*subsquare[1]/3+i][col]:
				swapped += 1
				tmp = grid[row][col]
				grid[row][col] = grid[row+1][col]
				grid[row+1][col] = tmp
				#print('Vert: '+str(grid[row][col])+(' < ',' > ')[ineqVert[2*subsquare[1]/3+i][col]]+str(grid[row+1][col]))
			i += 1

	return (grid, swapped)

def visuGrid(grid):
	mystr = ''
	i = 0
	for row in range(9):
		#line of numbers and ineqHori
		mystr += str(grid[row][0])+('<','>')[ineqHori[row][0]]+str(grid[row][1])+('<','>')[ineqHori[row][1]]+str(grid[row][2])+'|'
		mystr += str(grid[row][3])+('<','>')[ineqHori[row][2]]+str(grid[row][4])+('<','>')[ineqHori[row][3]]+str(grid[row][5])+'|'
		mystr += str(grid[row][6])+('<','>')[ineqHori[row][4]]+str(grid[row][7])+('<','>')[ineqHori[row][5]]+str(grid[row][8])+'\n'
		if(row%3 != 2):
			print('i: '+str(i))
			#line of ineqVert
			mystr += ('^','v')[ineqVert[i][0]]+' '+('^','v')[ineqVert[i][1]]+' '+('^','v')[ineqVert[i][2]]+'|'
			mystr += ('^','v')[ineqVert[i][3]]+' '+('^','v')[ineqVert[i][4]]+' '+('^','v')[ineqVert[i][5]]+'|'
			mystr += ('^','v')[ineqVert[i][6]]+' '+('^','v')[ineqVert[i][7]]+' '+('^','v')[ineqVert[i][8]]+'\n'
			i += 1	
		else:
			if row != 8:
				mystr += '-----------------\n'

	return mystr

#print(grid2string(randomGrid()))
swapNumbers()
#print(checkLines(randomGrid()))
