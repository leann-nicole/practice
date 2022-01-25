#include <iostream>
using namespace std;
// this program creates a binary search tree

class Node{

	int data;
	Node* left;
	Node* right;
	public:
		Node(int data):data(data){
			left = NULL;
			right = NULL;
		}
		int getData(){
			return data;
		}	
		void printData(){
			cout<<data<<' ';
		}
	friend void addToTree(Node* root, Node *newNode);
	friend void traverseTree(Node* node);
};

void addToTree(Node* root, Node *newNode){
	Node* nodeToCompare = root;
	Node* parent;
	while(true){
		parent = nodeToCompare;
		if(newNode->getData() <= nodeToCompare->getData()){
			if(nodeToCompare->left == NULL){
				parent->left = newNode;
				break;
			}
			nodeToCompare = nodeToCompare->left;
		}
		else{
			if(nodeToCompare->right == NULL){
				parent->right = newNode;
				break;
			}
			nodeToCompare = nodeToCompare->right;
		}
	}
}

void traverseTree(Node* node){ //in-order traversal (left, root, right)
	if(node != NULL){
		traverseTree(node->left);
		node->printData();
		traverseTree(node->right);	
	}
}

int main(){
	Node newnode = new Node(2);
	Node nodes_array[] = {5,3,5,2,5,6,3,5,7,8,8,0};
	for(int i=1; i<int(sizeof(nodes_array)/sizeof(Node)); i++){
		addToTree(&nodes_array[0],&nodes_array[i]);
	}
	traverseTree(&nodes_array[0]);
	return 0;
}
