import sys
from collections import deque

class Node:
	'''
	Node
	Object to contain information about each article. Each node is an article.
	Properties when created:
		node.index (int, < 10^5) the index of an article (the position in the article reading time array that it appeared)
		node.time (int, < 10^6) the reading time of the article
	Properties after a leaf has been chosen as root:
		node.children (dict) a hashtable of all the children of this article (dict for constant time lookup mutable items)
			dictionary key: int, index of the child article
			dictionary value: reference to the Node object corresponding to this child article
		node.parent (Node) the parent article of this article
		node.remaining_time (float) the time a reader is expected to take to read the rest of the tree when he has reached
			this node, after starting from the root. This time includes the time it takes to read this article (node.time)
		node.expected_time (float) the time a reader is expected to take if he starts reading at this node

	'''
	def __init__(self, index, time):
		self.index = index
		self.time = time
		self.children = {}
		self.parent = None
		self.remaining_time = None
		self.expected_time = None

	def countChildren(self):
		'''
		Node.countChildren
		Gets the number of children of this article.
		Return value:
			int: number of children
		'''
		return len(self.children)

	def countDegrees(self):
		'''
		Node.countDegrees
		Gets the number of degrees of this article (the number of articles it's connected to).
		Return value:
			int: number of degrees
		'''
		if self.parent == None:
			return len(self.children)
		return len(self.children) + 1

	def makeParent(self, node):
		'''
		Make one of articles this article is connected to its parent.
		Argument:
			node (Node): the article to be made parent
		Return value:
			None, but node is assigned as parent of this article
		'''
		#if (not (node in self.children.values())):
		#	raise Exception('Node not connected to the current node')
		self.parent = node



def makeTree(timebyquestion, edges):
	'''
	makeTree
	Makes a tree to represent articles and their relatendness.
	Each node of the tree is an article. Each edge denotes that two articles are related.
	One leaf (node with only one degree) is chosen as root, after which each node is assigned an
	appropriate parent.
	Arguments:
		timebyquestion: list(int) of length n, n < 10^5. Element n is the reading time for article n + 1
		edges:list(tuple) of length n -1. Each element is a tuple with two integers a and b, denoting that 
		a and b are related articles
	Return values:
		root (Node) reference to the Node object that is the root of the tree
	'''
	# Create tree nodes
	nodes = [None]
	for i in range(1, len(timebyquestion) + 1):
		new_node = Node(i, timebyquestion[i - 1])
		nodes.append(new_node)
	# Connect related articles
	for pair in edges:
		nodes[pair[0]].children[pair[1]] = nodes[pair[1]]
		nodes[pair[1]].children[pair[0]] = nodes[pair[0]]
	# Get node
	for node in nodes:
		if node == None:
			continue
		if node.countChildren() == 1:
			root = node
			break

	# Orient the tree by asigning parents

	stack = deque()
	for child in root.children.values():
		stack.append(tuple([child, root]))
	while stack:
		node_parent_pair = stack.popleft()
		node_parent_pair[0].makeParent(node_parent_pair[1])
		del node_parent_pair[0].children[node_parent_pair[1].index]
		for child in node_parent_pair[0].children.values():
			stack.append(tuple([child, node_parent_pair[0]]))

	return root

def calculateRemainingTimes(root):
	'''
	calculateRemainingTimes
	For each node in the tree,calculate the time a reader is expected to take to read the rest of the tree when he has reached
	this node, after starting from the root. This time includes the time it takes to read the node's article.
	The remaining times are calculated by starting at the leaves and working up to the root.
	Argument:
		root (Node) reference to the Node object that is the root of the tree
	Return value:
		None 
	'''
	stack = [root]

	while stack:
		# Look at the last article in the stack
		peek = stack[-1]
		level_completion = True
		# If it is a leaf, then its remaining time is equal to its reading time. Remove it from the stack
		if peek.countChildren() == 0:
			peek.remaining_time = peek.time
			stack.pop()
			continue
		# If it's not a leaf, then look at its children. Push children whose remaining time time hasn't been calculated
		# yet onto the stack and flag the article to be evaluated later
		for child in peek.children.values():
			if child.countChildren() == 0:
				child.remaining_time = child.time
				continue
			if child.remaining_time == None:
				level_completion = False
				stack.append(child)
		# If all children have their reamaining time calculated, then calculatedthe remaining time for this node
		# and remove it from the stack
		if level_completion:
			node = stack.pop()
			node.remaining_time = 0
			for child in node.children.values():
				node.remaining_time += child.remaining_time 
			node.remaining_time = float(node.remaining_time) / node.countChildren() 
			node.remaining_time += node.time

def getMinReadingTimeArticle(root):
	'''
	getMinReadingTimeArticle
	Gets the index of the article with the shortest expected reading time.
	Does this by traversing the tree, starting at the root, and calculating the expected time for each article
	from the reading time and remaining time of the articles it's connected to.
	Argument:
		root (Node) reference to the Node object that is the root of the tree
	Return value:
		min_article (int < 10^5) the index of the article with the shortest expected reading time
	'''
	# The expected reading time of the root is its remaining time
	root.expected_time = root.remaining_time
	min_article = root
	# Each itme on the stack is a tuple with two values: stackitem[0] is a Node, and stackitem[2] is an accumulative
	# number needed to calculate the parent node's contribution to the expected reading time
	# Initialize it with the root and 0 (since the root has no parent)
	stack = [(root, 0.0)]

	while stack:

		next_node = stack.pop()
		node = next_node[0]
		accumulated = next_node[1]
		
		degree = node.countDegrees()

		# Calculate the contribution of an article's parent node to its reading time
		# This contribution is equal to the accumulative number / # of node degrees
		# (The division is done later in the function)
		time_from_parent = 0
		if not (node.parent == None):
			time_from_parent = accumulated


		# Calculate the contribution of an article's children node to its reading time
		# This contribution is equal to the sum of all of their remaining times / # of node degrees
		# (The division is done later in the function)
		time_from_children = 0
		for child in node.children.values():
			time_from_children += child.remaining_time

		# Summing the two numbers above 
		time_without_this_node = time_from_children + time_from_parent

		# Pushing the children nodes onto the stack
		for child in node.children.values():
			# The accumulative number is the contribution of this node to its children's expected reading time
			child_accumulated = node.time + (time_without_this_node - child.remaining_time) / max(1, degree -1)
			stack.append((child, child_accumulated))

		# The node's expected reading time is the sum of its reading time plus the contribution from its parent and children
		node.expected_time = node.time + time_without_this_node / degree
		if node.expected_time < min_article.expected_time:
			min_article = node

	return min_article


def findMinStartingPoint(timebyquestion, edges):
	'''
	findMinStartingPoint

	Gets inputs from stdin and gives the index of the article with shortest expected reading time.
	Step 1: Makes a tree with articles as nodes and edges connecting related articles.
	Step 2: Makes one leaf the root. For all nodes, calculates the expected remaining reading time as if the reader
	has just reached that node after starting at the root.
	Step 3: Calculates the expected reading time for each article by arithmetic on the remaining times.
	Time complexity: O(N)

	Arguments:
		timebyquestion: list(int) of length n, n < 10^5. Element n is the reading time for article n + 1
		edges:list(tuple) of length n -1. Each element is a tuple with two integers a and b, denoting that 
		a and b are related articles
	Return value:
		None, but outputs to stdout an integer that is the article with the shortest expected reading time
	'''
	# Make a tree with articles as nodes and edges as relatedness
	root = makeTree(timebyquestion, edges)
	# Calculate remaining time (see docstring for getAllRemainingTimes)
	calculateRemainingTimes(root)
	# Find the article with the shortest expected reading time
	min_article = getMinReadingTimeArticle(root)
	# Print it to stdout
	print min_article.index
	return None

# Get stdin input
# First line has 1 integers n: the number of articles
# Next line has n integers, each corresponding to the reading times of article 1 to n
# Next n-1 lines has two integers a b, to denote that a and b are related articles

_n = int(raw_input())

_timebyquestion = raw_input().split()

for i in range(0, len(_timebyquestion)):
	_timebyquestion[i] = int(_timebyquestion[i])

# Tree building

_edges = []

for i in range(0, _n - 1):
	_pair = raw_input().split()
	for j in [0, 1]:
		_pair[j] = int(_pair[j])
	_edges.append(tuple(_pair))

findMinStartingPoint(_timebyquestion, _edges)