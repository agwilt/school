#include <stdio.h>

static int solved = 0;

void solve(int maze[9][9], int x, int y)
{
	if (maze[x][y] == 2) {
		solved = 1;
	} else if (maze[x][y] == 0) {
		maze[x][y] = 8;
		solve(maze, x, (y+1));
		if ( solved == 0 ) {
			solve(maze, (x+1), y);
		} if ( solved == 0 ) {
			solve(maze, (x-1), y);
		} if ( solved == 0 ) {
			solve(maze, x, (y-1));
		} if ( solved == 0 ) {
			maze[x][y] = 0;
		}
	}
}

int main()
{
	int maze[9][9] = {
		{1,1,1,1,1,1,1,1,1},
		{1,0,0,0,1,0,0,0,1},
		{1,1,1,0,1,0,1,0,1},
		{0,0,0,0,0,0,1,0,1},
		{1,1,1,1,1,1,1,0,1},
		{1,0,0,0,0,0,1,0,1},
		{1,0,1,1,1,0,1,0,1},
		{1,0,0,0,1,0,0,0,1},
		{1,1,1,2,1,1,1,1,1}};
	int x = 3;
	int y = 0;
	solve(maze, x, y);
	for ( int i = 0; i < 9; i++) {
		for ( int j = 0; j < 9; j++) {
			printf("%d", maze[i][j]);
		}
		printf(" %d \n", i);
	}
}
