#!/usr/bin/env python3

maze = [['#','#','#','#','#','#','#','#','#'],
		['#',' ',' ',' ',' ',' ',' ',' ','#'],
		['#','#','#',' ','#','#','#',' ','#'],
		[' ',' ',' ',' ',' ',' ','#',' ','#'],
		['#','#','#','#','#','#','#',' ','#'],
		['#',' ',' ',' ',' ',' ','#',' ','#'],
		['#',' ','#','#','#',' ','#',' ','#'],
		['#',' ',' ',' ','#',' ',' ',' ','#'],
		['#','#','#','Z','#','#','#','#','#']]

pos = [3,0]
solved = False

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


if __name__ == "__main__":
	solve(maze, pos)
	for line in maze:
		for col in line:
			print(col, end='')
		print('')
