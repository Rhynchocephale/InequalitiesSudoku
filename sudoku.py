import itertools
import numpy as np

numbers = '123456789'
subsquares = [0,3,6]
#inequalities, line by line. 0 for <, 1 for >
ineq = [[[0,1,0,0,0,1],[1,0,0,1,1,1],[0,1,1,1,0,1],[1,1,1,1,0,1],[1,0,0,1,0,1],[1,1,0,0,1,0],[1,0,1,0,1,0],[1,1,0,1,1,0],[0,1,0,1,0,0]],
[[1,0,1,0,0,1],[1,0,0,1,1,0],[0,1,0,1,1,1],[1,1,0,0,1,1],[0,1,1,1,0,1],[0,0,1,1,0,1],[0,1,0,0,1,0],[1,0,1,0,1,0],[1,1,0,1,1,1]]]
#second line is column by column, grid turned CLOCKWISE

def randomGrid():
	grid = np.array([[0 for x in range(9)] for x in range(9)])
	for firstRow in subsquares:
		for firstCol in subsquares:
			square = ''.join(np.random.permutation(list(numbers)))
			i = 0
			for row in [x + firstRow for x in range(3)]:
				for col in [x + firstCol for x in range(3)]:
					grid[row][col] = square[i]
					i += 1
	return grid

def grid2string(grid):
	gridString = ''
	for row in range(9):
		for col in range(9):
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
	lines = checkLines(npgrid)
	if lines != 10:
		return False
	squares = checkSquares(npgrid)
	if squares != 10:
		return False
	return True
		
	
def swapNumbers():
		
	while(True):
		grid = randomGrid()
		swapped = 1
		iterations = 0
		totalSwaps = -1
		grid = randomGrid()
		
		while(swapped > 0):
			swapped = 0
			
			for transposed in range(2):
				for row in range(9):
					i = 0
					for col in [0,1,3,4,6,7]:
						if (grid[row][col] > grid[row][col+1]) != ineq[transposed][row][i]:
							swapped += 1
							tmp = grid[row][col]
							grid[row][col] = grid[row][col+1]
							grid[row][col+1] = tmp
						i += 1
					
				grid = grid.transpose()
						
			iterations += 1
			totalSwaps += swapped
			print('-----')
			print('Iterations: '+str(iterations))
			print('Swaps: '+str(swapped))
		
		print('-------------------')
		print('-------------------')
		print('-------------------')
		print('Total iterations: '+str(iterations))
		print('Total swaps: '+str(totalSwaps))

		if(checkValid(grid)):
			print(grid2string(grid))
			return 0
	

swapNumbers()
