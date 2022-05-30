# Sudoku: Print to Console Functions

# ==================================================================================================== #

# Print Functions
def print_options_array(puzzle):
	horizontal_double_line = "==========================================================="
	horizontal_single_line = "||-----|-----|-----||-----|-----|-----||-----|-----|-----||"

	print(horizontal_double_line)
	
	for y in range(9):
		line = "|| "
		for x in range(9):
			if isinstance(puzzle[x][y], list):
				line += "1" if 1 in puzzle[x][y] else " "
				line += "2" if 2 in puzzle[x][y] else " "
				line += "3" if 3 in puzzle[x][y] else " "
				line += " | "
			else:
				line += "   " + " | "
			if x in [2, 5, 8]:
					line = line[0 : -1]
					line += "| "
		print(line)

		line = "|| "
		for x in range(9):
			if isinstance(puzzle[x][y], list):
				line += "4" if 4 in puzzle[x][y] else " "
				line += "5" if 5 in puzzle[x][y] else " "
				line += "6" if 6 in puzzle[x][y] else " "
				line += " | "
			else:
				line += "   " + " | "
			if x in [2, 5, 8]:
					line = line[0 : -1]
					line += "| "
		print(line)

		line = "|| "
		for x in range(9):
			if isinstance(puzzle[x][y], list):
				line += "7" if 7 in puzzle[x][y] else " "
				line += "8" if 8 in puzzle[x][y] else " "
				line += "9" if 9 in puzzle[x][y] else " "
				line += " | "
			else:
				line += "   " + " | "
			if x in [2, 5, 8]:
					line = line[0 : -1]
					line += "| "

		print(line)

		if y not in [2, 5, 8]:
			print(horizontal_single_line)
		else:
			print(horizontal_double_line)

# ==================================================================================================== #

def print_puzzle(puzzle):
	horizontal_double_line = "========================================="
	horizontal_single_line = "||---|---|---||---|---|---||---|---|---||"

	print(horizontal_double_line)

	for y in range(9):
		line = "||"
		for x in range(9):
			value = str(puzzle[x][y]) if isinstance(puzzle[x][y], int) else " "
			line += " " + value + " " + "|"
			if x in [2, 5, 8]:
				line += "|"
		print(line)

		if y not in [2, 5, 8]:
			print(horizontal_single_line)
		else:
			print(horizontal_double_line)