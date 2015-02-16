import time
import math
import sys
import pygame
from pygame.locals import *

# Angles are measured in radians, because that's what the math module uses.
# Thus, right is 0, down is 0.5*math.pi, left is math.pi, and up is 1.5*math.pi.
# Also, an angle should always be positive, and under 2*math.pi.

#   y
#   |
# 3 |
#   |   x-------
# 2 |     .a)
#   |       .
# 1 |         .
#   |
# 0 +---------------x
#   0  1  2  3  4

debug = False
god = False

if "-d" in sys.argv:
	debug = True
	god = True

if "-g" in sys.argv:
	god = True

# Constants (not really meant to be configurable)
TILE = 32
pi = math.pi

# Variables (maybe read from config file?)
plane_x = 1280 # resolution of plane/screen
plane_y = 720
fov = math.radians(60)
step = 20
turn = math.radians(5)

# World Variables
hl = 100 #horiz, vert height of field
vl = 50
world = [[0 for i in range(vl)] for j in range(hl)]
p_x = 32 #player x,y
p_y = 32
p_a = 0 #pointing right

# computed variables
plane_d = (plane_x / 2) / math.tan(fov/2) #distance from player to plane
ray_angle = fov / plane_x #angle between rays

world[9][12] = 1
world[9][13] = 1
world[10][12] = 1
world[10][13] = 1

def update(oldworld):
	"""Run one *life* iteration, return the new world"""
	# Initialize a completely new array, to clear up confusion.
	newworld = [[0 for i in range(vl)] for j in range(hl)]

	# This loops through *every* cell in the world.
	for col in range(hl):
		for row in range(vl):
			# Check row above, middle row, and row beneath.
			ncount = oldworld[(col-1)%hl][(row-1)%vl] + oldworld[col][(row-1)%vl] + oldworld[(col+1)%hl][(row-1)%vl]
			ncount += oldworld[(col-1)%hl][row] + oldworld[(col+1)%hl][row]
			ncount += oldworld[(col-1)%hl][(row+1)%vl] + oldworld[col][(row+1)%vl] + oldworld[(col+1)%hl][(row+1)%vl]
			# Do things depending on the number of neighbouring cells.
			if (ncount < 2) or (ncount > 3):
				newworld[col][row] = 0
			elif ncount == 2 and oldworld[col][row] == 1:
				newworld[col][row] = 1
			elif ncount == 3:
				newworld[col][row] = 1

	return newworld


def quit():
	"""Exit cleanly."""
	pygame.quit()
	exit()


def cast(world, p_x, p_y, a):
	"""Cast a ray with angle a, and return a distance. -1 if no collision. Can also return 0."""

	if type(p_x) != int:
		exit(123)

	# max. it: use hl, vl
	# {x,y}_i are intervals, h_{x,y} is the horiz point, v_{x,y} vertical

	# If we are standing *in* a block, we return 0, which dist_to_offset() can handle.
	if world[p_x // TILE][p_y // TILE] == 1:
		return 0

	# By default, h and v checks are invalid. If we find a wall, then they become valid.
	vvalid = False
	hvalid = False

	# First we are casting for vertical intersections.
	# If the angle is pointing up or down, don't bother checking.
	# If the angle is left or right, we check with y_i = 0 and x_i = (-)TILE.
	if not (a == 0.5*pi or a == 1.5*pi):

		# Get x_i (+TILE if pointing right, -TILE if left).
		# Get v_x (x coord of the first point).
		if (a < 0.5 * pi) or (a > 1.5 * pi): # pointing right
			x_i = TILE
			v_x = (p_x // TILE)*TILE + TILE
		else:
			x_i = -1 * TILE
			v_x = (p_x // TILE)*TILE - 1

		# Get y_i, using tan.
		# Get v_y, using magic.
		if a == 0 or a == pi: # completely horizontal ray
			y_i = 0
			v_y = p_y # The ray won't 'move' on the y-axis, thus v_y is always p_y, and increments by 0.
		else:
			y_i = int(math.tan(a) * (-1) * x_i)
			v_y = int(p_y - math.tan(a)*(v_x-p_x))


		for i in range(hl): # maximum number of iterations is the number of cells along the horizontal
			try:
				if world[v_x // TILE][v_y // TILE]:
					vvalid = True
					break
			except IndexError:
				if debug:
					print("v. error!", v_x,v_y, '\n Ray:', p_x, p_y, a)
				break
			v_x += x_i
			v_y += y_i
			if v_x >= (hl*TILE) or v_y >= (vl*TILE):
				break

		# Calculate distance. All credit goes to Pythagoras.
		vdist = math.sqrt((v_x-p_x)**2 + (v_y-p_y)**2)
	
	# OK, now we'll check horizontal intersections.
	# Again, we won't check if the ray is 0° or 180°.
	if 0 and not (a == 0 or a == pi):

		# Get y_i and h_y
		if a < pi: # pointing down
			y_i = -1 * TILE
			h_y = (p_y // TILE)*TILE - 1
		else:
			y_i = TILE
			h_y = (p_y // TILE)*TILE + TILE

		# Get x_i and h_x
		if a == 0.5*pi or a == 1.5*pi: # vertical ray
			x_i = 0
			h_x = p_x
		else:
			x_i = int(-1 * y_i / math.tan(a))
			h_x = p_x # TODO: write this bit

		for i in range(vl):
			try:
				if world[h_x // TILE][h_y // TILE]:
					hvalid = True
					break
			except IndexError:
				if debug:
					print("h. error!", h_x,h_y)
				break
			h_x += x_i
			h_y += y_i
			if h_x >= (hl*TILE) or h_y >= (vl*TILE):
				break

	# Return the shortest distance.
	if vvalid and hvalid: # both rays collide
		return min(vdist, hdist)
	elif vvalid: # only vertical collision
		return vdist
	elif hvalid:
		return hdist
	else: # no collision
		return -1


def dist_to_offset(dist):
	"""Take a distance (to an object), and return the offset from the middle to start drawing the column."""
	if dist == 0:
		return plane_y * 0.5
	# Distance of -1 means no collision. So it shouldn't render anything.
	elif dist == -1:
		return 0
	else:
		return (TILE / dist) * plane_d * 0.5


def walk(world, p_x, p_y, a):
	"""Return new cords (p_x, p_y). You cannot walk into live cells or the walls"""
	# If we're in a block, don't walk.
	if world[p_x // TILE][p_y // TILE] == 1:
		return (p_x,p_y)
	if cast(world, p_x, p_y, p_a) >= step: # TODO: Make this better.
		p_y = int(p_y - (math.sin(a) * step)) % (vl*TILE)
		p_x = int(p_x + (math.cos(a) * step)) % (hl*TILE)
	return (p_x, p_y)


def draw(world):
	"""render the scene, by casting rays for each column"""
	# First we draw the background.
	screen.fill((255,255,255))
	pygame.draw.rect(screen, (200,200,200),	((0,(plane_y/2)),(plane_x,plane_y)))

	# Now we get the angle of the first ray.
	angle = (p_a - (fov/2)) % (2*pi)

	# For all columns, cast a ray, and draw a vertical line on the screen.
	for col in range(plane_x):
		dist = cast(world, p_x, p_y, angle)
		if dist != -1:
			pygame.draw.line(screen, (0,0,0), (col,((plane_y/2) - dist_to_offset(dist))), (col, (plane_y/2) + dist_to_offset(dist)))
		angle = (angle + ray_angle) % (2*pi)
	pygame.display.flip()

	# If the debug flag is set, we print debug information.
	if debug:
		print("(%d,%d) %d" % (p_x,p_y,math.degrees(p_a)))
	# If the map flag is set, print a map to stdout.
	if "-m" in sys.argv:
		for row in range(vl-1,-1,-1):
			for col in range(hl):
				if (row,col) == (p_x // TILE,p_y // TILE):
					print('x',end='')
				elif world[col][row] == 0:
					print('.',end='')
				else:
					print('#',end='')
			print('')
		print('\n')


# Initialize clock and pygame stuff.
pygame.init()
screen = pygame.display.set_mode((plane_x,plane_y))
clock = pygame.time.Clock()
tick = 30
paused = False
update_if_div_by_ten = 0

while True:
	update_if_div_by_ten += 1
	# First get a list of pressed keys.
	keys = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == QUIT:
			quit()

	if keys[K_p]:
		paused = not paused

	# These are the game controls.
	if not paused:
		if keys[K_ESCAPE]:
			quit()
		if keys[K_UP] or keys[K_w]: # go forwards
			p_x, p_y = walk(world, p_x, p_y, p_a)
		if keys[K_DOWN] or keys[K_s]: # go back
			p_x, p_y = walk(world, p_x, p_y, (p_a + pi))
		if keys[K_a] or keys[K_COMMA]: # strafe left
			p_x, p_y = walk(world, p_x, p_y, (p_a - (0.5*pi)))
		if keys[K_d] or keys[K_PERIOD]: # strafe right
			p_x, p_y = walk(world, p_x, p_y, (p_a + (0.5*pi)))
		if keys[K_LEFT]: # turn left
			p_a = (p_a - turn) % (2*pi)
		if keys[K_RIGHT]: # turn right
			p_a = (p_a + turn) % (2*pi)

	# Check if you died. We don't want this in debug mode.
	if not god:
		if world[p_x // TILE][p_y // TILE] == 1:
			print("You got mown over. By a *cell*.")
			quit()
	
	# Draw and update stuff.
	draw(world)
	clock.tick(tick)
	if (not paused) and (update_if_div_by_ten % 10 == 0):
		world = update(world)
