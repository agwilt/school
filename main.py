import time, math
import pygame
from pygame.locals import *

# angles are in radians
# (0,0) is in the top left
# 0 is pointing to the right
# pi/2 is pointing up
# pi is pointing left
# 1.5 pi is pointing down

# Constants (not really configurable)
TILE = 64

# variables (maybe read from config file?)
plane_x = 800 # resolution of plane/screen
plane_y = 600
fov = math.radians(60)
step = 10
turn = math.radians(10)

# World Variables
hl = 100 #horiz, vert height of field
vl = 50
world = [[0 for i in range(hl)] for j in range(vl)]
p_x = 32 #player x,y
p_y = 32
p_a = 0 #pointing right
p_height = 32

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
	newworld = [[0 for i in range(hl)] for j in range(vl)]
	for row in range(vl):
		for col in range(hl):
			ncount = 0
			ncount += oldworld[(row-1)%vl][(col-1)%hl] + oldworld[(row-1)%vl][col] + oldworld[(row-1)%vl][(col+1)%hl]
			ncount += oldworld[row][(col-1)%hl] + oldworld[row][(col+1)%hl]
			ncount += oldworld[(row+1)%vl][(col-1)%hl] + oldworld[(row+1)%vl][col] + oldworld[(row+1)%vl][(col+1)%hl]
			if (ncount < 2) or (ncount > 3):
				newworld[row][col] = 0
			elif ncount == 2 and oldworld[row][col] == 1:
				newworld[row][col] = 1
			elif ncount == 3:
				newworld[row][col] = 1
	return newworld

def quit():
	exit()

def draw(world):
	for row in range(vl):
		for col in range(hl):
			if world[row][col] == 0:
				print('.',end='')
			else:
				print('#',end='')
		print('')
	print('\n(%d,%d) A %d' % (p_x, p_y, math.degrees(p_a)))
	if paused:
		print("P A U S E D")

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
				p_y = (p_y + math.sin(p_a) * step) % vl
				p_x = (p_x + math.cos(p_a) * step) % hl
			if keys[K_DOWN] or keys[K_s]: # go back
				p_y = (p_y - math.sin(p_a) * step) % vl
				p_x = (p_x - math.cos(p_a) * step) % vl
			if keys[K_a] or keys[K_COMMA]: # strafe left
				p_y = (p_y + math.sin(p_a - math.radians(90)) * step) % vl
				p_x = (p_x + math.cos(p_a - math.radians(90)) * step) % hl
			if keys[K_d] or keys[K_PERIOD]: # strafe right
				p_y = (p_y - math.sin(p_a + math.radians(90)) * step) % vl
				p_x = (p_x - math.cos(p_a + math.radians(90)) * step) % hl
			if keys[K_LEFT]: # turn left
				p_a -= turn
			if keys[K_RIGHT]: # turn right
				p_a += turn
	draw(world)
	clock.tick(tick)
	if not paused:
		world = update(world)
