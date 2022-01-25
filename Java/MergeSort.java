package MergeSortPackage;

import java.util.Arrays;

public class MergeSort {
    private static int[] merge(int[] arr1, int[] arr2){
        int[] newArray = new int[arr1.length+arr2.length];                      //create new array, size = arr1.length + arr2.length
        int arr1index = 0, arr2index = 0;                                       //values for traversing the 2 arrays for comparison
        for(int i=0;i<newArray.length;i++){                                     //assigning values to each index in the new array
            if(arr1index==arr1.length) newArray[i] = arr2[arr2index++];         //if one of the 2 arrays is completely evaluated
            else if(arr2index==arr2.length) newArray[i] = arr1[arr1index++];
            else if(arr1[arr1index]<arr2[arr2index]) newArray[i] = arr1[arr1index++]; //else, compare values
            else newArray[i] = arr2[arr2index++];
        }
        return newArray;
    }
    private static int[] split(int[] arr){
        if(arr.length == 1)return arr;                                 //base case
        int split_index = (arr.length)/2;                              //find index where the array should be halved
        int[] arr1 = split(Arrays.copyOfRange(arr, 0, split_index));
        int[] arr2 = split(Arrays.copyOfRange(arr, split_index, arr.length));
        return merge(arr1, arr2);                                      //merge the arrays, each of them sorted by now
    }
    public static void main(String[] args){
        int[] arr = {22,0,3,5,7,-1,49,54,68,6,2,5};
        System.out.printf("BEFORE QUICKSORT:\n" + Arrays.toString(arr) + "\n");
        System.out.printf("AFTER QUICKSORT:\n" + Arrays.toString(split(arr))); 
    }
}