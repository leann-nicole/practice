// this program implements Kruskal's algorithm for finding the MST
//note to self: don't return references to a local variable. 
//memory inside a function gets deallocated when execution flow goes out of that function. your pointer now points to garbage
#include <iostream>
#include <array>
#include <vector>
#include <algorithm>
#define V 5
using namespace std;

class Edge{
	
	public: 
	int weight;
	int source;
	int dest;
	
	public:
	
		Edge(int w, int s, int d): weight(w), source(s), dest(d){}
		void printEdge(){
			cout<<"   "<<char(source+65)<<"      "<<char(dest+65)<<"        "<<weight<<endl;
		}
	
};

bool byWeight(Edge a, Edge b);
vector<Edge> createEdgeObj(int graph[V][V]);
bool noCycleCreated(Edge e, array<int,V>& parent);
vector<Edge> buildMST(vector<Edge> edgelist, array<int,V>& parent, int& total);

int main(){
	//the graph
	int graph[V][V] = {
	  // a b c d e 
		{0,2,3,0,0},		
		{2,0,1,3,2},
		{3,1,0,0,1},
		{0,3,0,0,5},
		{0,2,1,5,0}
		};
	int total = 0; // MST Cost
	
	array<int,V> parent;  // index is the node, value at index is the parent
	parent.fill(-1);
	
	vector<Edge> edgeList = createEdgeObj(graph); //returns all edges in graph, sorted by increasing weight
	
	vector<Edge> MST_Edges = buildMST(edgeList, parent, total); //returns only the edges that are part of the MST
	//print the MST and MST cost
	cout<<" source  dest    weight\n";
	for(Edge e: MST_Edges){
		e.printEdge();
	}
	cout<<"\n     MST Cost = "<<total<<endl;
	return 0;
}

bool byWeight(Edge a, Edge b){
	return a.weight < b.weight;
}

vector<Edge> createEdgeObj(int graph[V][V]){
	vector<Edge> edgeList;
	for(int row=0; row<V; row++){
		for(int col=0; col<V; col++){
			if(row < col && graph[row][col]!=0){
				Edge edge(graph[row][col], row, col);
				edgeList.push_back(edge);
			}
		}
	}
	//sort before returning
	sort(edgeList.begin(), edgeList.end(), byWeight);
	return edgeList;
}

bool noCycleCreated(Edge e, array<int,V>& parent){
	int index = e.source;
	while(parent[index] != -1){
		if(parent[index] == e.dest)return false;
		index = parent[index];
	}
	return true;
}

vector<Edge> buildMST(vector<Edge> edgeList, array<int,V>& parent, int& total){
	int added=0; //counts # of nodes added to MST
	vector<Edge> MST_Edges; //edges part of the MST

	for(int i=0; i<int(edgeList.size()); i++){
		if(noCycleCreated(edgeList[i], parent) && added!=V-1){ //if the edge doesn't create a cycle and not all nodes have been added to the MST
			parent[edgeList[i].source] = edgeList[i].dest;
			MST_Edges.push_back(edgeList[i]);
			added++;
			total += edgeList[i].weight;
		}
	}
	return MST_Edges;
}
