
package quicksort;

import java.util.Arrays;

public class Quicksort {
    public static void main(String[] args) {
        int[] arr = {2,3,5,7,4,54,68,6,2,5};
        System.out.printf("Before: " + Arrays.toString(arr) +"\n");
        Sorter.quickSort(arr,0,9);
        System.out.printf("After: " + Arrays.toString(arr) +"\n");
    }
}
