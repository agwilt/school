import time, copy

wl = 50

hl = 100
vl = 50

world = [[0 for i in range(wl)] for j in range(wl)]

world[10][10] = 1
world[10][11] = 1
world[10][12] = 1
world[8][11] = 1
world[9][12] = 1

def update(oldworld):
	newworld = [[0 for i in range(wl)] for j in range(wl)]
	for row in range(wl):
		for col in range(wl):
			ncount = 0
			ncount += oldworld[(row-1)%wl][(col-1)%wl] + oldworld[(row-1)%wl][col] + oldworld[(row-1)%wl][(col+1)%wl]
			ncount += oldworld[row][(col-1)%wl] + oldworld[row][(col+1)%wl]
			ncount += oldworld[(row+1)%wl][(col-1)%wl] + oldworld[(row+1)%wl][col] + oldworld[(row+1)%wl][(col+1)%wl]
			if (ncount < 2) or (ncount > 3):
				newworld[row][col] = 0
			elif ncount == 2 and oldworld[row][col] == 1:
				newworld[row][col] = 1
			elif ncount == 3:
				newworld[row][col] = 1
	return newworld

def draw(world):
	for row in range(wl):
		for col in range(wl):
			if world[row][col] == 0:
				print('.',end='')
			else:
				print('#',end='')
		print('')
	print('\n')

while True:
	draw(world)
	time.sleep(0.1)
	world = update(world)
