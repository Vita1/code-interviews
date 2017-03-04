import sys

# Works in linear time!
# 1st Quora challenge on this page:https://www.quora.com/about/challenges (upvotes)

def _fillForwardArray(k, pos, array):
	'''
	_fillForwardArray
	Helper function for filling out the forward lists in _parseArray. Take the position of the end of a decreasing or
	increasing subrange, and backward-fill the array from there until reaches a non-None value.
	Best not to call.
	Arguments:
		k (int, k > 0): the window size
		pos (int, 0 < pos < len(array)): the position after the position to be filled from 
		array (list[int]): the list to be updated
	Return value:
		array (list[int]): the list after all the values have been filled up to pos
	'''
	array[pos - 1] = 0
	for back_pos in range(pos - 2, -1, -1):
		if not array[back_pos] == None:
			return array
		array[back_pos] = min(k - 1, array[back_pos + 1] + 1)
	return array

def _parseArray(k, numbers):
	'''
	_parseArray
	From the list(n) of numbers from input, produce 4 lists of size n.
	Each element [i] in each list is how far you can go (backward or forward, non-increasing or non-increasing) starting from there.
	Arguments:
		k (int, k > 0): the window size
		numbers (list[int]): list of numbers given by the input
	Return value:
		list(4): List of 4 list[int], where each element [i] of the list is:
			non_decreasing_forward: how far you can go non-decreasingly, forward (toward the end of the list) starting from there
			non_decreasing_backward: how far you can go non-decreasingly, backward (toward the beginning of the list) starting from there
			non_increasing_forward: how far you can go non-increasingly, forward starting from there
			non_increasing_baackward: how far you can go non-increasingly, backward starting from there
	'''
	n = len(numbers)
	non_decreasing_forward = []
	non_decreasing_backward = []
	non_increasing_forward = []
	non_increasing_backward = []

	# Initialize arrays

	for pos in range(0, n):
		non_decreasing_forward.append(None)
		non_decreasing_backward.append(None)
		non_increasing_forward.append(None)
		non_increasing_backward.append(None)

	# The backward arrays start with 0

	non_decreasing_backward[0] = 0
	non_increasing_backward[0] = 0

	for pos in range(1, n):
		# Fill the backward array by checking if an element is greater than or equal to the element before it
		if numbers[pos] >= numbers[pos - 1]:
			non_decreasing_backward[pos] = min(k - 1, non_decreasing_backward[pos - 1] + 1)
		else:
			non_decreasing_backward[pos] = 0
			# At the end of a subrange, note the position and fill the forward array up to there by moving backward
			non_decreasing_forward = _fillForwardArray(k, pos, non_decreasing_forward)			
		# Do that again for the non-increasing array
		if numbers[pos] <= numbers[pos - 1]:
			non_increasing_backward[pos] = min(k -1, non_increasing_backward[pos - 1] + 1)
		else:
			non_increasing_backward[pos] = 0
			non_increasing_forward = _fillForwardArray(k, pos, non_increasing_forward)
	non_decreasing_forward = _fillForwardArray(k, n, non_decreasing_forward)
	non_increasing_forward = _fillForwardArray(k, n, non_increasing_forward)

	# Add another element of 0 to each array to prevent index out of bound error later

	non_decreasing_forward.append(0)
	non_decreasing_backward.append(0)
	non_increasing_forward.append(0)
	non_increasing_backward.append(0)

	return [non_decreasing_forward, non_decreasing_backward, non_increasing_forward, non_increasing_backward]

def _getResult(k, non_decreasing_forward, non_decreasing_backward, non_increasing_forward, non_increasing_backward):
	'''
	_getResult
	Get the difference between # of non-decreasing subranges and # of non-increasing subranges for each window of size k.
	Arguments:
		k (int, k > 0): the window size
		non_decreasing_forward (list(n+1), list[int]): how far you can go non-decreasingly, forward (toward the end of the list) starting from there
		non_decreasing_backward (list(n+1), list[int]): how far you can go non-decreasingly, backward (toward the beginning of the list) starting from there
		non_increasing_forward (list(n+1), list[int]): how far you can go non-increasingly, forward starting from there
		non_increasing_baackward (list(n+1), list[int]): how far you can go non-increasingly, backward starting from there
	Return value:
		result (list[int], list(n - k + 1)): the result for each of the window, in order. There should be n - k + 1 windows
	'''
	result = []
	# Get result of the first window by summing the backward arrays
	result.append(sum(non_decreasing_backward[:k]) - sum(non_increasing_backward[:k]))
	for i in range(0, len(non_decreasing_backward) - k - 1):
		new_result = result[i] - non_decreasing_forward[i] + non_decreasing_backward[i + k ] - (non_increasing_forward[i] + non_increasing_backward[i + k])
		result.append(new_result)
	return result


def upvotes(k, numbers):
	'''
	upvotes
	Print the difference between # of non-decreasing subranges and # of non-increasing subranges for each window of size k in order.
	Each result is printed on its own line.
	Time complexity: O(N)
	Inputs:
		2 lines through stdin.
		First line is:
		% n k
		Where:
			n (int, n > 0) is the number of numbers in the input
			k (int, 0 < k < n) is the window size
		Second line is n numbers in order. For example for n = 5:
		% 1 2 3 1 1
	Arguments:
		k (int, k > 0): the window size
		numbers (list[int]): list of numbers given by the input through stdin
	Return values:
		None
		But it prints the result through stdout. The result for each window is printed in order on its own line.
	'''
	# Create non-decreasing and non-increasing arrays
	[non_decreasing_forward, non_decreasing_backward, non_increasing_forward, non_increasing_backward] = _parseArray(k, numbers)
	# Calculate value of each window
	result = _getResult(k, non_decreasing_forward, non_decreasing_backward, non_increasing_forward, non_increasing_backward)
	# Output result through stdout
	for i in result:
		print i
	return None


[_n, _k] = raw_input().split()
[_n, _k] = [int(_n), int(_k)]

_numbers = raw_input().split()

for i in range(0, _n):
	_numbers[i] = int(_numbers[i])

upvotes(_k, _numbers)