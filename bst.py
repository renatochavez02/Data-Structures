# BST Variation 2

from __future__ import annotations
import json

# The class for a particular node in the tree.
# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key        : int  = None,
                  value      : int  = None,
                  leftchild  : Node = None,
                  rightchild : Node = None):
        self.key        = key
        self.value      = value
        self.leftchild  = leftchild
        self.rightchild = rightchild

# For the tree rooted at root:
# Return the json.dumps of the list with indent=2.
# DO NOT MODIFY!
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key"        : node.key,
            "value"      : node.value,
            "leftchild"  : (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "rightchild" : (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)

# Helper function to find the rightmost child of a BST
def find_rightmost(root: Node) -> Node:
    if root is None:
        return root
    
    if root.rightchild is None:
        return root
    else:
        return find_rightmost(root.rightchild)
    
# Helper function to find the leftmost child of a BST
def find_leftmost(root: Node) -> Node:
    if root is None:
        return root
    
    if root.leftchild is None:
        return root
    else:
        return find_leftmost(root.leftchild)
    
# Helper function to count the nodes of a BST
def count_nodes(root: Node) -> int:
    if root is None:
        return 0
    return 1 + count_nodes(root.leftchild) + count_nodes(root.rightchild)

# Helper functions to find the inorder predecessor and successor
def find_inorder_predecessor(root: Node) -> Node:
    if root is None:
        return None
    
    curr = root
    while curr.rightchild is not None:
        curr = curr.rightchild

    return curr

def find_inorder_successor(root: Node) -> Node:
    if root is None:
        return None
    
    curr = root
    while curr.leftchild is not None:
        curr = curr.leftchild

    return curr


# For the tree rooted at root and the key and value given:
# Insert the key/value pair.
# The key is guaranteed to not be in the tree.
# Follow the variation rules as per the PDF.
def insert(root: Node, key: int, value: int) -> Node:
    # If the tree is empty, create a new tree with the given node
    if root is None:
        return Node(key = key, value = value)
    else:
        # Define the largest value of the left subtree and the smallest value of the right subtree
        lchild_rightmost_child = find_rightmost(root.leftchild)
        rchild_leftmost_child = find_leftmost(root.rightchild)

        # If the given key can replace the root, replace it
        if (lchild_rightmost_child is None or lchild_rightmost_child.key < key) and (rchild_leftmost_child is None or rchild_leftmost_child.key > key):
            # Save the values of the original root
            prev_key = root.key
            prev_value = root.value
            root.key = key
            root.value = value

            # Insert the original root in one of the two subtrees depending on its value
            if prev_key < key:
                root.leftchild = insert(root.leftchild, prev_key, prev_value)
            else:
                root.rightchild = insert(root.rightchild, prev_key, prev_value)
        else:
            # If the given key cannot replace the root, find what node in the BST it fits best.
            if key < root.key:
                root.leftchild = insert(root.leftchild, key, value)
            else:
                root.rightchild = insert(root.rightchild, key, value)

    return root

# For the tree rooted at root and the key given, delete the key.
# Follow the variation rules as per the PDF.
def delete(root: Node, key: int) -> Node:
    # Locate the node with the key we are trying to delete
    if key < root.key:
        root.leftchild = delete(root.leftchild, key)
    elif key > root.key:
        root.rightchild = delete(root.rightchild, key)
    else:
        # When the node with the key is found

        # Check if we need to find a replacement
        if root.leftchild is None:
            return root.rightchild
        elif root.rightchild is None:
            return root.leftchild
        
        # If we need to find a replacement, follow the rules of the PDF

        # Check which subtree has more nodes and replace accordingly
        left_subtree_nodes = count_nodes(root.leftchild)
        right_subtree_nodes = count_nodes(root.rightchild)
        
        if left_subtree_nodes > right_subtree_nodes:
            pred = find_inorder_predecessor(root.leftchild)
            root.key = pred.key
            root.value = pred.value
            root.leftchild = delete(root.leftchild, pred.key)
        else:
            succ = find_inorder_successor(root.rightchild)
            root.key = succ.key
            root.value = succ.value
            root.rightchild = delete(root.rightchild, succ.key)


    return root

# For the tree rooted at root and the key given:
# Calculate the list of values on the path from the root down to and including the search key node.
# The key is guaranteed to be in the tree.
# Return the json.dumps of the list with indent=2.
def search(root: Node, search_key: int) -> str:
    value_list = []
    curr_node = root

    # Iterate until we find the key
    while curr_node is not None:
        # Add the current value to our value list
        value_list.append(curr_node.value)
        if curr_node.key == search_key:
            break
        elif search_key < curr_node.key:
            curr_node = curr_node.leftchild
        else:
            curr_node = curr_node.rightchild
    
    return json.dumps(value_list,indent = 2)