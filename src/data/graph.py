from random import randint, choice

NON_EXISTENT_VERTEX = "The vertex does not exist in the graph."
NON_EXISTENT_VERTICES = "One or both of the vertices do not exist in the graph."
EXISTENT_VERTEX = "The vertex already exists in the graph."
DISJOINT_VERTICES = "The vertices are not connected by an edge."
NO_VERTICES = "The graph has no vertices."

class Node():

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f'{self.name}'
    
    def __str__(self) -> str:
        return f'{self.name}'
    
class Graph():
    
    def __init__(self, is_directed, vertex_list = []):
        self.is_directed = is_directed
        self.vertices = vertex_list
        self.num_vertices = len(vertex_list)
        self.structure = {}
        
        if vertex_list:
            for vertex in vertex_list:
                self.structure[vertex] = {}
    
    def belongs(self, v):
        return v in self.structure

    def add_vertex(self, v):
        if self.belongs(v):
            raise ValueError(EXISTENT_VERTEX) 
            
        self.vertices.append(v)
        self.structure[v] = {}
        self.num_vertices += 1

    def add_edge(self, v, w, weight = 1):
        if self.belongs(v) and self.belongs(w):
            self.structure[v][w] = weight
            if not self.is_directed: 
                self.structure[w][v] = weight
        else:
            raise ValueError(NON_EXISTENT_VERTICES)

    def are_connected(self, v, w):
        if not self.belongs(v) or not self.belongs(w):
            raise ValueError(NON_EXISTENT_VERTICES)
            
        w_in_v = (w in self.structure[v])
        if self.is_directed:
            return w_in_v
        return v in self.structure[w] and w_in_v

    def edge_weight(self, v, w):
        if not self.belongs(v) or not self.belongs(w):
            raise ValueError(NON_EXISTENT_VERTICES)
        
        if not self.are_connected(v,w):
            return ValueError(DISJOINT_VERTICES)
        
        return self.structure[v][w]

    def get_vertices(self):
        return self.vertices