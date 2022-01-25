#include <iostream>
using namespace std;

void swap(int* a, int* b){
	int temp = *a;
	*a = *b;
	*b = temp;
}

void heapsort(int arr[], int last){

	if(!last)return;
	
	int curr = last;
	if(curr%2 != 0){
		if(arr[curr] > arr[(curr-1)/2]){
			swap(&arr[curr],&arr[(curr-1)/2]);
		}
		curr--;
	}
	while(curr != 0){
		if(arr[curr] > arr[(curr-2)/2]){
			swap(&arr[curr],&arr[(curr-1)/2]);
		}
		if(!--curr)break;
		if(arr[curr] > arr[(curr-1)/2]){
			swap(&arr[curr],&arr[(curr-2)/2]);
		}
		if(!--curr)break;
	}
	swap(&arr[0],&arr[last]);
	heapsort(arr, --last);
}

int main(){
	int arr[11] = {2,1,5,5,6,3,1,0,7,6,0};
	heapsort(arr,10);
	for(int i: arr)cout<<i<<' ';
	return 0;
}
