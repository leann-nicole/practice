#include <iostream>
#include <cstdlib>
using namespace std;
bool newgame=1,board_full=0;
//our 4x4 board
int board[4][4]={0};
//move all numbers to entered direction
void move(char movement);
//board after a move
void genTiles();
//add similar numbers
void add(char movement);
//displays board
int disBoard();
int main(){
	srand(clock());
	cout<<"W : up | S : down | A : left | D : right\n";
	cout<<"   Reach 2048. Don't run out of moves.\n";
	cout<<"----------------------------------------\n";
	genTiles();
	disBoard();
	//user input
	do{
	char movement;
	cin>>movement;
	switch(movement){
		case 'a':
		case 'A':
		case 'W':
		case 'w':
		case 'S':
		case 's':
		case 'D':
		case 'd':
			add(movement);	
			if(!board_full)genTiles();
			system("clear");
			cout<<"W : up | S : down | A : left | D : right\n";
			cout<<"   Reach 2048. Don't run out of moves.\n";
			cout<<"----------------------------------------\n";
			if(!disBoard())return 0;
			break;
		case 'Q':
		case 'q':
			cout<<"You quit."<<endl;
			return 0;			
		default: 
			cout<<"What do you mean?"<<endl;
	}
	}while(true);	
}
void genTiles(){
	int col=rand()%4,row=rand()%4,times=0;
	if(newgame){
		times=2;
		newgame=0;
	}
	else times=1;
	for(int a=1;a<=times;a++){
			while(board[row][col]!=0){
				col=rand()%4;
				row=rand()%4;
			}
			int num_plug=0;
			while(num_plug!=2&&num_plug!=4)num_plug=rand()%4+1;
			board[row][col]=num_plug;
	}
}
int disBoard(){
	board_full=0;
	bool is_full=1, won=0;
	for(int i=0;i<4;i++){
		for(int j=0;j<4;j++){
			if(board[i][j]==0)is_full=0;
			if(board[i][j]==2048)won=1;
			cout<<"\t";
			if(board[i][j]==0)cout<<'.'<<' ';
			else cout<<board[i][j]<<' ';
		}
		cout<<endl<<endl;
	}
	if(won){
		cout<<"\n\t\t2048 ya'll!\n";
		return 0;
	}
	if(is_full){
		bool no_moves=1;
		for(int row=0;row<4;row++){
			for(int col=0;col<3;col++){
				if(board[row][col]==board[row][col+1]){
					no_moves=0;
					goto leave;
				}
			}
		}
		for(int col=0;col<4;col++){
			for(int row=0;row<3;row++){
				if(board[row][col]==board[row+1][col]){
					no_moves=0;
					goto leave;
				}
			}
		}
		leave:
		if(no_moves){
			cout<<"\n\t\tGAME OVER\n";
			return 0;
		}
		else board_full=1;
	}
	return 1;
}
void move(char movement){
	if(movement=='a'||movement=='A'){
		for(int row=0;row<4;row++){
			for(int col=0;col<4;col++){
				int walker=col+1;
				if(board[row][col]==0){
					//look for closest non-zero number to move
					while(board[row][walker]==0&&walker<4){
						walker++;
					}
					//if a non-zero number was found
					if(walker!=4){
						board[row][col]=board[row][walker];
						board[row][walker]=0;
					}
					//row was all zeros
					else break;
				}
			}
		}
	}
	else if(movement=='w'||movement=='W'){
		for(int col=0;col<4;col++){
			for(int row=0;row<4;row++){
				int walker=row+1;
				if(board[row][col]==0){
					while(board[walker][col]==0&&walker<4){
						walker++;
					}
					if(walker!=4){
						board[row][col]=board[walker][col];
						board[walker][col]=0;
					}
					else break;
				}
			}
		}
	}
	else if(movement=='d'||movement=='D'){
		for(int row=0;row<4;row++){
			for(int col=3;col>=0;col--){
				int walker=col-1;
				if(board[row][col]==0){
					while(board[row][walker]==0&&walker>=0){
						walker--;
					}
					if(walker!=-1){
						board[row][col]=board[row][walker];
						board[row][walker]=0;
					}
					else break;
				}
			}
		}
	}
	else if(movement=='s'||movement=='S'){
		for(int col=0;col<4;col++){
			for(int row=3;row>=0;row--){
				int walker=row-1;
				if(board[row][col]==0){
					while(board[walker][col]==0&&walker>=0){
						walker--;
					}
					if(walker!=-1){
						board[row][col]=board[walker][col];
						board[walker][col]=0;
					}
					else break;
				}
			}
		}
	}
}
void add(char movement){
	if(movement=='a'||movement=='A'){
		for(int row=0;row<4;row++){
			for(int col=0;col<4;){
				if(board[row][col]!=0){
					int walker=col+1;
					while(board[row][walker]==0&&walker<4)walker++;
					if(walker<4&&board[row][walker]==board[row][col]){
							board[row][col]*=2;
							board[row][walker]=0;
					}
					col=walker;
				}
				else col++;
			}
		}
	}
	else if(movement=='w'||movement=='W'){
		for(int col=0;col<4;col++){
			for(int row=0;row<4;){
				if(board[row][col]!=0){
					int walker=row+1;
					while(board[walker][col]==0&&walker<4)walker++;
					if(walker<4&&board[walker][col]==board[row][col]){
							board[row][col]*=2;
							board[walker][col]=0;
					}
					row=walker;
				}
				else row++;
			}
		}
	}
	else if(movement=='d'||movement=='D'){
		for(int row=0;row<4;row++){
			for(int col=3;col>=0;){
				if(board[row][col]!=0){
					int walker=col-1;
					while(board[row][walker]==0&&walker>=0)walker--;
					if(walker>=0&&board[row][walker]==board[row][col]){
							board[row][col]*=2;
							board[row][walker]=0;
					}
					col=walker;
				}
				else col--;
			}
		}
	}
	else if(movement=='s'||movement=='S'){
		for(int col=0;col<4;col++){
			for(int row=3;row>=0;){
				if(board[row][col]!=0){
					int walker=row-1;
					while(board[walker][col]==0&&walker>=0)walker--;
					if(walker>=0&&board[walker][col]==board[row][col]){
							board[row][col]*=2;
							board[walker][col]=0;
					}
					row=walker;
				}
				else row--;
			}
		}
	}
	move(movement);
}
