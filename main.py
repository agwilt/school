import time, copy

world = [[0,0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0,0]]

wl = len(world)

def update(oldworld):
	newworld = [[0 for i in range(wl)] for j in range(wl)]
	for row in range(wl):
		print("***ROW %d***" % row)
		for col in range(wl):
			ncount = 0
			print("COL %d" % col)
			ncount = oldworld[row][(col-1)%wl] + oldworld[row][(col+1)%wl]
			ncount += oldworld[(row-1)%wl][(col-1)%wl] + oldworld[(row-1)%wl][col] + oldworld[(row-1)%wl][(col+1)%wl]
			ncount += oldworld[(row+1)%wl][(col-1)%wl] + oldworld[(row+1)%wl][col] + oldworld[(row+1)%wl][(col+1)%wl]
			print(ncount)
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
	time.sleep(0.5)
	world = update(world)
