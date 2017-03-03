'''
Print a square (NxN) matrix following a spiral path, starting at the top left position.

Example input:

input = [[1,2,3], [4,5,6], [7,8,9]]

Example output:

[1,2,3,6,9,8,7,4,5]
'''

def _getTraversedItem(matrix, side, first, n, i):
	'''
	Get the specified item.
	Arguments:
		matrix: list[n][n] of int, n > 1
		side: int in [0, 1, 2, 3]
			 0: "top", elements to be printed left to right
			 1: "right", elements to be printed up to down
			 2: "bottom", elements to be printed right to left
			 3; "left", elements to be printed down to up
		first: the top-most / left-most element of the side currently printed
		n: the right-most / bottom-most elemented to the side currently printed
		i: the position of the element to be printed in specified row or column
	Return value:
		int: the element to be printed
	'''
	if side == 0:
		return matrix[first][i]
	if side == 1:
		return matrix[i][n-1]
	if side == 2:
		return matrix[n-1][i]
	if side == 3:
		return matrix[i][first]

def _traverseSide(matrix, side, first, n):
	'''
	Get all the elements from one side of the matrix in the order they should be printed.
	Arguments:
		matrix: list[n][n] of int, n > 1
		side: int in [0, 1, 2, 3]
			 0: "top", elements to be printed left to right
			 1: "right", elements to be printed up to down
			 2: "bottom", elements to be printed right to left
			 3; "left", elements to be printed down to up
		first: the top-most / left-most element to be printed
		n: the right-most / bottom-most elemented to be printed
	Return value:
		numlist: list[int] of all elements along that side, printed in order
	'''
	sideMap = {
		0: range(first, n),
		1: range(first + 1, n),
		2: range(n - 2, first - 1, -1),
		3: range(n -2, first, -1),
	}
	numlist = []
	for i in sideMap[side]:
		numlist += [_getTraversedItem(matrix, side, first, n, i)]
	return numlist


def printSpiralMatrix(matrix):
	'''
	Print the elements of the given NxN matrix following a spiral path.
	Argument:
		matrix: list[n][n] of int, n > 1
	Return value:
		spiral: list[n * n] of integers from matrix, following a spiral pattern from the top left corner
	'''
	n = len(matrix)
	first = 0
	spiral = []
	while first < n:
		for i in range(0,4):
			spiral += _traverseSide(matrix, i, first, n - first)
		first += 1
	return spiral
