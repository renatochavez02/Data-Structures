from __future__ import annotations
import json
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

class SplayForest():
    def  __init__(self,
                  roots : None):
        self.roots = roots

    def newtree(self,treename):
        self.roots[treename] = None

    # For the tree rooted at root:
    # Return the json.dumps of the object with indent=2.
    # DO NOT MODIFY!!!
    def dump(self):
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "right": (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parentkey": pk
            }
        if self.roots == None:
            dict_repr = {}
        else:
            dict_repr = {}
            for t in self.roots:
                if self.roots[t] is not None:
                    dict_repr[t] = _to_dict(self.roots[t])
        print(json.dumps(dict_repr,indent = 2))

    # This helper method calls splay on a node, bringing it to the root after a series of operations
    def splay(self, node: Node, root: Node = None):
        # If we pass in a root, it is because we are calling splay on a value using the subtree as a root
        if root is not None:
            # Iterate until we took the splayed node to the root or to the right subtree
            while node.parent is not None and node != root.rightchild:
                parent = node.parent
                grandparent = parent.parent

                # Zig opeartion could happen if we are at a root's child considering the root can be a subtree
                if grandparent is None or parent.parent.parent is None:
                    # Perform a right rotation if the node is the root's left child
                    if node == parent.leftchild:
                        self.right_rotate(parent)
                    # Perform a left rotation if the node is the root's right child
                    else:
                        self.left_rotate(parent)

                # Zig-Zig or Zig-Zag operations
                else:
                    # Zig-Zig operations
                    if node == parent.leftchild and parent == grandparent.leftchild:
                        self.right_rotate(grandparent)
                        self.right_rotate(parent)
                    elif node == parent.rightchild and parent == grandparent.rightchild:
                        self.left_rotate(grandparent)
                        self.left_rotate(parent)
                    # Zig-Zag operations
                    elif node == parent.rightchild and parent == grandparent.leftchild:
                        self.left_rotate(parent)
                        self.right_rotate(grandparent)
                    else:
                        self.right_rotate(parent)
                        self.left_rotate(grandparent)
        else:
            # Check if the node is finally at the root, if it is not proceed with the correct operation
            while node.parent is not None:
                # Define who is the parent and who is the grandparent
                parent = node.parent
                grandparent = parent.parent

                # Zig opeartion
                if grandparent is None:
                    # Perform a right rotation if the node is the root's left child
                    if node == parent.leftchild:
                        self.right_rotate(parent)
                    # Perform a left rotation if the node is the root's right child
                    else:
                        self.left_rotate(parent)

                # Zig-Zig or Zig-Zag operations
                else:
                    # Zig-Zig operations
                    if node == parent.leftchild and parent == grandparent.leftchild:
                        self.right_rotate(grandparent)
                        self.right_rotate(parent)
                    elif node == parent.rightchild and parent == grandparent.rightchild:
                        self.left_rotate(grandparent)
                        self.left_rotate(parent)
                    # Zig-Zag operations
                    elif node == parent.rightchild and parent == grandparent.leftchild:
                        self.left_rotate(parent)
                        self.right_rotate(grandparent)
                    else:
                        self.right_rotate(parent)
                        self.left_rotate(grandparent)

    # This helper method performs a right rotation at the given node
    def right_rotate(self, node: Node):
        # Define who is the left child and check if it is empty
        left_child = node.leftchild
        if left_child is None:
            return
        # Adjust the left child's right subtree to be the node's left subtree
        node.leftchild = left_child.rightchild
        # If there is a left child's right subtree, update the parent to be the node
        if left_child.rightchild is not None:
            left_child.rightchild.parent = node
        # Update the left child's parent to be what was the node's parent since it will be taking its place
        left_child.parent = node.parent

        # If the given node was the root, set the left child as the new root in the list of trees
        if node.parent is None:
            for treename, root in self.roots.items():
                if root == node:
                    self.roots[treename] = left_child
        # Otherwise update the child reference of the node's parent to be the left child since it took its place
        elif node == node.parent.leftchild:
            node.parent.leftchild = left_child
        else:
            node.parent.rightchild = left_child
        # Set the left child's right subtree to be the node, and update the node's parent to be the left child
        left_child.rightchild = node
        node.parent = left_child

    # This method performs a left rotation, and it works symetrically compared to the right rotation
    def left_rotate(self, node: Node):
        right_child = node.rightchild
        if right_child is None:
            return
        
        node.rightchild = right_child.leftchild

        if right_child.leftchild is not None:
            right_child.leftchild.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            for treename, root in self.roots.items():
                if root == node:
                    self.roots[treename] = right_child
        elif node == node.parent.leftchild:
            node.parent.leftchild = right_child
        else:
            node.parent.rightchild = right_child

        right_child.leftchild = node
        node.parent = right_child

    # This helper method helps us find the nearest node to the key we are attempting to insert
    # It finds the node where we'd fall out of the tree if we were to insert the key.
    def find_nearest(self, node: Node, key: int) -> Node:
        while True:
            if key < node.key:
                if node.leftchild is None:
                    return node
                node = node.leftchild
            else:
                if node.rightchild is None:
                    return node
                node = node.rightchild

    # This method will help us find a node in a tree based on a given key
    def find_node_or_iop_ios(self, key: int, treename: str = "", root = None) -> Node:
        iop_ios = None
        # If we pass in a root, then we are finding the ios
        if root is not None:
            node = root
            # Iterate until we can return the ios
            while node is not None:
                iop_ios = node
                if key < node.key and node.leftchild is not None:
                    node = node.leftchild
                elif key > node.key and node.rightchild is not None:
                    node = node.rightchild
                else:
                    return iop_ios
        # If we do not have the root, then there is a chance we might actually find the key in the tree
        else:
            node = self.roots[treename]
            while node is not None:
                iop_ios = node
                if key < node.key:
                    node = node.leftchild
                elif key > node.key:
                    node = node.rightchild
                else:
                    return node
        
        return iop_ios


    # Search:
    # Search for the key or the last node before we fall out of the tree.
    # Splay that node.
    def search(self,treename: str,key:int):
        node = self.find_node_or_iop_ios(key, treename=treename)
        self.splay(node)

    # Insert Type 1:
    # The key is guaranteed to not be in the tree.
    # Call splay(x) and respond according to whether we get the IOP or IOS.
    def insert(self,treename:str,key:int):
        # Set our root equal to the corresponding one based on the treename argument
        root = self.roots[treename]
        # If the tree is empty, simply set the root equal to a node with the key that was passed
        if root is None:
            self.roots[treename] = Node(key)
            return
        
        # Search for the nearest node to the key we are trying to insert
        # In other words, the node where we fall out of the tree when we try to insert the key
        nearest = self.find_nearest(root, key)
        # Call splay on the nearest node which will be either the iop or ios
        self.splay(nearest)
        # Figure out if it is the ios or ios and adjust the subtrees accordingly
        if nearest.key < key:
            new_root = Node(
                key, 
                leftchild=nearest, 
                rightchild=nearest.rightchild)
            nearest.rightchild = None
        else:
            new_root = Node(
                key, 
                leftchild=nearest.leftchild, 
                rightchild=nearest)
            nearest.leftchild = None

        # Update the subtrees' parent which will be the new root
        if new_root.leftchild is not None:
            new_root.leftchild.parent = new_root
        if new_root.rightchild is not None:
            new_root.rightchild.parent = new_root
        # Update the root corresponding to the treename in the trees list
        self.roots[treename] = new_root

    # Delete Type 1:
    # The key is guarenteed to be in the tree.
    # Call splay(key) and then respond accordingly.
    # If key (now at the root) has two subtrees call splay(key) on the right one.
    def delete(self,treename:str,key:int):
        # Save the node we want to delete in a variable
        node_to_delete = self.find_node_or_iop_ios(key, treename=treename)
        # If the node we want to delete is the only node in the tree (the root) then simply delete it
        if node_to_delete.leftchild is None and node_to_delete.rightchild is None and node_to_delete.parent is None:
            self.roots[treename] = None
            return

        # Call splay on the node we want to delete
        self.splay(node_to_delete)
        # Set L and R as our left and right subtrees
        left_subtree = node_to_delete.leftchild
        right_subtree = node_to_delete.rightchild
        # If the left subtree is empty, we simply set the right subtree as the new tree
        if left_subtree is None:
            self.roots[treename] = right_subtree
            right_subtree.parent = None
        # Symetrically, do the same if the right subtree is empty
        elif right_subtree is None:
            self.roots[treename] = left_subtree
            left_subtree.parent = None
        # If none of the subtrees are empty
        else:
            # Find in order successor of the node we want to delete in the right subtree
            node_to_delete_ios = self.find_node_or_iop_ios(key, root=right_subtree)
            # Call splay on the original node we wanted to delete, but using the right subtree as the root
            self.splay(node_to_delete_ios, node_to_delete)
            # The new root will be the root of the right subtree now, since we now have the in order successor at the root
            new_root = node_to_delete.rightchild
            self.roots[treename] = new_root
            new_root.parent = None
            # Attach the left subtree to the new root
            new_root.leftchild = left_subtree
            left_subtree.parent = new_root
        