
package binarytreesort;

public class Node {
    private int data;
    Node leftChild;
    Node rightChild;
    
    public Node(int d){
        data = d;
        leftChild = null;
        rightChild = null;
    }
    
    int getData(){return data;}
    void printData(){System.out.print(data + " ");}  
    
}
