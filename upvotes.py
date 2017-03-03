import sys

# Works in linear time!
# 1st Quora challenge on this page:https://www.quora.com/about/challenges (upvotes)

def _increaseUntilMax(k, num):
	if (num + 1) >= k:
		return k - 1
	return num + 1

def _fillForwardArray(k, pos, array):
	array[pos - 1] = 0
	for back_pos in range(pos - 2, -1, -1):
		if not array[back_pos] == None:
			return array
		array[back_pos] = _increaseUntilMax(k, array[back_pos + 1])
	return array

def _parseArray(k, numbers):
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

	# Populate arrays with the right values
	non_decreasing_backward[0] = 0
	non_increasing_backward[0] = 0
	for pos in range(1, n):
		# Fill the non_decreasing arrays
		if numbers[pos] >= numbers[pos - 1]:
			non_decreasing_backward[pos] = _increaseUntilMax(k, non_decreasing_backward[pos - 1])
		else:
			non_decreasing_backward[pos] = 0
			non_decreasing_forward = _fillForwardArray(k, pos, non_decreasing_forward)			
		# Fill the non_increasing arrays
		if numbers[pos] <= numbers[pos - 1]:
			non_increasing_backward[pos] = _increaseUntilMax(k, non_increasing_backward[pos - 1])
		else:
			non_increasing_backward[pos] = 0
			non_increasing_forward = _fillForwardArray(k, pos, non_increasing_forward)
	non_decreasing_forward = _fillForwardArray(k, n, non_decreasing_forward)
	non_increasing_forward = _fillForwardArray(k, n, non_increasing_forward)

	non_decreasing_forward.append(0)
	non_decreasing_backward.append(0)
	non_increasing_forward.append(0)
	non_increasing_backward.append(0)

	return [non_decreasing_forward, non_decreasing_backward, non_increasing_forward, non_increasing_backward]

def _getResult(k, non_decreasing_forward, non_decreasing_backward, non_increasing_forward, non_increasing_backward):
	result = []
	# Get result of the first window by summing the backward arrays
	result.append(sum(non_decreasing_backward[:k]) - sum(non_increasing_backward[:k]))
	for i in range(0, len(non_decreasing_backward) - k - 1):
		print result
		print non_decreasing_forward[i]
		print non_decreasing_backward[i + k - 1] 
		print non_increasing_forward[i]
		print non_increasing_backward[i + k - 1]
		new_result = result[i] - non_decreasing_forward[i] + non_decreasing_backward[i + k ] - (non_increasing_forward[i] + non_increasing_backward[i + k])
		result.append(new_result)
	return result


def upvotes(k, numbers):
	# Create non-decreasing and non-increasing array
	[non_decreasing_forward, non_decreasing_backward, non_increasing_forward, non_increasing_backward] = _parseArray(k, numbers)
	# Calculate value of each window
	result = _getResult(k, non_decreasing_forward, non_decreasing_backward, non_increasing_forward, non_increasing_backward)
	print result
	#for i in result:
	#	print i
	return None


[_n, _k] = raw_input().split()
[_n, _k] = [int(_n), int(_k)]

_numbers = raw_input().split()

for i in range(0, _n):
	_numbers[i] = int(_numbers[i])

upvotes(_k, _numbers)