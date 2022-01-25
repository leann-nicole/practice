#include <iostream>
#define S 9
#define RANGE 10
using namespace std;

bool solve_sudoku(int board[S][S], int row, int col);
void copy_board(int a[S][S], int b[S][S]);
bool valid(int board[S][S]);
void printBoard(int board[S][S]);

int main(){
	int sudokuBoard[S][S] =
		{ 
	    /*
		 {0,7,0,0,0,0,0,0,9},  //solvable in 1095 recursions
		 {5,1,0,4,2,0,6,0,0},
		 {0,8,0,3,0,0,7,0,0},
		 {0,0,8,0,0,1,3,7,0},
		 {0,2,3,0,8,0,0,4,0},
		 {4,0,0,9,0,0,1,0,0},
		 {9,6,2,8,0,0,0,3,0},
		 {0,0,0,0,1,0,4,0,0},
		 {7,0,0,2,0,3,0,9,6}
	   */
		 {0,0,0,8,0,0,0,0,0},  //solvable in 52770 recursions
		 {4,0,0,0,1,5,0,3,0},
		 {0,2,9,0,4,0,5,1,8},
		 {0,4,0,0,0,0,1,2,0},
		 {0,0,0,6,0,2,0,0,0},
		 {0,3,2,0,0,0,0,9,0},
		 {6,9,3,0,5,0,8,7,0},
		 {0,5,0,4,8,0,0,0,1},
		 {0,0,0,0,0,3,0,0,0},
	    /*
		 {2,0,0,9,0,0,0,0,0},  // bonkers grid
		 {0,0,0,0,0,0,0,6,0},
		 {0,0,0,0,0,1,0,0,0},
		 {5,0,2,6,0,0,4,0,7},
		 {0,0,0,0,0,4,1,0,0},
		 {0,0,0,0,9,8,0,2,3},
		 {0,0,0,0,0,3,0,8,0},
		 {0,0,5,0,1,0,0,0,0},
		 {0,0,7,0,0,0,0,0,0},
	   */ 
		};
	cout<<"\n  ORIGINAL BOARD\n";
	printBoard(sudokuBoard);

	if(solve_sudoku(sudokuBoard,0,0)){
		cout<<"   FINAL BOARD\n";
		printBoard(sudokuBoard);
	}
	else cout<<" BOARD UNSOLVABLE\n"<<endl;
	
	return 0;
}

void printBoard(int board[S][S]){
	cout<<endl;
	for(int i=0; i<S; i++){
		for(int j=0; j<S; j++){
			cout<<board[i][j]<<' ';
		}
		cout<<endl;
	}
	cout<<endl;
}

void copy_board(int a[S][S], int b[S][S]){
	for(int i=0; i<S; i++)
		for(int j=0; j<S; j++)
			a[i][j] = b[i][j];
}

bool valid(int board[S][S]){
	/*
	  check uniqueness in:
	  1  each 3x3 subgrid
	  2  each row
	  3  each column
	*/
	
	// 1 
	for(int Row=0; Row<(RANGE-1); Row+=3){
		for(int Col=0; Col<(RANGE-1); Col+=3){
			//if frequency of a number becomes greater than 1, return false
			int freq[RANGE]={0};
			for(int subRow=Row; subRow<Row+3; subRow++){
				for(int subCol=Col; subCol<Col+3; subCol++){
					if(board[subRow][subCol] != 0){
						freq[board[subRow][subCol]]++;
						if(freq[board[subRow][subCol]] > 1)return false;
					}
				}
			}
		}
	}
	// 2
	for(int Row=0; Row<(RANGE-1); Row++){
		int freq[RANGE] = {0};
		for(int Col=0; Col<(RANGE-1); Col++){
			if(board[Row][Col] != 0){
				freq[board[Row][Col]]++;
				if(freq[board[Row][Col]] > 1)return false;
			}
		}
	}
	// 3
	for(int Col=0; Col<(RANGE-1); Col++){
		int freq[RANGE] = {0};
		for(int Row=0; Row<(RANGE-1); Row++){
			if(board[Row][Col] != 0){
				freq[board[Row][Col]]++;
				if(freq[board[Row][Col]] > 1)return false;
			}
		}
	}
	
	//if all iterations were completed, there must be no duplicates
	return true;
}

bool solve_sudoku(int board[S][S], int row, int col){
	/*
	  
	We can add a threshold for the number of recursions.
	This can handle grid number 3.
	Be careful though. Valid boards differ greatly in the number of recursions it takes to solve them.
	 
	static int threshold = 0;
	threshold++; 
	if(threshold > input_desired_limit_here)return false;
	
	*/
	
	if(!valid(board))return false;
		
	if(row == S)return true;
	
	if(board[row][col] != 0){ //if box is already filled, just proceed to next box
		if(col != S-1){
			return(solve_sudoku(board, row, col+1));
			}
		else if(col == S-1){
			return(solve_sudoku(board, row+1, 0));
		}
	}
	else{ 
		int boardCopy[S][S];
		for(int n=1; n<RANGE; n++){
			copy_board(boardCopy, board);
			boardCopy[row][col] = n;
		
			if(col != S-1){
				if(solve_sudoku(boardCopy, row, col+1)){
					copy_board(board,boardCopy);
					return true;
				}
			}
			else if(col == S-1){
				if(solve_sudoku(boardCopy, row+1, 0)){
					copy_board(board,boardCopy);
					return true;
				}
			}
		}
		return false; //none in 1-9 solves the board
	}
}
