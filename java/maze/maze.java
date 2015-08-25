
/**
 * Write a description of class maze here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class maze
{
    // instance variables - replace the example below with your own
    private int map[][];
    private boolean solved;
    private int test[];

    /**
     * Constructor for objects of class maze
     */
    public maze()
    {
        // initialise instance variables
        map = new int[][] {
            {1,1,1,1,1,1},
            {0,0,0,1,0,1},
            {1,1,0,0,0,1},
            {1,0,1,1,0,1},
            {1,0,0,0,0,1},
            {1,2,1,1,1,1}
            };
        solve(1, 0);
        for (int i=0; i<6; i++) {
            for (int j=0; j<6; j++) {
                System.out.printf("%d", map[i][j]);
            }
            System.out.println("");
        }
                
    }

    /**
     * recursive solve method
     */
    public void solve(int x, int y)
    {
        // put your code here
        if ( map[x][y] == 2 ) {
            solved = true;
        } else if ( map[x][y] == 0 ) {
            map[x][y] = 8;
            solve(x, y+1);
            if ( ! solved ) {
                solve(x+1, y);
            } if ( ! solved ) {
                solve(x-1, y);
            } if ( ! solved ) {
                solve(x, y-1);
            } if ( ! solved ) {
                map[x][y] = 0;
            }
        }
    }
}
