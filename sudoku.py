import random, time, sys
from multiprocessing import Pool

random.seed()

def colOk(sudokuGrid, candidate, refCol):
	for row in range(9):
		if sudokuGrid[row][refCol] == candidate:
			return False
	return True

def rowOk(sudokuGrid, candidate, refRow):
	for col in range(9):
		if sudokuGrid[refRow][col] == candidate:
			return False
	return True

def squareOk(sudokuGrid, candidate, refRow, refCol):
	for row in range(refRow-refRow%3, refRow-refRow%3+3):
		for col in range(refCol-refCol%3, refCol-refCol%3+3):
			if sudokuGrid[row][col] == candidate:
				return False
	return True

def printGrid(sudokuGrid):
	gridString = ''
	for row in range(len(sudokuGrid)):
		for col in range(len(sudokuGrid[row])):
			gridString += str(sudokuGrid[row][col])
		gridString += '\n'
	print(gridString)

def visuGrid(grid):
	if not grid:
		return 0
	
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
	
	print(mystr)
	return mystr

def inequalityTest(sudokuGrid, ineqHori, ineqVert, candidate, row, col):
	colMod = col%3
	if colMod == 0:
		if sudokuGrid[row][col+1]:
			if (sudokuGrid[row][col+1] > candidate) == ineqHori[row][int(2*col/3)]:
				return False
	elif colMod == 1:
		if sudokuGrid[row][col-1]:
			if (candidate > sudokuGrid[row][col-1]) == ineqHori[row][int(2*(col-1)/3)]:
				return False
		if sudokuGrid[row][col+1]:
			if (sudokuGrid[row][col+1] > candidate) == ineqHori[row][int(2*(col-1)/3)+1]:
				return False
	else:
		if sudokuGrid[row][col-1]:
			if (candidate > sudokuGrid[row][col-1]) == ineqHori[row][int(2*(col-2)/3)+1]:
				return False
	
	rowMod = row%3
	if rowMod == 0:
		if sudokuGrid[row+1][col] and (sudokuGrid[row+1][col] > candidate) == ineqVert[int(2*row/3)][col]:
			return False
	elif rowMod == 1:
		if sudokuGrid[row-1][col] and (candidate > sudokuGrid[row-1][col]) == ineqVert[int(2*(row-1)/3)][col]:
			return False
		if sudokuGrid[row+1][col] and (sudokuGrid[row+1][col] > candidate) == ineqVert[int(2*(row-1)/3)+1][col]:
			return False
	else:
		if sudokuGrid[row-1][col] and (candidate > sudokuGrid[row-1][col]) == ineqVert[int(2*(row-2)/3)+1][col]:
			return False
			
	return True
	
def possibilitiesLeft(possibleNumbers):
	total = 0
	for row in possibleNumbers:
		for cell in row:
			total += len(cell)
			
	return total
	
def checkInput(ineqHori, ineqVert):
	if len(ineqHori) != 9:
		print("Length of ineqHori: "+str(len(ineqHori)))
		return False
	if len(ineqVert) != 6:
		print("Length of ineqVert: "+str(len(ineqVert)))
		return False
	for a in ineqHori:
		if len(a) != 6:
			print("Length of ineqHori element: "+str(len(a)))
			return False
	for a in ineqVert:
		if len(a) != 9:
			print("Length of ineqVert element: "+str(len(a)))
			return False
	return True
	
def transformInput(ineq):
	c = []
	for elem in ineq:
		d = []
		for x in elem:
			d.append(int(x))
		c.append(d)
	return c

def readSource():
	f = open("source.html", "r")
	ineqHori = ""
	ineqVert = ""
	for line in f:
		if "/gt.png" in line:
			ineqHori += "1"
		elif "/lt.png" in line:
			ineqHori += "0"
		elif "/gtv.png" in line:
			ineqVert += "1"
		elif "/ltv.png" in line:
			ineqVert += "0"
	
	ineqVert = [ineqVert[i:i + 9] for i in range(0, len(ineqVert), 9)]
	ineqHori = [ineqHori[i:i + 6] for i in range(0, len(ineqHori), 6)]

	return ineqHori, ineqVert

#line by line. 0 for <, 1 for >
#ineqHori = ["011001", "011000", "110101", "000011", "100001", "100110", "101110", "101111", "010110"]
#line by line, 0 for ^, 1 for v
#ineqVert = ["110110000", "011100111", "111001100", "000101011", "001000011", "101100010"]

ineqHori, ineqVert = readSource()

if not checkInput(ineqHori, ineqVert):
	sys.exit(0)
	
ineqHori = transformInput(ineqHori)
ineqVert = transformInput(ineqVert)

def solveSudoku(firstCases=[]):
	sudokuGrid = [[0 for _ in range(9)] for _ in range(9)]
	possibleNumbers = [[list(range(1,10)) for _ in range(9)] for _ in range(9)]
	
	if firstCases:
		possibleNumbers[0][0] = [firstCases[0]]
		possibleNumbers[0][1] = [firstCases[1]]
		possibleNumbers[0][2] = [firstCases[2]]
	
	row = 0
	col = 0
	previousLen = 9
	while row < 9:
		while col < 9:
			while(possibleNumbers[row][col]):
				candidate = random.choice(possibleNumbers[row][col])
				possibleNumbers[row][col].remove(candidate)
				if colOk(sudokuGrid, candidate, col) and rowOk(sudokuGrid, candidate, row) and squareOk(sudokuGrid, candidate, row, col) and inequalityTest(sudokuGrid, ineqHori, ineqVert, candidate, row, col):
					sudokuGrid[row][col] = candidate
					col += 1
					break
			else:
				possibleNumbers[row][col] = list(range(1,10))
				if col:
					col -= 1
				else:
					col = 8
					row -= 1
					if row < 0 or (row == 0 and col < len(firstCases)-1):
						return 0
				sudokuGrid[row][col] = 0
		col = 0
		row += 1

	return sudokuGrid

if __name__ == '__main__':
	t = time.time()
	
	processOrder = []
	for x in range(1, 10):
		for y in range(1, 10):
			for z in range(1, 10):
				if len(set([x, y, z])) == len([x, y, z]):
					processOrder.append([x, y, z])
	random.shuffle(processOrder)
	pool = Pool(processes=8)
	i = len(processOrder)
	for x in pool.imap_unordered(solveSudoku, processOrder):
		print(i)
		i-=1
		if x:
			visuGrid(x)
			print("Minutes taken: "+str((time.time() - t)/60))
			sys.exit(0)
			
