import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Outer_thingys finiding algo by Kronos :)")

GREEN = (6, 204, 88)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (197, 35, 48)
Outer_thingys = (18, 148, 71) 
end = (0, 120, 255)
idk = (44, 62, 80)
start = (14, 240, 191)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = idk
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == GREEN

	def is_open(self):
		return self.color == Outer_thingys

	def is_Outer_thingys(self):
		return self.color == PURPLE

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == start

	def is_end(self):
		return self.color == end

	def reset(self):
		self.color = idk

	def make_start(self):
		self.color = start

	def make_closed(self):
		self.color = GREEN

	def make_open(self):
		self.color = Outer_thingys

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = end

	def make_Outer_thingys(self):
		self.color = PURPLE

	def draw(self, win):
		
		if self.color == Outer_thingys or self.color == PURPLE:
			if self.color != Outer_thingys:	
				pygame.draw.rect(win, (0, 255, 106), (self.x, self.y, self.width, self.width))
				pygame.draw.circle(win, self.color, (self.x+self.width//2, self.y+self.width//2), self.width//3)
			else:
				pygame.draw.circle(win, GREEN, (self.x+self.width//2, self.y+self.width//2), self.width//3)
				# pygame.draw.circle(win, (242, 242, 0), (self.x+self.width//2, self.y+self.width//2), self.width//3)
		else:
			pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_Outer_thingys(came_from, current, draw, Start):
	del came_from[next(iter(came_from))]
	del came_from[next(iter(came_from))]
	del came_from[next(iter(came_from))]
	del came_from[next(iter(came_from))]
	while current in came_from:
		current = came_from[current]
		current.make_Outer_thingys()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_Outer_thingys(came_from, end, draw, start)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(idk)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)
				
				if event.key == pygame.K_r:
					for row in grid:
						for spot in row:
							if spot.is_closed() or spot.is_open() or spot.is_Outer_thingys():
								spot.reset()

				if event.key == pygame.K_w:
					for row in grid:
						for spot in row:
							if spot.is_barrier() or spot.is_closed() or spot.is_open() or spot.is_Outer_thingys():
								spot.reset()

	pygame.quit()

main(WIN, WIDTH)