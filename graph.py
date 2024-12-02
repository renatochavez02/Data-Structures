from __future__ import annotations
from typing import List

# The Graph object is a bit of a hybrid object.
# It is initialized with only an adjacency matrix self.adjmat but it also contains:
# self.edgelist: A list of edges of the form [x,y] with x<y, sorted by weight with ties broken by x and then by y.
# self.parent: A list which represents the disjoint set data structure corresponding to the edges of the graph.
# self.size: A list such that:
#     if i is the root of a component tree then self.size[i] = the size of the tree
#     else self.size[i] = 1

class Graph():
    def __init__(self,adjmat):
        # The next lines do the following:
        # - Assign self.adjmat from the parameter passed.
        # - Assign self.parent to represent a DSDS containing one component for each edge.
        # - Assign self.size to represent the size of each component.
        self.adjmat = adjmat
        self.parent = list(range(len(adjmat)))
        self.size = [1] * len(adjmat)
        # Fill in edgelist so it is a list of edges of the form [x,y] with x<y,
        # sorted by weight with ties broken by x and then by y.
        # Add the code here to fill in edgelist.
        self.edgelist = []
        for i in range(len(adjmat)):
            for j in range(i + 1, len(adjmat[i])): # Avoid duplicates
                if adjmat[i][j] != 0: # Include edges that have a non-zero value
                    self.edgelist.append([i, j]) # Add edge 
        # Sort the edge list by weight with ties broken by x then y.
        self.edgelist.sort(key=lambda edge: (self.adjmat[edge[0]][edge[1]], edge[0], edge[1]))
        
    # Dump various things from the graph.
    # DO NOT MODIFY!
    def dump_adjmat(self):
        for row in self.adjmat:
            print(row)
    def dump_edgelist(self):
        for row in self.edgelist:
            print(row)

    # Perform Kruskal's Algorithm.
    # Print the list of included edges in the order they are included.
    def kruskal(self):
        includededges = []
        # Iterate through self.edgelist.
        # For each edge determine if adding it would create a cycle.
        # If not, append the edge to includededges.
        # Update the disjoint set data structure accordingly.
        # Once we've obtained the correct number, bail.
        num_vertices = len(self.adjmat)
        for edge in self.edgelist:
            x, y = edge
            if self.findrep(x) != self.findrep(y):
                includededges.append(edge)
                self.union(x, y)
                # If we have enough edges, we stop
                if len(includededges) == num_vertices - 1:
                    break
        # Print the included edges.
        for row in includededges:
            print(row)


    # Perform Kruskal's Algorithm.
    # Print the list of included edges in the order they are included.
    def unkruskal(self):
        excludededges = []
        # Iterate through self.edgelist.
        # For each edge determine if adding it would create a cycle.
        # If so, append the edge to includededges.
        # Update the disjoint set data structure accordingly.
        # Once we've obtained the correct number, bail.
        num_vertices = len(self.adjmat)
        for edge in self.edgelist:
            x, y = edge
            if self.findrep(x) == self.findrep(y):
                excludededges.append(edge)
            else:
                self.union(x, y)
                # If we have enough excluded edges
                if len(excludededges) == len(self.edgelist) - (num_vertices - 1):
                    break
        # Print the excluded edges.
        for row in excludededges:
            print(row)

    # Find the representative for the edge with index i.
    # Use path compression.
    def findrep(self,i) -> int:
        # If i is not the root, in other words, its own parent, 
        if self.parent[i] != i:
            # Recursively call the method with i's parent to find the root and compress
            self.parent[i] = self.findrep(self.parent[i])
        return self.parent[i]

    # Take the weighted union of the sets containing the edges with indices i and j.
    # Use the above findrep.
    def union(self,i,j):
        # Declare variables for readibility and easier access of representatives
        i_rep = self.findrep(i)
        j_rep = self.findrep(j)
        # If i and j are not the same element
        if i_rep != j_rep:
            # Check if the size of i's structure is larger than or equal to j's
            if self.size[i_rep] >= self.size[j_rep]:
                # If so, attach j to i and update the size of i accordingly
                self.parent[j_rep] = i_rep
                self.size[i_rep] += self.size[j_rep]
            # If not, add i to j and update the size of j accordingly
            else:
                self.parent[i_rep] = j_rep
                self.size[j_rep] += self.size[i_rep]