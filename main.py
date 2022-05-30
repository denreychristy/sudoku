# Sudoku: Main

import pygame as pg

from printer import *
from creator import *
from copier import *

# ==================================================================================================== #

class Sudoku:

	def __init__(self):
		pg.init()
		self.clock = pg.time.Clock()
		self.tick_rate = 30

		# Window
		self.w = pg.Rect(0, 0, 800, 600)
		self.window = pg.display.set_mode(self.w.size, pg.RESIZABLE)
		pg.display.set_caption("Sudoku")

		# Font
		self.font = pg.font.get_default_font()

		# Colors
		self.color_background			= [ 31,  31,  31, 255]
		self.color_puzzle_lines			= [  0,   0,   0, 255]
		self.color_given_values			= [  0,   0, 255, 255]
		self.color_option_values		= [  0, 255,   0, 255]
		self.color_user_input_values	= [255, 255, 255, 255]
		self.color_button_new_puzzle	= [127,   0,   0, 255]
		self.color_button_show_options	= [  0, 127,   0, 255]

		# Variables
		self.puzzle_states		= []
		self.completed_puzzle	= False
		self.given_values		= False
		self.user_input_values	= False
		self.selected_cell		= [0, 0]

		# Flags
		self.flag_show_options	= False
		self.flag_puzzle_change	= False
		self.flag_option_matrix	= False

		# Main Function Call
		self.flag_run = True
		self.run_program()
		pg.quit()

	def run_program(self):
		while self.flag_run:
			self.clock.tick(self.tick_rate)

			# Variables
			self.reset_constants()
			self.VARIABLES_update_options()

			# Display
			self.window.fill(self.color_background)
			self.DISPLAY_puzzle()
			self.DISPLAY_button_new_puzzle()
			self.DISPLAY_button_show_options()
			self.DISPLAY_option_matrix()
			pg.display.flip()

			# User Input
			for event in pg.event.get():
				self.USERINPUT_quit(event)
				self.USERINPUT_button_new_puzzle(event)
				self.USERINPUT_button_show_options(event)
				self.USERINPUT_click_puzzle_cell(event)
				self.USERINPUT_adjust_options(event)

	def reset_constants(self):
		self.w = self.window.get_rect()
		self.box_size = round((min(self.w.size) / 9)) - 2
		self.button_font_size = 25

		oms = 55 # option matrix size
		self.option_matrix_locations = [
			[round(self.w.w - 2.5 * oms), round(self.w.h - 2.5 * oms)],
			[round(self.w.w - 1.5 * oms), round(self.w.h - 2.5 * oms)],
			[round(self.w.w - 0.5 * oms), round(self.w.h - 2.5 * oms)],
			[round(self.w.w - 2.5 * oms), round(self.w.h - 1.5 * oms)],
			[round(self.w.w - 1.5 * oms), round(self.w.h - 1.5 * oms)],
			[round(self.w.w - 0.5 * oms), round(self.w.h - 1.5 * oms)],
			[round(self.w.w - 2.5 * oms), round(self.w.h - 0.5 * oms)],
			[round(self.w.w - 1.5 * oms), round(self.w.h - 0.5 * oms)],
			[round(self.w.w - 0.5 * oms), round(self.w.h - 0.5 * oms)]
			]

	def save_puzzle_states(self):
		self.puzzle_states.append(copy_puzzle(self.user_input_values))

	def VARIABLES_update_options(self):
		# Only do this if there has been a change to the puzzle
		if self.flag_puzzle_change:
			for x in range(9):
				for y in range(9):
					if isinstance(self.user_input_values[x][y], int):
						selection = self.user_input_values[x][y]
						# Reassess options per row
						for other_x in range(9):
							if other_x != x:
								if isinstance(self.user_input_values[other_x][y], list):
									if selection in self.user_input_values[other_x][y]:
										del self.user_input_values[other_x][y][self.user_input_values[other_x][y].index(selection)]

						# Reassess options per column
						for other_y in range(9):
							if other_y != y:
								if isinstance(self.user_input_values[x][other_y], list):
									if selection in self.user_input_values[x][other_y]:
										del self.user_input_values[x][other_y][self.user_input_values[x][other_y].index(selection)]

						# Reassess options per box
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
									if isinstance(self.user_input_values[other_x][other_y], list):
										if selection in self.user_input_values[other_x][other_y]:
											del self.user_input_values[other_x][other_y][self.user_input_values[other_x][other_y].index(selection)]

			self.flag_puzzle_change = False

	def DISPLAY_button_new_puzzle(self):
		try:
			mouse_pos = pg.mouse.get_pos()
			mouse_over = self.button_new_puzzle_rect.collidepoint(mouse_pos)
		except:
			mouse_over = False
		
		if mouse_over:
			text_color = [255, 255, 255]
		else:
			text_color = [0, 0, 0]

		self.button_new_puzzle_text = "New Puzzle"
		self.button_new_puzzle_image = pg.font.Font(self.font, self.button_font_size).render(
			self.button_new_puzzle_text,
			True,
			text_color,
			self.color_button_new_puzzle)
		self.button_new_puzzle_rect = self.button_new_puzzle_image.get_rect(topright = [self.w.w - 5, 5])
		self.window.blit(self.button_new_puzzle_image, self.button_new_puzzle_rect)

	def DISPLAY_button_show_options(self):
		# Only show this if a puzzle has been created
		if not self.completed_puzzle:
			return False

		try:
			mouse_pos = pg.mouse.get_pos()
			mouse_over = self.button_show_options_rect.collidepoint(mouse_pos)
		except:
			mouse_over = False
		
		if mouse_over:
			text_color = [255, 255, 255]
		else:
			text_color = [0, 0, 0]

		self.button_show_options_text = "Show Options"
		self.button_show_options_image = pg.font.Font(self.font, self.button_font_size).render(
			self.button_show_options_text,
			True,
			text_color,
			self.color_button_show_options)
		self.button_show_options_rect = self.button_show_options_image.get_rect(topright = [self.w.w - 5, 10 + self.button_font_size])
		self.window.blit(self.button_show_options_image, self.button_show_options_rect)

	def DISPLAY_puzzle(self):
		# Puzzle Grid
		for i in range(10):
			line_width = 5 if i not in [0, 3, 6, 9] else 10
			pg.draw.line(
				self.window,
				self.color_puzzle_lines,
				[5 + 0 * self.box_size, 5 + i * self.box_size],
				[5 + 9 * self.box_size, 5 + i * self.box_size],
				line_width
				)
			pg.draw.line(
				self.window,
				self.color_puzzle_lines,
				[5 + i * self.box_size, 5 + 0 * self.box_size],
				[5 + i * self.box_size, 5 + 9 * self.box_size],
				line_width
				)

		# Stop function if no puzzle created yet
		if not self.completed_puzzle:
			return False

		# Given Values
		for x in range(9):
			for y in range(9):
				if isinstance(self.given_values[x][y], int):
					location = [5 + round((x + .5) * self.box_size), 10 + round((y + .5) * self.box_size)]
					text = str(self.given_values[x][y])
					font_size = self.box_size - 5
					image = pg.font.Font(self.font, font_size).render(text, True, self.color_given_values)
					rect = image.get_rect(center = location)
					self.window.blit(image, rect)

		# Option Values
		if self.flag_show_options:
			font_size = round(self.box_size / 4)
			options_rect = pg.Rect(0, 0, round(self.box_size * .7), round(self.box_size * .7))
			for x in range(9):
				for y in range(9):
					if isinstance(self.user_input_values[x][y], list):
						location = [5 + round((x + .5) * self.box_size), 5 + round((y + .5) * self.box_size)]
						options_rect.center = location
						for value in range(1, 10):
							if value in self.user_input_values[x][y]:
								value_image = pg.font.Font(self.font, font_size).render(str(value), True, self.color_option_values)
								if value == 1:
									value_rect = value_image.get_rect(topleft = options_rect.topleft)
								elif value == 2:
									value_rect = value_image.get_rect(midtop = options_rect.midtop)
								elif value == 3:
									value_rect = value_image.get_rect(topright = options_rect.topright)
								elif value == 4:
									value_rect = value_image.get_rect(midleft = options_rect.midleft)
								elif value == 5:
									value_rect = value_image.get_rect(center = options_rect.center)
								elif value == 6:
									value_rect = value_image.get_rect(midright = options_rect.midright)
								elif value == 7:
									value_rect = value_image.get_rect(bottomleft = options_rect.bottomleft)
								elif value == 8:
									value_rect = value_image.get_rect(midbottom = options_rect.midbottom)
								elif value == 9:
									value_rect = value_image.get_rect(bottomright = options_rect.bottomright)
								self.window.blit(value_image, value_rect)

		# User Input Values
		for x in range(9):
			for y in range(9):
				if isinstance(self.user_input_values[x][y], int):
					if self.user_input_values[x][y] != self.given_values[x][y]:
						location = [5 + round((x + .5) * self.box_size), 10 + round((y + .5) * self.box_size)]
						text = str(self.user_input_values[x][y])
						font_size = self.box_size - 5
						image = pg.font.Font(self.font, font_size).render(text, True, self.color_user_input_values)
						rect = image.get_rect(center = location)
						self.window.blit(image, rect)

	def DISPLAY_option_matrix(self):
		if not self.completed_puzzle:
			return False

		if not self.flag_show_options:
			return False

		for location in self.option_matrix_locations:
			pg.draw.circle(self.window, self.color_button_show_options, location, 25)

		x, y = self.selected_cell
		if isinstance(self.user_input_values[x][y], list):
			options = self.user_input_values[x][y]
			for i in range(1, 10):
				if i in options:
					image = pg.font.Font(self.font, 20).render(str(i), True, [255, 255, 255])
					rect = image.get_rect(center = self.option_matrix_locations[i - 1])
					self.window.blit(image, rect)

	def USERINPUT_quit(self, event):
		if event.type == pg.QUIT:
			self.flag_run = False

	def USERINPUT_button_new_puzzle(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			try:
				mouse_pos = pg.mouse.get_pos()
				if self.button_new_puzzle_rect.collidepoint(mouse_pos):
					self.completed_puzzle = generate_puzzle()[:]
					self.given_values = value_eraser(copy_puzzle(self.completed_puzzle))
					self.user_input_values = copy_puzzle(self.given_values)
					self.flag_puzzle_change = True

			except:
				pass

	def USERINPUT_button_show_options(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			try:
				mouse_pos = pg.mouse.get_pos()
				if self.button_show_options_rect.collidepoint(mouse_pos):
					self.flag_show_options = not self.flag_show_options
			except:
				pass

	def USERINPUT_click_puzzle_cell(self, event):
		if not self.completed_puzzle:
			return False

		if event.type == pg.MOUSEBUTTONDOWN:
			mouse_pos = pg.mouse.get_pos()
			
			cell_locations = []
			for x in range(9):
				for y in range(9):
					rect = pg.Rect(5 + x * self.box_size, 5 + y * self.box_size, self.box_size, self.box_size)
					cell_locations.append(rect)
			clicked = False
			for i, rect in enumerate(cell_locations):
				if rect.collidepoint(mouse_pos):
					x = i // 9
					y = i % 9
					clicked = True
			if not clicked:
				return False

			if isinstance(self.user_input_values[x][y], list):
				# Only one option
				if len(self.user_input_values[x][y]) == 1:
					self.save_puzzle_states()
					self.user_input_values[x][y] = self.user_input_values[x][y][0]
					self.flag_puzzle_change = True
				
				# Multiple options
				else:
					self.selected_cell = [x, y]
					self.flag_option_matrix = True

	def USERINPUT_adjust_options(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			mouse_pos = pg.mouse.get_pos()
			for i, location in enumerate(self.option_matrix_locations):
				distance = ((mouse_pos[0] - location[0]) ** 2 + (mouse_pos[1] - location[1]) ** 2) ** .5
				if distance < 25:
					option = i + 1
					x, y = self.selected_cell
					if option in self.user_input_values[x][y]:
						index = self.user_input_values[x][y].index(option)
						del self.user_input_values[x][y][index]
					else:
						self.user_input_values[x][y].append(option)

# ==================================================================================================== #

if __name__ == "__main__":
	Sudoku()