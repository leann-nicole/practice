#include <bits/stdc++.h>
using namespace std;

class Node
{
public:
    int value;
    int count;
    int height;
    Node *lChild;
    Node *rChild;
    Node(int n)
    {
        value = n;
        count = 1;
        lChild = NULL;
        rChild = NULL;
        height = 0;
    }
};

int getHeight(Node *root)
{
    if (root == NULL)
        return 0;
    return 1 + max(getHeight(root->lChild), getHeight(root->rChild));
}

Node *leftRotate(Node *root)
{
    Node *newRoot = root->rChild;
    newRoot->lChild = root;
    root->rChild = newRoot->lChild;

    root->height = getHeight(root);
    newRoot->height = getHeight(newRoot);

    return newRoot;
}

Node *rightRotate(Node *root)
{
    Node *newRoot = root->lChild;
    newRoot->rChild = root;
    root->lChild = newRoot->rChild;

    root->height = getHeight(root);
    newRoot->height = getHeight(newRoot);

    return newRoot;
}

int height(Node *node)
{
    if (node == NULL)
        return 0;
    return node->height;
}

int balFactor(Node *root)
{
    return getHeight(root->lChild) - getHeight(root->rChild);
}

void traverseInOrder(Node *root)
{
    if (root != NULL)
    {
        traverseInOrder(root->lChild);
        cout << root->value << endl;
        traverseInOrder(root->rChild);
    }
}

Node *insertNode(Node *root, int value) // returns the new root node
{
    // normal BST insertion
    if (root == NULL) // base case
        return new Node(value);
    if (value < root->value)
        root->lChild = insertNode(root->lChild, value);
    else if (value > root->value)
        root->rChild = insertNode(root->rChild, value);
    else if (value == root->value)
    {
        root->count++; // similar values are not stored separately in self-balancing trees, imagine trying to balance 3 nodes of similar values, i guess it's what caused a segmentation fault
        return root;
    }

    //update root height since node was inserted
    root->height = getHeight(root);

    //balancing
    int heightDiff = balFactor(root);
    // if heigDiff is 0 or 1, tree is balanced so return old root, else:
    if (heightDiff > 1 and value < root->lChild->value)
    {
        return rightRotate(root); // rotations work their way to the top
    }
    else if (heightDiff > 1 and value > root->lChild->value)
    {
        root->lChild = leftRotate(root);
        return rightRotate(root);
    }
    else if (heightDiff < -1 and value > root->rChild->value)
    {
        return leftRotate(root);
    }
    else if (heightDiff < -1 and value < root->rChild->value)
    {
        root->rChild = rightRotate(root);
        return leftRotate(root);
    }

    return root;
}

int main()
{
    Node *root = new Node(10);
    root = insertNode(root, 9);
    root = insertNode(root, 11);
    root = insertNode(root, 3);
    root = insertNode(root, 3);
    root = insertNode(root, 3);
    root = insertNode(root, 12);
    traverseInOrder(root);           // In-Order BST traversal present elements in sorted manner
    cout << balFactor(root) << endl; // we can see that the tree is balanced
    return 0;
}