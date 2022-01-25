#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#define S 16
using namespace std;
// A* pathfinding algorithm

class Point{
	
	public:
		int x,y; //coordinate on the grid
		int G;   //distance from start point
		int H;   //distance from end point
		int F;   // H + G
		Point* Parent;
		Point(int a, int b):x(a),y(b){}; //constructor for end Point
		Point(int a, int b, Point* parent, Point* end):x(a),y(b){
			Parent = parent;
			if(parent == NULL) G = 0; //a starting point
			else{ //calculate G
				if(parent->x != x && parent->y != y)G = parent->G + 14;
				else G = parent->G + 10;
			}
			if(end == NULL) H = 0; //an end point
			else{ //calculate H 
				int run = abs(end->x-x);
				int rise = abs(end->y-y);
				double h = abs(run - rise); //get the excess, before using Pythagorean
				int shorter = min(rise,run); 
				h += sqrt(pow(shorter,2)*2); //apply Pythagorean theorem	
				h *= 10; //for readability
				H = h;   //truncate
			}
			F = H + G;
		}
		friend bool operator==(Point a, Point b){ return a.H == b.H;}
		friend ostream& operator<<(ostream& out, Point& p){
			out<<"  ("<<p.x<<","<<p.y<<")";
			return out;
		}
};

int obstacle[S][S] = 
   // 0 1 2 3 4 5 6	7 8 9 0 1 2 3 4 5      1 = obstacle
	{{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	 {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	 {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	 {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	 {0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},
	 {0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},
	 {0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},
	 {0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1},
	 {0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1},
	 {0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1},
	 {0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},
	 {0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},
	 {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	 {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	 {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	 {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}};
	 
Point* seen[S][S];

bool visited[S][S];

void printGrid();

bool decreasingF(Point* a, Point* b);

bool expand(Point* start, Point* end, Point* origin, vector<Point*>& to_expand);

int main(){	    
	Point* end = new Point(8,14);
	Point* origin = new Point(8,1,NULL,end);

	printGrid();
	
	vector<Point*> to_expand;
	to_expand.push_back(origin);
	
	while(!to_expand.empty()){
		sort(to_expand.begin(), to_expand.end(), decreasingF); //best Point (lowest F, lowest H) comes last
		Point* current = to_expand.back();
		to_expand.pop_back();
		if(expand(current, end, origin, to_expand))break;		
	}
	
	if(to_expand.empty())cout<<"NO PATH FOUND!"<<endl;
	printGrid();
	return 0;
}

void printGrid(){
	cout<<endl;
	for(int i=0;i<S;i++){
		cout<<"  ";
		for(int j=0;j<S;j++){
			cout<<obstacle[i][j]<<' ';
		}
		cout<<endl;
	}
	cout<<endl;
}

bool decreasingF(Point* a, Point* b){
	if(a->F == b->F) return a->H > b->H;	
	return a->F > b->F;
}

bool expand(Point* start, Point* end, Point* origin, vector<Point*>& to_expand){
	if(*start == *end){
		cout<<"TARGET REACHED. PATH TAKEN:"<<endl<<endl;
		cout<<*start<<" <---- target"<<endl;
		Point* pointparent = start;
		while(true){
			cout<<*(pointparent->Parent);
			if(pointparent->Parent == origin){
				cout<<" <---- origin"<<endl;
				break;
			}
			else{
				obstacle[pointparent->Parent->x][pointparent->Parent->y] = 9;
				cout<<endl;
				pointparent = pointparent->Parent;
			}
		}
		return true;//target point reached		
	}
	
	if(seen[start->x][start->y] == 0)seen[start->x][start->y] = start; //for start point
	visited[start->x][start->y] = 1; //mark current point as visited
	
	//evaluate surrounding points (there are 8 at max)
	//BEFORE CREATING POINT OBJECT:
	//is it inside the grid
	//is it not an obstacle
	//has it not been seen before
		//if it has been seen but is unvisited, check if origin->current->point is shorter than the point's current distance from origin (DIJKSTRA'S)
	if((start->x-1 >= 0 && start->y-1 >= 0) && (obstacle[start->x-1][start->y-1] == 0)){
		if(seen[start->x-1][start->y-1] == 0){
			Point* p1 = new Point(start->x-1,start->y-1,start,end); 
			to_expand.push_back(p1);
			seen[start->x-1][start->y-1] = p1;
		}
		else if(visited[start->x-1][start->y-1] == 0){
			//DIJKSTRA'S
			if(start->G + 14 < seen[start->x-1][start->y-1]->G){
				seen[start->x-1][start->y-1]->Parent = start;
				seen[start->x-1][start->y-1]->G = start->G + 14;
			}
		}
	}
	if((start->x-1 >= 0) && (obstacle[start->x-1][start->y] == 0)){	
		if(seen[start->x-1][start->y] == 0){ 
			Point* p2 = new Point(start->x-1,start->y,start,end); 
			to_expand.push_back(p2);
			seen[start->x-1][start->y] = p2;
		}
		else if(visited[start->x-1][start->y] == 0){
			if(start->G + 10 < seen[start->x-1][start->y]->G){
				seen[start->x-1][start->y]->Parent = start;
				seen[start->x-1][start->y]->G = start->G + 10;
			}
		}
	}
	if((start->x-1 >= 0 && start->y+1 < S) && (obstacle[start->x-1][start->y+1] == 0)){
		if(seen[start->x-1][start->y+1] == 0){ 
			Point* p3 = new Point(start->x-1,start->y+1,start,end); 
			to_expand.push_back(p3); 
			seen[start->x-1][start->y+1] = p3;
		}
		else if(visited[start->x-1][start->y+1] == 0){
			if(start->G + 14 < seen[start->x-1][start->y+1]->G){
				seen[start->x-1][start->y+1]->Parent = start;
				seen[start->x-1][start->y+1]->G = start->G + 14;
			}
		}
	}
	if((start->y-1 >= 0) && (obstacle[start->x][start->y-1] == 0)){
		if(seen[start->x][start->y-1] == 0){ 
			Point* p4 = new Point(start->x,start->y-1,start,end); 
			to_expand.push_back(p4);
			seen[start->x][start->y-1] = p4;
		}
		else if(visited[start->x][start->y-1] == 0){
			if(start->G + 10 < seen[start->x][start->y-1]->G){
				seen[start->x][start->y-1]->Parent = start;
				seen[start->x][start->y-1]->G = start->G + 10;
			}
		}
	}
	if((start->y+1 < S) && (obstacle[start->x][start->y+1] == 0)){
		if(seen[start->x][start->y+1] == 0){ 
			Point* p5 = new Point(start->x,start->y+1,start,end);
			to_expand.push_back(p5); 
			seen[start->x][start->y+1] = p5;
		}
		else if(visited[start->x][start->y+1] == 0){
			if(start->G + 10 < seen[start->x][start->y+1]->G){
				seen[start->x][start->y+1]->Parent = start;
				seen[start->x][start->y+1]->G = start->G + 10;
			}
		}	
	}
	if((start->x+1 < S && start->y-1 >= 0) && (obstacle[start->x+1][start->y-1] == 0)){
		if(seen[start->x+1][start->y-1] == 0){ 
			Point* p6 = new Point(start->x+1,start->y-1,start,end);	
			to_expand.push_back(p6); 
			seen[start->x+1][start->y-1] = p6;
		}
		else if(visited[start->x+1][start->y-1] == 0){
			if(start->G + 14 < seen[start->x+1][start->y-1]->G){
				seen[start->x+1][start->y-1]->Parent = start;
				seen[start->x+1][start->y-1]->G = start->G + 14;
			}
		}		
	}
	if((start->x+1 < S) && (obstacle[start->x+1][start->y] == 0)){
		if(seen[start->x+1][start->y] == 0){ 
			Point* p7 = new Point(start->x+1,start->y,start,end);	
			to_expand.push_back(p7); 
			seen[start->x+1][start->y] = p7;
		}
		else if(visited[start->x+1][start->y] == 0){
			if(start->G + 10 < seen[start->x+1][start->y]->G){
				seen[start->x+1][start->y]->Parent = start;
				seen[start->x+1][start->y]->G = start->G + 10;
			}				
		}
	}
	if((start->x+1 < S && start->y+1 < S) && (obstacle[start->x+1][start->y+1] == 0)){
		if(seen[start->x+1][start->y+1] == 0){ 
			Point* p8 = new Point(start->x+1,start->y+1,start,end);	
			to_expand.push_back(p8); 
			seen[start->x+1][start->y+1]  = p8;
		}
		else if(visited[start->x+1][start->y+1] == 0){
			if(start->G + 14 < seen[start->x-1][start->y]->G){
				seen[start->x+1][start->y+1]->Parent = start;
				seen[start->x+1][start->y+1]->G = start->G + 14;
			}
		}			
	}
	return false;
}
