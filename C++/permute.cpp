#include <iostream>
using namespace std;

void swap(string& str, int i1, int i2){
	char c1 = str[i1];
	str[i1] = str[i2];
	str[i2] = c1;
}

void permute(string str, int start, int end){
	if(start == end)cout<<str<<endl;
	else{
		for(int i = start; i <= end; i++){
			swap(str, start, i);
			permute(str, start+1, end);
		}
	}
}


int main(){
	string String = "ABC";
	permute(String, 0, String.length()-1);
	return 0;
}
