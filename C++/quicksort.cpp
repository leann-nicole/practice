#include <iostream>
using namespace std;
void swap(int* a, int* b);
int partition(int arr[], int left, int right);
void quicksort(int arr[], int start, int end);

int main(){
	int arr[10] = {6,9,5,8,3,2,10,0,7,4};
	cout<<"Before: ";
	for(int i=0;i<10;i++)cout<<arr[i]<<" ";
	cout<<endl;
	quicksort(arr,0,9);
	cout<<"After: ";
	for(int i=0;i<10;i++)cout<<arr[i]<<" ";
	cout<<endl;
	return 0;
}

void swap(int* a, int* b){
	int temp = *a;
	*a = *b;
	*b = temp;
}
int partition(int arr[], int left, int right){
	int pivot_index = left;
	int pivot = arr[left];
	left++;
	while(left<right){
		if((arr[left]>pivot)&&arr[right]<pivot){
			swap(&arr[left++],&arr[right--]);
		}
		else if(arr[left]>pivot)right--;
		else if(arr[right]<pivot)left++;
		else{
			left++; right--;
		}
	}
	if(pivot>=arr[left]){
		swap(&arr[pivot_index],&arr[left]);
		pivot_index = left;
	}
	else{
		swap(&arr[pivot_index],&arr[left-1]);
		pivot_index = left -1;
	}
	return pivot_index;
}
void quicksort(int arr[], int start, int end){
	if(start<end){
		int pivot = partition(arr, start, end);
		quicksort(arr, start, pivot-1);
		quicksort(arr, pivot+1, end);
	}
}
