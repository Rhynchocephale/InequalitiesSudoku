import itertools
from time import sleep
import numpy as np
from random import randint

numbers = '123456789'
subsquares = [[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]


#Olivia
ineqHori = [[1,0,1,0,0,0],[1,0,0,1,0,0],[1,1,1,0,0,1],[0,1,0,1,0,1],[0,0,1,1,0,1],[1,1,0,1,1,0],[0,1,0,0,0,0],[1,1,1,1,1,0],[0,1,0,0,1,1]]
ineqVert = [[1,1,0,0,0,1,1,1,1],[0,0,1,0,1,1,1,0,1],[1,1,0,0,1,0,0,0,1],[0,0,1,1,0,1,0,1,0],[1,1,1,0,0,1,0,1,0],[0,0,0,1,1,0,1,1,1]]

#Clement
'''
#inequalities, line by line. 0 for <, 1 for >
ineqHori = [[0,1,0,0,0,1],[1,0,0,1,1,1],[0,1,1,1,0,1],[1,1,1,1,0,1],[1,0,0,1,0,1],[1,1,0,0,1,0],[1,0,1,0,1,0],[1,1,0,1,1,0],[0,1,0,1,0,0]]
#line by line, 0 for ^, 1 for v
ineqVert = [[1,1,0,0,0,1,0,1,1],[1,0,1,0,1,1,1,0,0],[0,1,0,1,1,0,0,0,1],[1,0,0,1,1,0,1,1,0],[1,1,1,0,0,1,1,1,0],[1,0,0,1,1,1,1,0,1]]
'''

clues = [[0,0,0,0,1,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0,0],[0,0,0,0,0,1,0,0,0],[1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1,0],[0,0,0,1,0,0,0,0,0],[0,0,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,2,1]]
unclues = [[set() for x in range(9)] for x in range(9)]
emptyValue_unclues = set([0])

def fillUnclues():
	global unclues
	
	for xClues in range(9):
		for yClues in range(9):
			if clues[xClues][yClues]:
				for rowCol in range(9):
					if unclues[xClues][rowCol] != emptyValue_unclues:
						unclues[xClues][rowCol].add(clues[xClues][yClues])
					if unclues[rowCol][yClues] != emptyValue_unclues:
						unclues[rowCol][yClues].add(clues[xClues][yClues])
				unclues[xClues][yClues] = emptyValue_unclues
	
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
	return checkLines(grid)
				
def swapNumbers():
	retries = 0

	while(True):
		swapped = 1
		iterations = 0
		totalSwaps = -1
		
		if retries%10000 == 0:
			grid = randomGrid()
			subsquaresList = set(range(9))
		
		for i in range(3):
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
			f = open('/home/clement/SOLUTION.txt','w')
			f.write(visuGrid(grid))
			f.close()
			return 0
			
def randomizeSquare(grid,subsquare):
	
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
		i = 0
		for col in [x + subsquare[1] for x in range(2)]:
			if (grid[row][col] > grid[row][col+1]) != ineqHori[row][2*subsquare[0]/3+i] and not clues[row][col] and not clues[row][col+1] and not grid[row][col] in unclues[row][col+1] and not grid[row][col+1] in unclues[row][col]:
				doIt = randint(0,1)
				if doIt:
					swapped += 1
					tmp = grid[row][col]
					grid[row][col] = grid[row][col+1]
					grid[row][col+1] = tmp
				#print('Hori: '+str(grid[row][col])+(' < ',' > ')[ineqHori[row][2*subsquare[0]/3+i]]+str(grid[row][col+1]))
			i += 1
	
	for col in [x + subsquare[1] for x in range(3)]:		
		i = 0	
		for row in [x + subsquare[0] for x in range(2)]:
			if (grid[row][col] > grid[row+1][col]) != ineqVert[2*subsquare[1]/3+i][col] and not clues[row][col] and not clues[row+1][col] and not grid[row][col] in unclues[row+1][col] and not grid[row+1][col] in unclues[row][col]:
				doIt = randint(0,1)
				if doIt:
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
			#line of ineqVert
			mystr += ('^','v')[ineqVert[i][0]]+' '+('^','v')[ineqVert[i][1]]+' '+('^','v')[ineqVert[i][2]]+'|'
			mystr += ('^','v')[ineqVert[i][3]]+' '+('^','v')[ineqVert[i][4]]+' '+('^','v')[ineqVert[i][5]]+'|'
			mystr += ('^','v')[ineqVert[i][6]]+' '+('^','v')[ineqVert[i][7]]+' '+('^','v')[ineqVert[i][8]]+'\n'
			i += 1	
		else:
			if row != 8:
				mystr += '-----------------\n'

	return mystr
	
#checks if a 3x3 square has a unique solution by trying to solve it 1000 times, and checking each time if the solution is similar to the previous one
def checkUniqueSquare(miniGrid, miniIneqHori, miniIneqVert, miniClues, miniUnclues):
	
	for i in range(1000):
		swapped = 1
		
		while swapped > 0:
			
			swapped = 0
			for row in range(3):
				i = 0
				for col in range(2):
					if (miniGrid[row][col] > miniGrid[row][col+1]) != miniIneqHori[row][i] and not miniClues[row][col] and not miniClues[row][col+1] and not miniGrid[row][col] in miniUnclues[row][col+1] and not miniGrid[row][col+1] in miniUnclues[row][col]:
						doIt = randint(0,1)
						if doIt:
							swapped += 1
							tmp = miniGrid[row][col]
							miniGrid[row][col] = miniGrid[row][col+1]
							miniGrid[row][col+1] = tmp
					i += 1
			
			for col in range(3):		
				i = 0	
				for row in range(2)]:
					if (miniGrid[row][col] > miniGrid[row+1][col]) != ineqVert[i][col] and not miniClues[row][col] and not miniClues[row+1][col] and not miniGrid[row][col] in miniUnclues[row+1][col] and not miniGrid[row+1][col] in miniUnclues[row][col]:
						doIt = randint(0,1)
						if doIt:
							swapped += 1
							tmp = miniGrid[row][col]
							miniGrid[row][col] = miniGrid[row+1][col]
							miniGrid[row+1][col] = tmp
					i += 1
			
			if i != 0:
				oldSol = newSol
				newSol = grid2string(miniGrid)
			
				if oldSol != newSol:
					return false
			else:
				newSol = grid2string(miniGrid)
				
	return newSol

fillUnclues()
swapNumbers()
#grid = [['9','1','8','3','2','6','7','5','4'],['3','4','6','5','1','7','9','2','8'],['7','2','5','8','9','4','1','3','6'],['1','5','3','2','4','8','6','9','7'],['8','9','4','6','7','5','3','1','2'],['2','6','7','9','3','1','4','8','5'],['5','3','9','4','6','2','8','7','1'],['6','8','1','7','5','9','2','4','3'],['4','7','2','1','8','3','5','6','9']]
#print(checkValid(np.array(grid)))
