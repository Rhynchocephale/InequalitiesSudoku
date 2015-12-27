import itertools
from time import sleep
import numpy as np

numbers = '123456789'
subsquares = [0,3,6]
#inequalities, line by line. 0 for <, 1 for >
ineqHori = [[0,1,0,0,0,1],[1,0,0,1,1,1],[0,1,1,1,0,1],[1,1,1,1,0,1],[1,0,0,1,0,1],[1,1,0,0,1,0],[1,0,1,0,1,0],[1,1,0,1,1,0],[0,1,0,1,0,0]]
#line by line, 0 for ^, 1 for v
ineqVert = [[1,1,0,0,0,1,0,1,1],[1,0,1,0,1,1,1,0,1],[0,1,0,1,1,0,0,0,1],[1,0,0,1,1,0,1,1,0],[1,1,1,0,0,1,1,1,0],[1,0,0,1,1,1,1,0,1]]

def randomGrid():
	grid = [[0 for x in range(9)] for x in range(9)]
	for firstRow in subsquares:
		for firstCol in subsquares:
			square = ''.join(np.random.permutation(list(numbers)))
			i = 0
			for row in [x + firstRow for x in range(3)]:
				for col in [x + firstCol for x in range(3)]:
					grid[row][col] = square[i]
					i += 1
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
	for row in subsquares:
		for col in subsquares:
			square = grid[row:row+3,col:col+3]
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
		
	retries = 0
	while(True):
		grid = randomGrid()
		swapped = 1
		iterations = 0
		totalSwaps = -1
		grid = randomGrid()
		
		while(swapped > 0):
			swapped = 0

			for row in range(9):
				i = 0
				for col in [0,1,3,4,6,7]:
					if (grid[row][col] > grid[row][col+1]) != ineqHori[row][i]:
						swapped += 1
						tmp = grid[row][col]
						grid[row][col] = grid[row][col+1]
						grid[row][col+1] = tmp
					i += 1
			
			i = 0
			for row in [0,1,3,4,6,7]:
				for col in range(9):
					if (grid[row][col] > grid[row+1][col]) != ineqVert[i][col]:
						swapped += 1
						tmp = grid[row][col]
						grid[row][col] = grid[row+1][col]
						grid[row+1][col] = tmp		
				i += 1			
						
			iterations += 1
			totalSwaps += swapped
			#print('-----')
			#print('Iterations: '+str(iterations))
			#print('Swaps: '+str(swapped))
		
		print('Retries: '+str(retries)+', Iterations: '+str(iterations)+', Total swaps: '+str(totalSwaps))
		retries += 1

		if(checkValid(grid)):
			print(grid2string(grid))
			return 0

#print(grid2string(randomGrid()))
swapNumbers()
#print(checkLines(randomGrid()))
