#include <iostream>
using namespace std;

class Node
{
public:
    int val, col, count;
    Node *left, *right, *parent;
    Node(int n)
    {
        val = n;
        col = 1;
        count = 1;
        left = NULL;
        right = NULL;
        parent = NULL;
    }
};

class RBT
{
public:
    Node *root = NULL;
    RBT() {}
    void printTree(Node *root, string indent, bool right)
    {
        if (root != NULL)
        {
            cout << indent;
            if (right)
            {
                cout << "R----";
                indent += "     ";
            }
            else
            {
                cout << "L----";
                indent += "|    ";
            }
            string sColor = (root->col) ? "RED" : "BLACK";
            cout << root->val << "(" << sColor << ") x " << root->count << endl;
            printTree(root->left, indent, false);
            printTree(root->right, indent, true);
        }
    }

    void leftRotate(Node *node)
    {
        Node *newPar = node->right;

        node->right = newPar->left;
        if (newPar->left != NULL)
        {
            newPar->left->parent = node;
        }
        newPar->parent = node->parent;
        if (newPar->parent == NULL)
            root = newPar;
        else if (node == node->parent->left)
            node->parent->left = newPar;
        else
            node->parent->right = newPar;

        newPar->left = node;
        node->parent = newPar;
    }

    void rightRotate(Node *node)
    {
        Node *newPar = node->left;

        node->left = newPar->right;
        if (newPar->right != NULL)
        {
            newPar->right->parent = node;
        }
        newPar->parent = node->parent;
        if (newPar->parent == NULL)
            root = newPar;
        else if (node == node->parent->right)
            node->parent->right = newPar;
        else
            node->parent->left = newPar;

        newPar->right = node;
        node->parent = newPar;
    }

    void fixInsert(Node *kid)
    {
        Node *uncle;
        if (kid->parent == NULL)
            cout << "What?" << endl;
        while (kid->parent->col)
        {
            if (kid->parent == kid->parent->parent->left)
            { // parent is left node
                uncle = kid->parent->parent->right;
                if (uncle == NULL || uncle->col == 0)
                {
                    if (kid == kid->parent->right)
                    {
                        kid = kid->parent;
                        leftRotate(kid);
                    }
                    kid->parent->col = 0;
                    kid->parent->parent->col = 1;
                    rightRotate(kid->parent->parent);
                }
                else
                {
                    uncle->col = 0;
                    kid->parent->col = 0;
                    kid->parent->parent->col = 1;
                    kid = kid->parent->parent;
                }
            }
            else
            {
                uncle = kid->parent->parent->left;
                if (uncle == NULL || uncle->col == 0)
                {
                    if (kid == kid->parent->left)
                    {
                        kid = kid->parent;
                        rightRotate(kid);
                    }
                    kid->parent->col = 0;
                    kid->parent->parent->col = 1;
                    leftRotate(kid->parent->parent);
                }
                else
                {
                    uncle->col = 0;
                    kid->parent->col = 0;
                    kid->parent->parent->col = 1;
                    kid = kid->parent->parent;
                }
            }
            if (kid->parent == NULL)
                break;
        }
        root->col = 0;
    }
    void insertNode(int n)
    {
        Node *kid = new Node(n);
        if (root == NULL)
            root = kid;
        else
        {
            Node *backup = NULL;
            Node *lead = root;
            while (lead != NULL)
            {
                backup = lead;
                if (n < lead->val)
                    lead = lead->left;
                else if (n > lead->val)
                    lead = lead->right;
                else
                {
                    lead->count++;
                    return;
                }
            }
            kid->parent = backup;
            if (n < backup->val)
                backup->left = kid;
            else
                backup->right = kid;
        }
        if (kid->parent == NULL)
        {
            kid->col = 0;
            return;
        }
        if (kid->parent->parent == NULL)
        {
            return;
        }
        fixInsert(kid);
    }
};

int main()
{
    RBT rbt;
    rbt.insertNode(8);
    rbt.insertNode(18);
    rbt.insertNode(5);
    rbt.insertNode(15);
    rbt.insertNode(17);
    rbt.insertNode(25);
    rbt.insertNode(40);
    rbt.insertNode(80);

    rbt.printTree(rbt.root, "", true);
    return 0;
}