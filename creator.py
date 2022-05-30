# Sudoku: Creator

from random import randint

# ==================================================================================================== #

def generate_puzzle():
	# Based on the Wave Function Collapse algorithm idea
	success = False
	while not success:
		# New puzzle array: puzzle_array[x][y][option]
		puzzle_array = [[[i for i in range(1, 10)] for _ in range(9)] for _ in range(9)]
	
		for _ in range(81):
			# Select most stable cell to fill in
			stable_cell_list = []
			i = 1
			while len(stable_cell_list) == 0:
				for x in range(9):
					for y in range(9):
						if isinstance(puzzle_array[x][y], list):
							if len(puzzle_array[x][y]) == i:
								stable_cell_list.append([x, y])
				i += 1
			x, y = stable_cell_list[randint(0, len(stable_cell_list) -1)]

			# Select value for cell
			selection = puzzle_array[x][y][randint(0, len(puzzle_array[x][y]) - 1)]
			puzzle_array[x][y] = selection

			# Remove selection from row
			for other_x in range(9):
				if other_x != x:
					if isinstance(puzzle_array[other_x][y], list):
						if selection in puzzle_array[other_x][y]:
							del puzzle_array[other_x][y][puzzle_array[other_x][y].index(selection)]

			# Remove selection from column
			for other_y in range(9):
				if other_y != y:
					if isinstance(puzzle_array[x][other_y], list):
						if selection in puzzle_array[x][other_y]:
							del puzzle_array[x][other_y][puzzle_array[x][other_y].index(selection)]

			# Remove selection from box
			if x in [0, 1, 2]:
				box_x = [0, 1, 2]
			elif x in [3, 4, 5]:
				box_x = [3, 4, 5]
			elif x in [6, 7, 8]:
				box_x = [6, 7, 8]
			if y in [0, 1, 2]:
				box_y = [0, 1, 2]
			elif y in [3, 4, 5]:
				box_y = [3, 4, 5]
			elif y in [6, 7, 8]:
				box_y = [6, 7, 8]

			for other_x in box_x:
				for other_y in box_y:
					if other_x != x or other_y != y:
						if isinstance(puzzle_array[other_x][other_y], list):
							if selection in puzzle_array[other_x][other_y]:
								del puzzle_array[other_x][other_y][puzzle_array[other_x][other_y].index(selection)]

			# Algorithm Failure
			failure = False
			for x_ in range(9):
				for y_ in range(9):
					if isinstance(puzzle_array[x_][y_], list):
						if len(puzzle_array[x_][y_]) == 0:
							failure = True
			if failure:
				break
		
		if not failure:
			success = True

	return puzzle_array

# ==================================================================================================== #

def value_eraser(completed_puzzle, target_remaining_values = 27):
	# Given a completed puzzle, return a puzzle_puzzle array with most of the values removed and
	# and replaced with option lists.
	
	# Copy puzzle_array
	puzzle_array = completed_puzzle[:]

	# Remove values
	remaing_values = 81
	while remaing_values > target_remaining_values:
		x, y = randint(0, 8), randint(0, 8)
		if isinstance(puzzle_array[x][y], int):
			puzzle_array[x][y] = [i for i in range(1, 10)]
			remaing_values -= 1
	
	return puzzle_array

# ==================================================================================================== #