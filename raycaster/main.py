#!/usr/bin/env python3
"I hope you're not trying to import this in python. It's not really meant to work that way ..."

import math
import sys
import pygame
from pygame.locals import *

# Angles are measured in radians, because that's what the math module uses.
# Thus, right is 0, down is PI, left is PI, and up is 1.5*PI.
# Also, an angle should always be positive, and under 2*PI.

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

DEBUG = False
GOD = False

if "-d" in sys.argv:
	DEBUG = True
	GOD = True

if "-g" in sys.argv:
	GOD = True

# Constants (not really meant to be configurable)
TILE = 32
PI = math.pi

# Variables (maybe read from config file?)
TICK = 30
PLANE_X = 640  # resolution of plane/screen
PLANE_Y = 480
FOV = math.radians(60)
STEP = 20
TURN = math.radians(5)
HL = 100  # horiz, vert height of field
VL = 50

# computed variables
PLANE_D = (PLANE_X / 2) / math.tan(FOV/2)  #distance from player to plane
RAY_ANGLE = FOV / PLANE_X  # angle between rays

def update(oldworld):
	"""Run one *life* iteration, return the new world"""
	# Initialize a completely new array, to clear up confusion.
	newworld = [[0 for i in range(VL)] for j in range(HL)]

	# This loops through *every* cell in the world.
	for col in range(HL):
		for row in range(VL):
			# Check row above, middle row, and row beneath.
			ncount = oldworld[(col-1) % HL][(row-1) % VL] + \
			oldworld[col][(row-1) % VL] + oldworld[(col+1) % HL][(row-1) % VL]
			ncount += oldworld[(col-1) % HL][row] + oldworld[(col+1) % HL][row]
			ncount += oldworld[(col-1) % HL][(row+1) % VL] + \
			oldworld[col][(row+1) % VL] + oldworld[(col+1) % HL][(row+1) % VL]
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

	# max. it: use HL, VL
	# {x,y}_i are intervals, h_{x,y} is the horiz point, v_{x,y} vertical

	# If we are standing *in* a block, we return 0, which
	# dist_to_offset() can handle.
	if world[p_x // TILE][p_y // TILE] == 1:
		return 0

	# By default, h and v checks are invalid.
	# If we find a wall, then they become valid.
	vvalid = False
	hvalid = False

	# First we are casting for vertical intersections.
	# If the angle is pointing up or down, don't bother checking.
	# If the angle is left or right, we check with y_i = 0 and x_i = (-)TILE.
	if not (a == 0.5*PI or a == 1.5*PI):

		# Get x_i (+TILE if pointing right, -TILE if left).
		# Get v_x (x coord of the first point).
		if (a < 0.5 * PI) or (a > 1.5 * PI):  # pointing right
			x_i = TILE
			v_x = (p_x // TILE)*TILE + TILE
		else:
			x_i = -1 * TILE
			v_x = (p_x // TILE)*TILE - 1

		# Get y_i, using tan.
		# Get v_y, using magic.
		y_i = int(math.tan(a) * (-1) * x_i)
		v_y = int(p_y - math.tan(a)*(v_x-p_x))

		while True:
			if v_x < 0 or v_y < 0 or v_x >= (HL*TILE) or v_y >= (VL*TILE):
				break
			if world[v_x // TILE][v_y // TILE]:
				vvalid = True
				break
			v_x += x_i
			v_y += y_i

		# Calculate distance. All credit goes to Pythagoras.
		vdist = math.sqrt((v_x-p_x)**2 + (v_y-p_y)**2)
	
	# OK, now we'll check horizontal intersections.
	# Again, we won't check if the ray is 0° or 180°.
	if not (a == 0 or a == PI):

		# Get y_i and h_y
		if a < PI:  # pointing down
			y_i = -1 * TILE
			h_y = (p_y // TILE)*TILE - 1
		else:
			y_i = TILE
			h_y = (p_y // TILE)*TILE + TILE

		# Get x_i and h_x
		if a == 0.5*PI or a == 1.5*PI:  # vertical ray
			x_i = 0
			h_x = p_x
		else:
			x_i = int(-1 * y_i / math.tan(a))
			h_x = int(p_x - ((p_y - h_y) / math.tan(a)))

		while True:
			if h_x < 0 or h_y < 0 or h_x >= (HL*TILE) or h_y >= (VL*TILE):
				break
			if world[h_x // TILE][h_y // TILE]:
				hvalid = True
				break
			h_x += x_i
			h_y += y_i

		hdist = math.sqrt((h_x-p_x)**2 + (h_y-p_y)**2)

	# Return the shortest distance.
	if vvalid and hvalid:  # both rays collide
		return min(vdist, hdist)
	elif vvalid:  # only vertical collision
		return vdist
	elif hvalid:
		return hdist
	else:  # no collision
		return -1


def dist_to_offset(dist):
	"""Take a distance (to an object), and return the offset from the middle to start drawing the column."""
	if dist == 0:
		return PLANE_Y * 0.5
	# Distance of -1 means no collision. So it shouldn't render anything.
	elif dist == -1:
		return 0
	else:
		return (TILE / dist) * PLANE_D * 0.5


def walk(world, p_x, p_y, a):
	"""Return new cords (p_x, p_y)."""
	p_y = int(p_y - (math.sin(a) * STEP)) % (VL*TILE)
	p_x = int(p_x + (math.cos(a) * STEP)) % (HL*TILE)
	return (p_x, p_y)


def draw(world, p_x, p_y, p_a, screen):
	"""render the scene, by casting rays for each column"""
	# First we draw the background.
	screen.fill((255,255,255))
	pygame.draw.rect(screen, (200,200,200),	((0,(PLANE_Y/2)),(PLANE_X,PLANE_Y)))

	# Now we get the angle of the first ray.
	angle = (p_a - (FOV/2)) % (2*PI)

	# For all columns, cast a ray, and draw a vertical line on the screen.
	for col in range(PLANE_X):
		dist = cast(world, p_x, p_y, angle)
		if dist != -1:
			pygame.draw.line(screen, (0,0,0), \
			(col,((PLANE_Y/2) - dist_to_offset(dist))), \
			(col, (PLANE_Y/2) + dist_to_offset(dist)))
		angle = (angle + RAY_ANGLE) % (2*PI)
	pygame.display.flip()

	# If the DEBUG flag is set, we print DEBUG information.
	if DEBUG:
		print("(%d,%d) %d" % (p_x,p_y,math.degrees(p_a)))
	# If the map flag is set, print a map to stdout.
	if "-m" in sys.argv:
		for row in range(VL-1,-1,-1):
			for col in range(HL):
				if (row,col) == (p_x // TILE,p_y // TILE):
					print('x',end='')
				elif world[col][row] == 0:
					print('.',end='')
				else:
					print('#',end='')
			print('')
		print('\n')


def main():
	# Initialize clock and pygame stuff.
	pygame.init()
	screen = pygame.display.set_mode((PLANE_X,PLANE_Y))
	clock = pygame.time.Clock()
	paused = False
	should_update = 0

	# World Variables
	world = [[0 for i in range(VL)] for j in range(HL)]
	p_x = 32  # player x,y
	p_y = 32
	p_a = 0  # pointing right

	world[8][13] = 1
	world[9][14] = 1
	world[10][12] = 1
	world[10][13] = 1
	world[10][14] = 1

	while True:
		should_update += 1
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
			if keys[K_UP]:  # go forwards
				p_x, p_y = walk(world, p_x, p_y, p_a)
			if keys[K_DOWN]:  # go back
				p_x, p_y = walk(world, p_x, p_y, (p_a + PI))
			if keys[K_COMMA]:  # strafe left
				p_x, p_y = walk(world, p_x, p_y, (p_a - (0.5*PI)))
			if keys[K_PERIOD]:  # strafe right
				p_x, p_y = walk(world, p_x, p_y, (p_a + (0.5*PI)))
			if keys[K_LEFT]:  # turn left
				p_a = (p_a - TURN) % (2*PI)
			if keys[K_RIGHT]:  # turn right
				p_a = (p_a + TURN) % (2*PI)

		# Check if you died. We don't want this in DEBUG mode.
		if not GOD:
			if world[p_x // TILE][p_y // TILE] == 1:
				print("You got mown over. By a *cell*.")
				quit()
		
		# Draw and update stuff.
		draw(world, p_x, p_y, p_a, screen)
		clock.tick(TICK)
		if (not paused) and (should_update % 5 == 0):
			world = update(world)

if __name__ == "__main__":
	main()
