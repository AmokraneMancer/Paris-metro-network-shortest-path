#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 09:37:09 2020

@author: amokrane
"""

#networkx library
#https://networkx.github.io/
import networkx as nx
import matplotlib.pyplot as plt
import sys
import queue as q


#function to read the graph from the text file
#O(nodes + edges)
def readGraph():
    #initialise directed graph using networkx library
    g = nx.DiGraph()
    #open the file in rb mode instead of r mode
    #cause : utf-8 decoding issue
    f = open("/home/amokrane/Bureau/RLI/Projet/metro_complet.txt", "r", encoding = "ISO-8859-1")
    #reorganize content
    contents = f.read().split("\n") ##O(numberOfLines)
    #list which contains lines of text file
    result = []
    nodes = 0
    edges = 0
    #O(numberOfLines)
    for c in contents:
        #add line by line to the list
        s = str(c)
        result.append(s)
    #get values
    #O(nodes + edges)
    for i in range(len(result)):
        #get number of nodes and edges
        if i == 0:
            line = result[i].split(" ")
            nodes = int(line[0])
            edges = int(line[1])
        #get nodes with names (stations)
        elif i > 1 and i < nodes + 2:
            line = result[i].split(" ")
            #id of station (node)
            som = int(line[0])
            #station name
            #s used for composed names 
            #(ex : École Vétérinaire de Maisons-Alfort)
            s = ""
            for k in range (1,len(line)):              
                s = s + " " + line[k]
            #add node (id, name) to the graph
            #O(1)
            g.add_node(som, name = s)
        #get edges and weights (connctions between stations)
        elif i > nodes + 2 and i < len(result) - 1:
            line = result[i].split(" ")
            #add edge (out, in, weight = time)
            #O(1)
            g.add_edge(int(line[0]), int(line[1]), weight = float(line[2]))
    f.close()
    return g

#O(nodes)
def drawGraph(g):
    #get position
    pos=nx.spring_layout(g)
    #get stations name
    labels = {k:g.nodes[k]['name'] for k in g.nodes()}
    #get weights
    weightLabels  = nx.get_edge_attributes(g,'weight')
    #draw using matplotlib
    plt.axis('off')
    plt.figure(figsize=(150, 150))
    #draw nodes in blue color
    nx.draw_networkx_nodes(g,pos, node_color='b',node_size=15,alpha=0.8)
    #draw edges in red color
    nx.draw_networkx_edges(g,pos,edge_color='r')
    #add stations names
    nx.draw_networkx_labels(g,pos, labels, font_size = 10)
    #add weigh of each edge
    nx.draw_networkx_edge_labels(g,pos, edge_labels = weightLabels, font_size = 10)
    
    #save in png format
    plt.savefig("/home/amokrane/Bureau/RLI/Projet/graph.png")

#function to print path between two nodes
#g : graph
#parent: list of node parents
#j : current node
#dist : list which contains distance of each node in the path
#from the source
#O(nodes*log(nodes))
def printPath(g, parent, j, dist):
    if parent[j] == -1:
        return
    printPath(g, parent, parent[j], dist)
    print(g.nodes[j]['name'], ' : ', dist[j])
        
#dijsktra shortest path alogorithm (seen in lectures)
#The time complexity is O(edges * log(nodes))) 
#as there will be at most O(edges) nodes 
#in priority queue and O(log(edges)) is same as O(log(nodes)
def dijkstra(g, source, destination):
    #initialize parents list O(1)
    parent = [0 for i in range(len(g.nodes())) ]
    #set the pearent of source as -1 O(1)
    parent[0] = -1
    #list representing distance of each visited node from the source
    #0 for souce, infinity(sys.float_info.max) for all other nodes
    #O(nodes)
    dist = [sys.float_info.max  for i in range(len(g.nodes()))]
    dist[source] = 0
    #priority queue representing visited nodes
    #each element is tuple(distance, node)
    #distance as priority of retrieve
    visited = q.PriorityQueue()
    visited.put((dist[source], source)) #O(1)
    #get the adjacent nodes of each node
    #as dict of dicts
    adjacencyMatrix =  nx.convert.to_dict_of_dicts(g) #O(nodes)

    i = source
    while not visited.empty() and i != destination:
        #retrieve the element having lower distance
        #get() returns a tuple(priority, node)
        #so node is (get())[1]
        s = visited.get() #O(log(nodes))
        i = s[1]
        #get a dict representing ajacent nodes of node i
        #ex: {330: {'weight': 46.0}, 70: {'weight': 45.0}}
        adjacencyDict = adjacencyMatrix[i] #O(1)
        #for each ajacent node of i
        for l in adjacencyDict:
            if dist[l] > dist[i] + adjacencyDict[l]['weight']:
                #update distance as distance of parent in the path
                # + distance of l
                dist[l] = dist[i] + adjacencyDict[l]['weight']
                #push l in queue
                visited.put((dist[l], l)) #O(1)
                #set i as parent of l
                parent[l] = i
                
    #print the path
    printPath(g, parent, destination, dist)
    
def main():
    metroGraph = readGraph()
    #drawGraph(metroGraph)
    #shortest path between Créteil Préfecture – Gare du Nord
    chemin = dijkstra(metroGraph, 119, 161)
    stations = [metroGraph.nodes[k]['name'] for k in chemin[1]]
    print(chemin[0])
    print(stations)
    
#    length = nx.dijkstra_path_length(metroGraph,89,124) 
#    result = nx.dijkstra_path(metroGraph,89,124)  
#    print(length)
#    names = [metroGraph.nodes[k]['name'] for k in result]
#    for n in names:
#        print(n)
if __name__ == '__main__':
    main()
    
#[89, 90, 91, 185, 186, 372, 53, 167, 265, 257, 200, 
# 94, 205, 296, 105, 163, 18, 16, 331, 135,
# 67, 173, 227, 356, 77, 50]
