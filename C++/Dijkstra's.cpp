#include <iostream>
#include <array>
#include <climits>
#include <iomanip>
#define V 9
using namespace std;
//a program to implement Dijkstra's algorithm (shortest path)

void addVertex(int graph[V][V], array<int,V>& MST, array<int,V>& SV_distance, array<int,V>& parent);
bool notAllPartOf(array<int,V>& MST);
void printGraph(int graph[V][V]);

int main(){
	
	int graph[V][V] =  
	 //  0 1 2 3 4 5 6 7 8	
		{{0,4,0,0,0,0,0,8,0},
		{4,0,8,0,0,0,0,11,0},
		{0,8,0,7,0,4,0,0,2},
		{0,0,7,0,9,14,0,0,0},
		{0,0,0,9,0,10,0,0,0},
		{0,0,4,14,10,0,2,0,0},
		{0,0,0,0,0,2,0,1,6},
		{8,11,0,0,0,0,1,0,7},
		{0,0,2,0,0,0,6,7,0}};
	cout<<setw(25)<<"THE GRAPH\n\n";
	printGraph(graph);

	array<int,V> MST; 
	MST.fill(0);
	MST[0] = 1;	//starting vertex is vertex 0, the first member of the MST

	array<int,V> parent;
	parent.fill(0);

	array<int,V> SV_distance;
	SV_distance.fill(INT_MAX);
	SV_distance[0] = 0; //distance of starting vertex to itself is 0

	//find next vertex to add to MST while not all have been added
	while(notAllPartOf(MST))addVertex(graph, MST, SV_distance, parent); 
	
	
	cout<<endl<<"    VERTEX     DISTANCE     SOURCE\n";
	for(int i=0;i<V;i++){
		cout<<setw(8)<<i<<setw(12)<<SV_distance[i]<<setw(14)<<parent[i]<<endl;
	}
	
	return 0;
}

void printGraph(int graph[V][V]){
	for(int i=0; i<V; i++){
		for(int j=0; j<V; j++){
			cout<<setw(4)<<graph[i][j];
		}
		cout<<endl<<endl;
	}
}

bool notAllPartOf(array<int,V>& MST){
	for(int i: MST)if(i == 0)return true;
	return false;
}

void addVertex(int graph[V][V], array<int,V>& MST, array<int,V>& SV_distance, array<int,V>& parent){
	//traverse the MST
	//for each vertex in MST, look for adjacent vertices not yet part of the MST
	//if distance to a vertex is less than the current recorded distance, make changes
	
	for(int vertex=0; vertex<int(MST.size()); vertex++){
		if(MST[vertex] != 0){ //meaning this vertex is part of the MST
			for(int a=0; a<V; a++){ //check it's adjacents
				if(graph[vertex][a] != 0 && MST[a] == 0){ //if adjacent is not part of the MST yet
					if((SV_distance[vertex] + graph[vertex][a]) < SV_distance[a]){ //if shorter path
						SV_distance[a] = SV_distance[vertex] + graph[vertex][a]; //update 
						parent[a] = vertex; //update
					}
				}
			}
		}
	}
	
	//add vertex not part of MST and with lowest SV_distance
	int closest;
	int smallest = INT_MAX;
	for(int i=0;i<int(SV_distance.size());i++){
		if(SV_distance[i] < smallest && MST[i] == 0){
			smallest = SV_distance[i];
			closest = i;
		}
	}
	MST[closest] = 1;
}
