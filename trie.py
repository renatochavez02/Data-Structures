from __future__ import annotations
from typing import List
import json
import os

verbose = False

# The class for a particular Node in the tree.
# None-leaf nodes have:
#     value = None (the Python None)
#     branches = List of branches.
#                Each branch is an object with keys 'label' and 'child',
#                Here 'label' is the branch label.
#                Here 'child' points to the corresponding child Node.
# Leaf nodes have:
#     value = the value associated to that branch path.
#     branches = Empty list.
#
# Note: You do not need to sort the list of branches.  The dump function takes care of this for printing.
# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  value      : int = None,
                  branches   : List[None] = None):
        self.value      = value
        self.branches   = branches

class Trie():
    def __init__(self,
                 root: Node = None):
         self.root = None

    # DO NOT MODIFY!
    def dump(self):
        def _to_dict(node) -> dict:
            st = []
            node.branches.sort(key=lambda x:x['label'])
            for b in node.branches:
                st.append({'label':b['label'],'child':_to_dict(b['child'])})
            return {
                "value"      : node.value,
                "branches"   : st
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        print(json.dumps(dict_repr,indent = 2))

    # Helper method that helps us insert a word and its value based on the currrent compressed trie
    def insert_word(self, node: Node, word: str, value: int):
        # Iterate through all branches finding prefixes 
        for branch in node.branches:
            # For simplicity, we create a label variable and child variable
            label = branch['label']
            child = branch['child']

            # If the word starts with the current label, we can follow down the trie to the child node.
            if word.startswith(label):
                # Recursively call insert_word with the remaining part of the label
                self.insert_word(child, word[len(label):], value)
                return

            # Check if there is a common prefix between the word we want to add and the current branch label.
            common_prefix_len = 0
            for i in range(min(len(word), len(label))):
                if word[i] == label[i]:
                    common_prefix_len += 1
                else:
                    break
            # If there is a prefix, then we split the branch 
            if common_prefix_len > 0:
                # Declare useful variables for the split
                common_prefix = label[:common_prefix_len]
                leftover_label = label[common_prefix_len:]
                leftover_word = word[common_prefix_len:]
                # Update the existing branch to now be the common prefix
                branch['label'] = common_prefix
                new_child = Node(branches=[])
                new_child.branches.append({'label': leftover_label, 'child': child})
                # Add a new branch with the leftover word and value
                new_child.branches.append({'label': leftover_word, 'child': Node(value=None, branches=[{'label': '$', 'child': Node(value=value, branches=[])}])})
                branch['child'] = new_child
                return

        # If there is no common prefix, simply add a new branch
        if node.branches is None:
            node.branches = []
        node.branches.append({'label': word, 'child': Node(value=None, branches=[{'label': '$', 'child': Node(value=value, branches=[])}])})

    # Helper method to traverse the compress trie and return the value associated to the given word.
    def search_word(self, node: Node, word: str) -> int:
        # Check each branch in the given node
        for branch in node.branches:
            # Declare useful variables to refer to them later
            label = branch['label']
            child = branch['child']
            # If there is a match between the label and the word
            if word.startswith(label):
                # If it is a full match check for the dollar sign and return value
                if word == label:
                    if '$' in [b['label'] for b in child.branches]:
                        return child.branches[0]['child'].value
                    #return self.search_word(child, word[len(label):])
                # If it is a partial match, recursively call function with the leftover label
                return self.search_word(child, word[len(label):])

    # Insert thew word and the associated value into the compressed trie.
    def insert(self,word,value):
        # If the compressed trie is empty, simply add the word, value pair as the new root
        if not self.root:
            self.root = Node(branches=[])
            self.root.branches.append({'label': word, 'child': Node(value=None, branches=[{'label': '$', 'child': Node(value=value, branches=[])}])})
            return
        # Else, insert the word, value pair accordingly
        self.insert_word(self.root, word, value)

    # Delete the word and the associated value.
    def delete(self,word):
        # Check if the trie is empty
        if not self.root:
            return
        # Set variables that will help us keep track of where we are at in the trie
        grandparent_node = None
        parent_node = None
        curr_node = self.root
        branch_to_delete = None
        # Locate the leaf node, its parent, and grandparent
        while word and branch_to_delete is None:
            found = False # This will help us stop once we find the variable
            # Apply a similar logic to search, but we will get now the parent and grandparent nodes
            for branch in curr_node.branches:
                label = branch['label']
                child = branch['child']

                if word.startswith(label):
                    if word == label:
                        if '$' in [b['label'] for b in child.branches]:
                            grandparent_node = parent_node
                            parent_node = curr_node
                            branch_to_delete = branch
                            curr_node = child
                            found = True
                            break
                    else:
                        grandparent_node = parent_node
                        parent_node = curr_node
                        curr_node = child
                        word = word[len(label):]
                        found = True
                        break
            if not found:
                return
        # Delete the leaf node
        for i, branch in enumerate(curr_node.branches):
            if branch['label'] == '$':
                del curr_node.branches[i]
                break
        
        # Handle accordingly after deleting the node, potentially splicing
        while parent_node is not None:
            if not curr_node.branches:
                for i, branch in enumerate(parent_node.branches):
                    if branch['child'] == curr_node:
                        # Delete the node from the parent node
                        del parent_node.branches[i]
                        # Check if the parent node ended up with a single branch and is not the root
                        if len(parent_node.branches) == 1 and parent_node != self.root:
                            # This is the branch that we'll add to its parent branch
                            child_branch = parent_node.branches[0]
                            if grandparent_node:
                                for branch in grandparent_node.branches:
                                    # Merge the single branch and its children
                                    if branch['child'] == parent_node:
                                        branch['label'] += child_branch['label']
                                        branch['child'] = child_branch['child']
                                        break
                            break
            curr_node = parent_node
            parent_node = None

            # Find the new parent if there is any
            if curr_node != self.root:
                for branch in self.root.branches:
                    if branch['child'] == curr_node:
                        parent_node = self.root
                        break
                    else:
                        for b in branch['child'].branches:
                            if b['child'] == curr_node:
                                parent_node = branch['child']
                                break
                    if parent_node:
                        break

    # Search for the word and print the associated value.
    def search(self,word):
        # Call our recursive helper method to find the corresponding value
        value = self.search_word(self.root, word)
        print(value)     