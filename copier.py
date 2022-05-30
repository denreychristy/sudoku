# Sudoku: Copier

def copy_puzzle(puzzle_array):
	new_array = [[[] for _ in range(9)] for _ in range(9)]
	for x in range(9):
		for y in range(9):
			if isinstance(puzzle_array[x][y], int):
				new_array[x][y] = puzzle_array[x][y]
			elif isinstance(puzzle_array[x][y], list):
				new_array[x][y] = [i for i in puzzle_array[x][y]]
	return new_array