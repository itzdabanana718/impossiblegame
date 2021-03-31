import sys
import pygame
import random
WIDTH, HEIGHT = 1000, 1000
EIGTHX, EIGTHY = WIDTH / 8, HEIGHT / 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
GRAY = (138,138,138)
final = None
moving = None
#if final does not equal none then move the chip to the position
#center of each square. Used to place each chip in the center. 
#starting in top left and moving left and down
CENTERS = []
#position of the whole square
SQUARES = []
#CENTERS
for y in range(1,17,2):
	for x in range(1,17,2):
		center = [(WIDTH/16)*x,(HEIGHT/16)*y]
		CENTERS.append(center)
#SQUARES
number = -1
for y in range(8):
	for x in range(8):
		square = [(EIGTHX * x,EIGTHY * y),(EIGTHX * (x+1),EIGTHY * (y+1))]
		SQUARES.append(square)
class pieces():
	"""a class for the 'checkers' pieces"""
	def __init__(self,center,pos):
		self.radius = WIDTH/20
		self.color = (255,0,0)
		self.center = center
		self.selected = False
		self.pos = pos
		self.outline = (255,255,255)
	def blitme(self):
		pygame.draw.circle(screen, self.color, self.center, self.radius)
		if self.selected:
			pygame.draw.circle(screen, self.outline, self.center, self.radius, width=5)
def check_keydown_events(event):
	global final, moving
	if event.key == pygame.K_q:
		sys.exit()
	if event.key == pygame.K_ESCAPE:
		unglow(moving)
		final = None
		moving = None
	if event.key == pygame.K_r:
		reset()

def check_square(pos):
	"""given the position of the mouse, return the square number that the mouse is in"""
	cur_square = None
	for square in SQUARES:
		if square[0][0] < pos[0] < square[1][0] and square[0][1] < pos[1] < square[1][1]:
			cur_square = SQUARES.index(square)
			return cur_square

def glow(selected):
	"""given the selected tile, make it glow"""
	for chip in chips:
		if chip.pos == selected:
			chip.selected = True

def unglow(selected):
	"""given the previously selected chip make it not highlighted"""
	for chip in chips:
		if chip.pos == selected:
			chip.selected = False

def check_events():
	global moving, final
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			check_keydown_events(event)
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			if moving == None:
				moving = check_square(pos)#the chip that is going to be moved
				glow(moving)
			else:
				final = check_square(pos)
				#print("here")
				move_chips(moving)

def free(tile):
	"""return True if the selected square is free and False if it is occupied"""
	free = True
	for chip in chips:
			if chip.pos == tile:
				free = False
	return free

def chip_pos(starting, direc):
	"""return the position from the list given the position on the board"""
	pos = None
	#print(starting)
	for chip in chips:
		#print(chip.pos)
		if chip.pos == starting + direc:
			pos = chips.index(chip)
	return pos

def remove_tiles(starting,finishing, direction):
	"""given the start and finishing position of a tile, remove any jumped tiles"""
	global chips
	chip_copy = chips[:]
	#print(starting + direction)
	ind = chip_pos(starting,direction)
	if ind == None:
		return False
	chip_copy.remove(chip_copy[ind])
	chips = chip_copy
	return True
def move_chips(square):
	"""given the position in the list (as an int) that the chip is in and the final 
	position, move the chips"""
	global chips, final, moving
	if not free(final):
		unglow(moving)
		final = None
		moving = None
		return
	if final not in [square-16,square+16,square+2,square-2]:
		final = None
		unglow(moving)
		moving = None
		return
	if final == square + 16:
		direction = 8
	elif final == square + 2:
		direction = 1
	elif final == square - 2:
		direction = -1
	else:
		direction = -8
	for tile in chips:
		if tile.pos == square:
			valid = remove_tiles(square,final,direction)
			unglow(square)
			if valid:
				ind = chips.index(tile)
				chips[ind].center = CENTERS[final]
				chips[ind].pos = final
			else:
				final = None
				unglow(moving)
				moving = None
				return
			unglow(moving)
			final = None
			moving = None

def draw_grid():
	"""draw an 8x8 grid"""
	#vertical lines
	pygame.draw.line(screen,(0,0,0),[WIDTH/8,HEIGHT],[WIDTH/8,0])
	pygame.draw.line(screen,(0,0,0),[EIGTHX*2,HEIGHT],[EIGTHX*2,0])
	pygame.draw.line(screen,(0,0,0),[EIGTHX*3,HEIGHT],[EIGTHX*3,0])
	pygame.draw.line(screen,(0,0,0),[EIGTHX*4,HEIGHT],[EIGTHX*4,0])
	pygame.draw.line(screen,(0,0,0),[EIGTHX*5,HEIGHT],[EIGTHX*5,0])
	pygame.draw.line(screen,(0,0,0),[EIGTHX*6,HEIGHT],[EIGTHX*6,0])
	pygame.draw.line(screen,(0,0,0),[EIGTHX*7,HEIGHT],[EIGTHX*7,0])
	#horizontal lines
	pygame.draw.line(screen,(0,0,0),[WIDTH,EIGTHY],[0,EIGTHY])
	pygame.draw.line(screen,(0,0,0),[WIDTH,EIGTHY*2],[0,EIGTHY*2])
	pygame.draw.line(screen,(0,0,0),[WIDTH,EIGTHY*3],[0,EIGTHY*3])
	pygame.draw.line(screen,(0,0,0),[WIDTH,EIGTHY*4],[0,EIGTHY*4])
	pygame.draw.line(screen,(0,0,0),[WIDTH,EIGTHY*5],[0,EIGTHY*5])
	pygame.draw.line(screen,(0,0,0),[WIDTH,EIGTHY*6],[0,EIGTHY*6])
	pygame.draw.line(screen,(0,0,0),[WIDTH,EIGTHY*7],[0,EIGTHY*7])

def update_screen():
	"""make the most recent screen visible"""
	screen.fill(GRAY)
	draw_grid()
	for piece in chips:
		piece.blitme()
	
	
	pygame.display.flip()

chips = []#used to store the pieces

def reset():
	"""reset the game"""
	global chips
	chips = []
	for i in range(32,64):
		chips.append(pieces(CENTERS[i],i))

reset()
while True:
	check_events()
	update_screen()
