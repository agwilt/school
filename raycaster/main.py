import time, math, sys
import pygame
from pygame.locals import *

# angles are in radians
# (0,0) is in the bottom left
# 0 is pointing to the right
# pi/2 is pointing down
# pi is pointing left
# 1.5 pi is pointing up

debug = False

if "-d" in sys.argv:
	debug = True

# Constants (not really configurable)
TILE = 32

# variables (maybe read from config file?)
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
p_height = TILE / 2

# computed variables
plane_d = (plane_x / 2) / math.tan(fov/2) #distance from player to plane
ray_angle = fov / plane_x #angle between rays

world[7][11] = 1
world[7][14] = 1
world[8][10] = 1
world[9][10] = 1
world[9][14] = 1
world[10][10] = 1
world[10][11] = 1
world[10][12] = 1
world[10][13] = 1

world[19][20] = 1
world[21][20] = 1
world[20][20] = 1
world[20][21] = 1
world[20][22] = 1
world[20][23] = 1
world[20][24] = 1
world[19][24] = 1
world[21][24] = 1

def update(oldworld):
	"""Runs one *life* iteration, returns the new world"""
	newworld = [[0 for i in range(vl)] for j in range(hl)]
	for col in range(hl):
		for row in range(vl):
			ncount = oldworld[(col-1)%hl][(row-1)%vl] + oldworld[col][(row-1)%vl] + oldworld[(col+1)%hl][(row-1)%vl]
			ncount += oldworld[(col-1)%hl][row] + oldworld[(col+1)%hl][row]
			ncount += oldworld[(col-1)%hl][(row+1)%vl] + oldworld[col][(row+1)%vl] + oldworld[(col+1)%hl][(row+1)%vl]
			if (ncount < 2) or (ncount > 3):
				newworld[col][row] = 0
			elif ncount == 2 and oldworld[col][row] == 1:
				newworld[col][row] = 1
			elif ncount == 3:
				newworld[col][row] = 1
	return newworld

def quit():
	"""exit cleanly. I might add stuff like a highscore."""
	pygame.quit()
	exit()

def cast(world, p_x, p_y, a):
	"""casts a ray, return distance, -1 if no collision"""
	# TODO: add special cases for (p_a == 0 or p_a == 180)
	# max. it: use hl, vl
	# {x,y}_i are increments, h_{x,y} is the horiz point, v_{x,y} vertical
	# OK, horizontal checks first. use TILE as x_i
	#write later
	if world[p_x // 64][p_y // 64] == 1:
		return -1
	return math.degrees(a)

def dist_to_offset(dist):
	"""takes a distance (to an object), and returns the offset from the middle to start drawing the column."""
	if dist == 0:
		return plane_y * 0.5
	elif dist == -1:
		return 0
	else:
		return (TILE / dist) * plane_d * 0.5

def walk(world, p_x, p_y, a):
	"""return new cords (p_x, p_y). You cannot walk into live cells or the walls"""
	if world[p_x // TILE][p_y // TILE] == 1:
		return (p_x,p_y)
	if cast(world, p_x, p_y, p_a) >= step:
		p_y = int(p_y - (math.sin(a) * step)) % (vl*TILE)
		p_x = int(p_x + (math.cos(a) * step)) % (hl*TILE)
	return (p_x, p_y)

def draw(world):
	"""render the scene, by casting rays for each column"""
	screen.fill((255,255,255))
	pygame.draw.rect(screen, (200,200,200), ((0,(plane_y/2)),(plane_x,plane_y)))
	angle = (p_a - (fov/2)) % (2*math.pi)
	for col in range(plane_x):
		dist = cast(world, p_x, p_y, angle)
		if dist > 0:
			pygame.draw.line(screen, (0,0,0), (col,((plane_y/2) - dist_to_offset(dist))), (col, (plane_y/2) + dist_to_offset(dist)))
		angle = (angle + ray_angle) % (2*math.pi)
	pygame.display.flip()
	# print map to stdout
	if debug:
		print("(%d,%d) %d" % (p_x,p_y,math.degrees(p_a)))
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

#initialize pygame stuff
pygame.init()
screen = pygame.display.set_mode((plane_x,plane_y))
clock = pygame.time.Clock()
tick = 30
paused = False

while True:
	keys = pygame.key.get_pressed() # get all pressed keys
	for event in pygame.event.get():
		if event.type == QUIT:
			quit()
	if keys[K_p]:
		paused = not paused
	if not paused:
		if keys[K_ESCAPE]:
			quit()
		if keys[K_UP] or keys[K_w]: # go forwards
			p_x, p_y = walk(world, p_x, p_y, p_a)
		if keys[K_DOWN] or keys[K_s]: # go back
			p_x, p_y = walk(world, p_x, p_y, (p_a + math.pi))
		if keys[K_a] or keys[K_COMMA]: # strafe left
			p_x, p_y = walk(world, p_x, p_y, (p_a - (0.5*math.pi)))
		if keys[K_d] or keys[K_PERIOD]: # strafe right
			p_x, p_y = walk(world, p_x, p_y, (p_a + (0.5*math.pi)))
		if keys[K_LEFT]: # turn left
			p_a = (p_a - turn) % (2*math.pi)
		if keys[K_RIGHT]: # turn right
			p_a = (p_a + turn) % (2*math.pi)
	if not debug:
		if world[p_x // TILE][p_y // TILE] == 1:
			print("You got mown over. By a *cell*.")
			quit()
	draw(world)
	clock.tick(tick)
	if not paused:
		world = update(world)
