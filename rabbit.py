'''
There is a rabbit that starts in the middle of an n x m matrix, n > 0, m > 0.
Each element of a matrix is an integer representing points gained for being on the spot. 
If there are multiple possible "middles" then choose the one which has the highest point value to start on. 
On each iteration, the rabbit can move up, left, right, or down. 
The rabbit will always move to the next spot with the highest point value 
and will "consume" those points (set the point value in that position to 0). 
The rabbit spots when all positions around it are 0s. Calculate how many points the rabbit will score for a given m x n matrix.
'''

import operator

def _getStartingProperties(matrix):
	'''
	Get starting position of the rabbit.
	Argument:
		matrix: list[m][n] input matrix of at least 1 element each dimension
	Return value:
		center: list of array index in the form of [row, column]
	'''
	row = len(matrix)
	column = len(matrix[0])
	potential_center = {}
	if row % 2 and column % 2:
		center = [row / 2, column / 2]
	if (not (row % 2)) and (not (column % 2)):
		potential_center = {
			0: [row /2, column / 2],
			1: [row / 2 - 1, column / 2],
			2: [row / 2, column / 2 - 1],
			3: [row / 2 - 1, column / 2 - 1],
		}
	if (not (row % 2)) and column % 2:
		potential_center = {
			0: [row /2, column / 2],
			1: [row / 2 - 1, column / 2],
		}
	if row % 2 and (not (column % 2)):
		potential_center = {
			0: [row /2, column / 2],
			1: [row / 2, column / 2 - 1],
		}
	center = potential_center[max(potential_center, key = potential_center.get)]
	eaten = matrix[center[0]][center[1]]
	matrix[center[0]][center[1]] = 0
	return [matrix, center, eaten]

def _getAdjacentSquares(matrix, position):
	'''
	Get the value of the squares adjacent to current position.
	Arguments:
		matrix: list[m][n] input matrix of at least 1 element each dimension
		position: list of array index in the form of [row, column]
	Return value:
		adjacent_squares: dict with four keys: 'left', 'right', 'up', 'down'
			each value is the value of the square in that direction relative to current position
			value is None if there's no adjacent square in that direction
	'''

	if position[0] == len(matrix) - 1:
		down = None
	else:
		down = matrix[position[0] + 1][position[1]]

	if position[0] == 0:
		up = None
	else: 
		up = matrix[position[0] - 1][position[1]]

	if position[1] == len(matrix[0]) - 1:
		right = None
	else:
		right = matrix[position[0]][position[1] + 1]

	if position[1] == 0:
		left = None
	else:
		left = matrix[position[0]][position[1] - 1]

	adjacent_squares = {
		'left': left,
		'right': right,
		'up': up,
		'down': down,
	}
	return adjacent_squares

def _validAdjacent(matrix, position):
	'''
	Check to see if there's any non-None or non-zero square adjacent to the current position.
	Arguments:
		matrix: list[m][n] input matrix of at least 1 element each dimension
		position: list of array index in the form of [row, column]
	Return value:
		valid_square: true if there's still a non-zero, non-None square adjacent to the current position
						false otherwise
	'''
	adjacent = _getAdjacentSquares(matrix, position)
	valid_square = False
	for i in adjacent.values():
		if (not (i == None)) and (not (i == 0)):
			valid_square = True
			break
	return valid_square

def _updatePosition(position, direction):
	'''
	Give the new position of the rabbit after moving and eating.
	Do not call without checking that direction is valid first.
	Arguments:
		position: list of array index in the form of [row, column]
		direction: 'left', 'right', 'up' or 'down'. 
	Return value:
		new position as list of array index in the form of [row, column]
		[-1, -1] if direction input is invalid
	'''
	if direction == 'left':
		return [position[0], position[1] - 1]
	if direction == 'right':
		return [position[0], position[1] + 1]
	if direction == 'down':
		return [position[0] + 1, position[1]]
	if direction == 'up':
		return [position[0] - 1, position[1]]
	return [-1, -1]


def _moveAndEat(matrix, position):
	'''
	Move the rabbit, update eating count and get updated garden matrix.
	Arguments:
		matrix: list[m][n] input matrix of at least 1 element each dimension
		position: list of array index in the form of [row, column]
	Return values:
		eaten_matrix: [m][n] matrix after the rabbit has eaten the adjacent square with the most carrots
		new_position: the new position of the rabbit after having eaten, list of array index in the form of [row, column]
		amount_eaten: the amount of carrots the rabbit just ate
	'''

	# Get values of adjacent squares
	adjacent = _getAdjacentSquares(matrix, position)
	# Get the direction of value of adjacent square with max carrots
	direction = max(adjacent, key = adjacent.get)
	amount_eaten = adjacent[direction]
	# Update rabbit position
	new_position = _updatePosition(position, direction)
	# Update the matrix after eaten 
	matrix[new_position[0]][new_position[1]] = 0
	return [matrix, new_position, amount_eaten]

def amountEaten(matrix):
	'''
	Main function.
	Arguments:
		matrix: list[m][n] input matrix of at least 1 element each dimension
	Return value:
		eaten: int, amount of rabbits eaten by the rabbit
	'''
	# Determine matrix size and starting position
	matrix, position, eaten = _getStartingProperties(matrix)
	while _validAdjacent(matrix, position):
		[matrix, position, new_carrots] = _moveAndEat(matrix, position)
		eaten += new_carrots
	return eaten
