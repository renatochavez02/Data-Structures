from __future__ import annotations
import json
import math
from typing import List

# Node Class.
# You may make minor modifications.
class Node():
    def  __init__(self,
                  keys     : List[int] = None,
                  children : List[Node] = None,
                  parent   : Node = None):
        self.keys     = keys
        self.children = children
        self.parent   = parent

# DO NOT MODIFY THIS CLASS DEFINITION.
class Btree():
    def  __init__(self,
                  m    : int  = None,
                  root : Node = None):
        self.m    = m
        self.root = None

    # DO NOT MODIFY THIS CLASS METHOD.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            return {
                "k": node.keys,
                "c": [(_to_dict(child) if child is not None else None) for child in node.children]
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)
    

    # This method will find the node where a key should be inserted
    def find_node(self, node: Node, key: int) -> Node:
        # If we are on a leaf, return the node
        if not any(node.children):
            return node
        # Traverse the tree looking for the correct node
        for i, child_key in enumerate(node.keys):
            if key == child_key:
                return node
            elif key < child_key:
                    return self.find_node(node.children[i], key)
        # Add the case where the key we want to insert is the greatest value
        return self.find_node(node.children[-1], key)
    
    # This method inserts the key in the correct node, then checks if it is overfull and handles it accordingly
    def insert_key(self, node: Node, key: int):
        # Insert the key in the given node, then sort the keys
        node.keys.append(key)
        node.keys.sort()
        # Ensure that the number of children of the node is 1 + number of keys
        while len(node.children) < len(node.keys) + 1:
            node.children.append(None)

        # Check if the node is overfull
        if len(node.keys) > self.m - 1:
            # Check if a left sibling has room, if so, do left rotations as needed
            if self.left_sibling_has_room(node):
                self.left_rotation(node)
            # Check if a right sibling has room, if so, do right rotations as needed
            elif self.right_sibling_has_room(node):
                self.right_rotation(node)
            # If no sibling has room, do a split and promote
            else:
                self.split_node(node)

    # This method checks if any left sibling has room for one more key and not be overfull
    def left_sibling_has_room(self, node: Node) -> bool:
        # Check if we are in the root node
        parent = node.parent
        if parent is None:
            return False
        # Start from the left sibling of the given node and keep moving left as needed
        index = parent.children.index(node)
        for i in range(index - 1, -1, -1):
            if index > 0:
                left_sibling = parent.children[i]
                # Check if the left sibling has space
                if len(left_sibling.keys) < self.m - 1:
                    return True
        return False
        
    # Similarly, this method checks if any right sibling has room for one more key and not be overfull
    def right_sibling_has_room(self, node: Node) -> bool:
        parent = node.parent
        if parent is None:
            return False
        
        index = parent.children.index(node)
        for i in range(index + 1, len(parent.children)):
            if index < len(parent.children) - 1:
                right_sibling = parent.children[i]
                # Check if the right sibling has space
                if len(right_sibling.keys) < self.m - 1:
                    return True
        return False
    
    # This method does a left rotation on the given node
    def left_rotation(self, node: Node):
        # Define the parent as well as the index where the child is within the parent's children list
        parent = node.parent
        index = parent.children.index(node)
        left_sibling = parent.children[index - 1]
        # Define the keys that will be rotating, from right child to parent and parent to left child
        new_parent_key = node.keys.pop(0)
        new_node_key = parent.keys[index - 1]
        parent.keys[index - 1] = new_parent_key
        # Add the key to the left child and sort the key list
        left_sibling.keys.append(new_node_key)
        left_sibling.keys.sort()
        # Ensure that any associated children of the node that was rotated move with it
        rotating_child = node.children.pop(0)
        left_sibling.children.append(rotating_child)
        if rotating_child is not None:
            rotating_child.parent = left_sibling
        # If the left sibling is now overfull, do another left rotation
        if len(left_sibling.keys) > self.m - 1:
            self.left_rotation(left_sibling)

    # Similarly, this method does a right rotation
    def right_rotation(self, node: Node):
        parent = node.parent
        index = parent.children.index(node)
        right_sibling = parent.children[index + 1]

        new_parent_key = node.keys.pop(-1)
        new_node_key = parent.keys[index]
        parent.keys[index] = new_parent_key

        right_sibling.keys.append(new_node_key)
        right_sibling.keys.sort()

        rotating_child = node.children.pop()
        right_sibling.children.insert(0, rotating_child)
        if rotating_child is not None:
            rotating_child.parent = right_sibling

        if len(right_sibling.keys) > self.m - 1:
            self.right_rotation(right_sibling)

    # This method does split and promote
    def split_node(self, node: Node):
        # Define the parent node and find the lower median which will be promoted
        parent = node.parent     
        if len(node.keys) % 2 == 0:
            lower_median_index = (len(node.keys) // 2) - 1
        else:
            lower_median_index = len(node.keys) // 2
        mid_key = node.keys[lower_median_index]

        # Create two new nodes
        left_child = Node(keys = node.keys[:lower_median_index], children = node.children[:lower_median_index + 1], parent = parent)
        right_child = Node(keys = node.keys[lower_median_index + 1:], children = node.children[lower_median_index + 1:], parent = parent)
        
        # Ensure that the new nodes' children are 1 + number of keys
        while len(left_child.children) < len(left_child.keys) + 1:
            left_child.children.append(None)
    
        while len(right_child.children) < len(right_child.keys) + 1:
            right_child.children.append(None)

        # Update the children's parent
        for child in left_child.children:
            if child:
                child.parent = left_child
        for child in right_child.children:
            if child:
                child.parent = right_child

        # Create a new root if there isnt a parent
        if parent is None: 
            self.root = Node(keys = [mid_key], children = [left_child, right_child])
            left_child.parent = self.root
            right_child.parent = self.root
        # Insert the lower median key into the parent and attach the new children
        else:
            parent.keys.append(mid_key)
            parent.keys.sort()
            parent.children[parent.children.index(node)] = left_child
            parent.children.insert(parent.children.index(left_child) + 1, right_child)

            # Now check if the parent is overfull. 
            if len(parent.keys) > self.m - 1:
                # If it is we check if any sibling has room, if not, do another split and promote
                if self.left_sibling_has_room(parent):
                    self.left_rotation(parent)
                elif self.right_sibling_has_room(parent):
                    self.right_rotation(parent)
                else:
                    self.split_node(parent)

    # Helpers for deletion

    # This helper method finds the IOS and the node that it belongs to
    def get_ios_with_node(self, node: Node, key: int) -> (int, Node):
        # The IOS will always be the smallest value in the right subtree
        index = node.keys.index(key)
        right_child = node.children[index + 1]
        # Traverse all the tree until we get to leftmost value in the right subtree
        while right_child.children[0] is not None:
            right_child = right_child.children[0]
        return right_child.keys[0], right_child
    
    # This method checks is a left sibling has extra keys to share without being underfull
    def left_sibling_has_extra(self, node: Node) -> bool:
        parent = node.parent
        if parent is None:
            return False
        
        index = parent.children.index(node)
        # Look for the first sibling that has keys to spare
        for i in range(index - 1, -1, -1):
            if index > 0:
                left_sibling = parent.children[i]
                if len(left_sibling.keys) > math.ceil(self.m / 2) - 1:
                    return True               
        return False
    
    # This method finds the specific sibling with keys to spare, similar to the above but returns the node
    def closest_left_with_extra(self, node: Node) -> Node:
        parent = node.parent
        index = parent.children.index(node)
        if parent is not None:
            for i in range(index - 1, -1, -1):
                if index > 0:
                    left_sibling = parent.children[i]
                    if len(left_sibling.keys) > math.ceil(self.m / 2) - 1:
                        return left_sibling
    
    # Similarly we have a method to find if there is a right sibling with keys to spare
    def right_sibling_has_extra(self, node: Node) -> bool:
        parent = node.parent
        if parent is None:
            return False
        
        index = parent.children.index(node)
        for i in range(index + 1, len(parent.children)):
            if index < len(parent.children) - 1:
                right_sibling = parent.children[i]
                if len(right_sibling.keys) > math.ceil(self.m / 2) - 1:
                    return True        
        return False
    
    # Similarly, we have a method to find the closest right sibling with keys to spare
    def closest_right_with_extra(self, node: Node) -> Node:
        parent = node.parent
        index = parent.children.index(node)
        if parent is not None:
            for i in range(index + 1, len(parent.children)):
                if index < len(parent.children) - 1:
                    right_sibling = parent.children[i]
                    if len(right_sibling.keys) > math.ceil(self.m / 2) - 1:
                        return right_sibling

    # This method does a sequence of right rotations as needed starting at the left sibling with keys to spare until a node is not underfull
    def right_rotation_seq(self, node: Node):
        curr_node = self.closest_left_with_extra(node)
        parent = curr_node.parent
        index = parent.children.index(curr_node)
        right_sibling = parent.children[index + 1]

        new_parent_key = curr_node.keys.pop(-1)
        new_node_key = parent.keys[index]
        parent.keys[index] = new_parent_key

        right_sibling.keys.append(new_node_key)
        right_sibling.keys.sort()
        # Update child of key being rotated
        rotating_child = curr_node.children.pop()
        right_sibling.children.insert(0, rotating_child)
        if rotating_child is not None:
            rotating_child.parent = right_sibling
        # If still underfull keep the sequence
        if len(node.keys) < math.ceil(self.m / 2) - 1:
            self.right_rotation_seq(node)

    # In a similar way, this does left rotation starting at closest right sibling with extra keys until no node is underfull
    def left_rotation_seq(self, node: Node):
        curr_node = self.closest_right_with_extra(node)
        parent = curr_node.parent
        index = parent.children.index(curr_node)
        left_sibling = parent.children[index - 1]

        new_parent_key = curr_node.keys.pop(0)
        new_node_key = parent.keys[index - 1]
        parent.keys[index - 1] = new_parent_key

        left_sibling.keys.append(new_node_key)
        left_sibling.keys.sort()
        # Update child of key being rotated
        rotating_child = curr_node.children.pop()
        left_sibling.children.append(rotating_child)
        if rotating_child is not None:
            rotating_child.parent = left_sibling
        # If still underfull keep the sequence
        if len(node.keys) < math.ceil(self.m / 2) - 1:
            self.left_rotation_seq(node)
    
    # This method merges a node with its left sibling and the corresponding parent key
    def merge_with_left(self, node: Node):
        parent = node.parent
        index = parent.children.index(node)
        left_sibling = parent.children[index - 1]

        left_sibling.keys += [parent.keys.pop(index - 1)] + node.keys
        left_sibling.children += node.children

        parent.children.remove(node)
        # Update the parents in the newly formed node
        for child in left_sibling.children:
            if child:
                child.parent = left_sibling

        # Check that the parent is not underfull
        if len(parent.keys) < math.ceil(self.m / 2) - 1:
            if parent == self.root and len(parent.keys) == 0:
                self.root = left_sibling
                left_sibling.parent = None
            else:
                self.handle_underfull(parent)

    # Similarly, this method merges a node with its right sibling and the corresponding parent key
    def merge_with_right(self, node: Node):
        parent = node.parent
        index = parent.children.index(node)
        right_sibling = parent.children[index + 1]

        node.keys += [parent.keys.pop(index)] + right_sibling.keys
        node.children += right_sibling.children

        parent.children.remove(right_sibling)
        # Update children's parent
        for child in node.children:
            if child: 
                child.parent = node
        # Check that the parent is not not underfull
        if len(parent.keys) < math.ceil(self.m / 2) - 1:
            if parent == self.root and len(parent.keys) == 0:
                self.root = node
                node.parent = None
            else:
                self.handle_underfull(parent)

    # This is the method we use to handle underfull nodes
    def handle_underfull(self, node: Node):
        parent = node.parent
        index = parent.children.index(node)
        if parent is None:
            return
        # If a left sibling has keys to spare, do sequence of right rotations
        if self.left_sibling_has_extra(node):
            self.right_rotation_seq(node)
        # If a right sibling has keys to spare, do a sequence of left rotations
        elif self.right_sibling_has_extra(node):
            self.left_rotation_seq(node)
        # If no siblings have keys to spare merge with left sibling if possible
        elif index > 0:
            self.merge_with_left(node)
        # If there is not left sibling to merge with, merge with the right sibling
        else:
            self.merge_with_right(node)
    
    # This method deletes the IOS 
    def delete_ios(self, node: Node, key = int):
        node.keys.remove(key)
        while len(node.children) > len(node.keys) + 1:
            node.children.pop()
        if node.parent is not None and len(node.keys) < math.ceil(self.m / 2) - 1:
            self.handle_underfull(node)

    # Insert.
    def insert(self, key: int):
        # Check if the tree is empty
        if self.root is None:
            self.root = Node(keys = [key], children = [], parent = None)
        else:
            # Find the correct node where the insertion needs to happen
            node = self.find_node(self.root, key)
            # Insert the given key into the correct node
            self.insert_key(node, key)
        
    # Delete.
    def delete(self, key: int):
        # Find the node containing the key we want to delete
        node = self.find_node(self.root, key)
        index = node.keys.index(key)
        # Check if the key is in a non-leaf node
        if node.children[0] is not None:
            # Find the IOS so that it can be the replacement key
            replacement_key, ios_node = self.get_ios_with_node(node, key)
            node.keys[index] = replacement_key
            # After replacing the key, make sure we delete the ios which was on a leaf node
            self.delete_ios(ios_node, replacement_key)

        # If the key is in a leaf, simply delete
        else:
            node.keys.remove(key)
        # Ensure we still have the right number of children, that is 1 + number of keys
        while(len(node.children) > len(node.keys) + 1):
            node.children.pop()
        # Check if the node we deleted from is underfull. If it is, handle it accordingly
        if node.parent is not None and len(node.keys) < math.ceil(self.m / 2) - 1:
            self.handle_underfull(node)

    # Search
    def search(self,key) -> str:
        # Keep track of the current node and the list we will return as we traverse the tree searching for a value
        curr_node = self.root
        path_indices = []  

        # If the key is in the root, return an empty list
        if key in curr_node.keys:
            return json.dumps([])

        # Traverse the tree until we find the key
        while curr_node is not None:
            # If the key is in the current node, return the list
            if key in curr_node.keys:
                return json.dumps(path_indices)
            # Compare the key to each key in the current node and see where we can continue our search
            for i, k in enumerate(curr_node.keys):
                if key < k:
                    # Append as we travel down the tree
                    path_indices.append(i)
                    curr_node = curr_node.children[i]  
                    break
            # If the key is greater than all current node's keys, we need the last child
            else:  
                path_indices.append(len(curr_node.keys))  
                curr_node = curr_node.children[-1]


