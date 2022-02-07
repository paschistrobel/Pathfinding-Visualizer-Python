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
Create node | **Mouse_left_click** on free space |
Remove node | Position mouse cursor on existing node + key **'r'** |
Select node | **Mouse_left_click** on existing (unselected) node |
Unselect node | **Mouse_left_click** on existing (selected) node |
Mark start node | Position mouse cursor on existing node + key **'s'** |
Mark end node | Position mouse cursor on existing node + key **'e'** |
Connect nodes | key **'c'** (connects all selected nodes) |
Disconnect nodes | key **'d'** (disconnects all unselected nodes) |
Start breadth-first visualization | key **'1'** |
Start depth-first visualization | key **'2'** |
Stop/Reset algorithm progress | key **'SPACE'** |
### Legend
