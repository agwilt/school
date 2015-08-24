#!/usr/bin/env python3

maze = [['#','#','#','#','#','#','#','#','#'],
		['#',' ',' ',' ','#',' ',' ',' ','#'],
		['#','#','#',' ','#',' ','#',' ','#'],
		[' ',' ',' ',' ',' ',' ','#',' ','#'],
		['#','#','#','#','#','#','#',' ','#'],
		['#',' ',' ',' ',' ',' ','#',' ','#'],
		['#',' ','#','#','#',' ','#',' ','#'],
		['#',' ',' ',' ','#',' ',' ',' ','#'],
		['#','#','#','Z','#','#','#','#','#']]

pos = [3,0]
solved = False

def check(pos, direction):
	direction %= 4
	try:
		if direction == 0:
			return maze[pos[0]][pos[1]+1]
		if direction == 1:
			return maze[pos[0+1]][pos[1]]
		if direction == 2:
			return maze[pos[0]][pos[1]-1]
		if direction == 3:
			return maze[pos[0-1]][pos[1]]
	except:
		return 0
	return 0

def solve(maze, pos):
	global solved

	if maze[pos[0]][pos[1]] == 'Z':
		solved = True
	elif maze[pos[0]][pos[1]] == ' ':
		maze[pos[0]][pos[1]] = '.'
		solve(maze, [pos[0],pos[1]+1])
		if not solved:
			solve(maze, [pos[0]+1,pos[1]])
		if not solved:
			solve(maze, [pos[0]-1,pos[1]])
		if not solved:
			solve(maze, [pos[0],pos[1]-1])
		if not solved:
			maze[pos[0]][pos[1]] = ' '


solve(maze, pos)
for line in maze:
	for col in line:
		print(col, end='')
	print('')



"""
#needs to keep going in direction it was before
def move(pos, direction=0):
	print(pos)
	if maze[pos[0]][pos[1]] == 2:
		return 2
	# is field to the right empty
	if check(pos, 0+direction): #fwd
		pos[1] += 1
		if move(pos, direction=direction) == 2:
			
	elif check(pos, 1+direction): #right
		pos[0] += 1
	elif check(pos, 3+direction): #left
		pos[0] -= 1
	else:
		return 0	# have to go back
	move(pos, direction=direction)
"""
