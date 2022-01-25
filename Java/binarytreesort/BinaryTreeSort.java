
package binarytreesort;

import java.util.ArrayList;

public class BinaryTreeSort {
    static void addToTree(Node root, Node node){
        Node stepper = root;
        Node parent;
        while(true){
            parent = stepper;
            if(node.getData() >= stepper.getData()){
                if(stepper.rightChild == null){
                    parent.rightChild = node;
                    break;
                }
                stepper = stepper.rightChild;
            }
            else{
                if(stepper.leftChild == null){
                    parent.leftChild = node;
                    break;
                }
                stepper = stepper.leftChild;
            }
        }
    }
    
    static void traverseTree(Node root){
        if(root != null){
            traverseTree(root.leftChild);
            root.printData();
            traverseTree(root.rightChild);
        }
    }
    public static void main(String[] args) {
        Node root = new Node(2); 
        ArrayList<Node> listOfNodes = new ArrayList<>();
        listOfNodes.add(new Node(3));
        listOfNodes.add(new Node(1));
        listOfNodes.add(new Node(0));
        listOfNodes.add(new Node(0));
        listOfNodes.add(new Node(4));
        listOfNodes.add(new Node(12));
        listOfNodes.add(new Node(9));
        
        for(Node node: listOfNodes){
            addToTree(root,node);
        }
   
        traverseTree(root);
    }
}
