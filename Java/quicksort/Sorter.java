
package quicksort;

public class Sorter {
    private static int partition(int[] arr, int left, int right){
        int pivot = arr[left];
        int pivot_index = left;
        left++;
        while(left<right){
            if(arr[left]>pivot&&arr[right]<pivot){
                int temp = arr[left];
                arr[left] = arr[right];
                arr[right] = temp;
                left++;
                right--;
            }
            else if(arr[left]>pivot)right--;
            else if(arr[right]<pivot)left++;
            else{
                left++;
                right--;
            }
        }
        if(pivot>arr[left]){
            int temp = arr[left];
            arr[left] = pivot;
            arr[pivot_index] = temp;
            pivot_index = left;
        }
        else{
            int temp = arr[left-1];
            arr[left-1] = pivot;
            arr[pivot_index] = temp;
            pivot_index = left-1;
        }
        return pivot_index;
    }
    static void quickSort(int[] arr, int start, int end){
        if(start<end){
            int pivot = partition(arr, start, end);
            quickSort(arr, start, pivot-1);
            quickSort(arr, pivot+1, end);
        }
    }
    
}
