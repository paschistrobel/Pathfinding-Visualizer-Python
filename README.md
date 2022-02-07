# Python Pathfinding Visualizer
## Required Installations
```
 python3 -m pip install pygame==2.1.2
```
## Usage
Start the application: 
```
 python PathfindingVisualizer.py
```
### Introduction
This is a visualization tool for pathfinding algorithms. The visualization consists of nodes and connections between them (paths). Each node and each connection can be manually added or removed. To get startet you can follow the short tutorial below:
1. Create nodes on the canvas (**by clicking left mouse button**) --> each node created is provided with a unique label (single character)
2. Select your created nodes (**by clicking on existing node**) and connect (**key 'c'**) them --> be aware, that all selected nodes are connected with each other!
3. If needed, remove nodes (**by placing mouse cursor on node and pressing key 'r'**) or disconnect them (**by selecting nodes and pressing key 'd'**)
4. Choose a start node (**by putting mouse on node and pressing key 's'**) and a target/end node (**by putting mouse on node and pressing key 'e'**)
5. Run pathfinding algorithm visualization (**key '1' for BreadthFirstSearch, key '2' for DepthFirstSearch**) --> be aware that to you need to specify a start and end node to start the pathfinding (However, they do not need to be connected)
6. Stop/Reset the pathfinding algorithm progress (**key 'SPACE'**)

A summary of the possible actions, as well as a legend for the meaning of colors and symbols can be found in the next two sections.
### Controls
Action | Controls |
--- | --- |
Create Node | 301 |
```
'mouse_left_click'               --> create/select node
'mouse_cursor_on_node'  +  's'   --> mark node as start node --> start node has one ring around it
'mouse_cursor_on_node'  +  'e'   --> mark node as end node --> end node has two rings around it
'mouse_cursor_on_node'  +  'r'   --> remove node
'c'                              --> connect all selected nodes (to select a node, click on it)
'd'                              --> disconnect all selected nodes (to select a node, click on it)
'1'                              --> start bread-first algorithm
'2'                              --> start depth-first algorithm
'SPACE'                          --> reset the pathfinding algorithm progress
```
### Legend
