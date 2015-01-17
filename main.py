import time, copy

hl = 100
vl = 50

world = [[0 for i in range(hl)] for j in range(vl)]

world[10][10] = 1
world[10][11] = 1
world[10][12] = 1
world[8][11] = 1
world[9][12] = 1

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

def draw(world):
	for row in range(vl):
		for col in range(hl):
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
