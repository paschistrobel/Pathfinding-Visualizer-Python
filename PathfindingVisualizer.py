import pygame
import sys
from ColorCollection import Colors
from Graph import NetworkGraph
from Pathfinding import BreadthFirst, DepthFirst

########################################################################################################################
# create the application window
########################################################################################################################
pygame.init()
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualization")
# icon from: https://www.iconfinder.com/icons/1891030/blue_direction_gps_location_map_marker_navigation_icon
pygame.display.set_icon(pygame.image.load("icon.png"))

########################################################################################################################
# initialize components, variables, functions
########################################################################################################################
clock = pygame.time.Clock()
time_elapsed = 0
network_graph = NetworkGraph()
algorithm = None
screen.fill(Colors.WHITE)  # make background white initially


########################################################################################################################
# Print information to console
########################################################################################################################
print("\n\nThis is a pathfinding visualization. Two algorithms were implemented to find a path from a specified start to an end node.")
print("The visualization consists of nodes and connections between them, all of which can be manually added/ deleted.")
print("Here's a brief introduction on how to use this tool:")
print("     1. Create Nodes (left clicking with mouse)")
print("     2. Select Nodes (click on existing node) and connect ('c') them --> be aware, that all selected nodes are connected with each other!")
print("     3. If needed, remove nodes (put mouse cursor on node and press 'r') or disconnect them (select nodes and press 'd')")
print("     4. Choose a start node (put mouse on node and press 's') and a target/end node (put mouse on node and press 'e')")
print("     5. Run pathfinding algorithm visualization ('1' for BreadthFirstSearch, '2' for DepthFirstSearch) --> be aware that to you need to specify a start and end node to start the pathfinding (However, they do not need to be connected)")
print("     6. Reset the pathfinding algorithm progress ('SPACE')")

print("Now you should have a general clue of what to do. Below you find further information...")
print("Below you find an summary of controls, as well as an explanation for what the different colors stand for...")
########################################################################################################################
# Print controls to console
########################################################################################################################
print("\n#############################  CONTROLS  #############################")
print("'mouse_left_click'               --> create OR select node")
print("'mouse_cursor_on_node'  +  's'   --> mark node as start node --> start node has one ring around it")
print("'mouse_cursor_on_node'  +  'e'   --> mark node as end node --> end node has two rings around it")
print("'mouse_cursor_on_node'  +  'r'   --> remove node")
print("'c'                              --> connect all selected nodes (to select a node, click on it)")
print("'d'                              --> disconnect all selected nodes (to select a node, click on it)")
print("'1'                              --> start bread-first algorithm")
print("'2'                              --> start depth-first algorithm")
print("'SPACE'                          --> reset the pathfinding algorithm progress")

########################################################################################################################
# Print the meaning of colors to console
########################################################################################################################
print("\n#############################  COLORS  #############################")
print("The color of a node or a connection represents its current state. Below a list of possible colors and their meanings...")
print("BLACK        --> Default node state")
print("BLUE         --> Node is currently selected and can be connected ('c') or disconnected ('d') with other selected nodes. Note that a node does not have to be selected to delete it/ mark it as start or end point")
print("Lime/Green   --> The lime colored node is the one that is currently looked at from the pathfinding algorithm")
print("GREY         --> grey nodes/ paths mean that they are currently on the 'waiting list', waiting to be be visited by the algorithm (but have not been visited yet)")
print("PURPLE       --> Nodes that were already visited by the pathfinding algorithm")
print("PINK         --> After a pathfinding algorithm was successfull, the path from start to end node is colored pink")

# method for handling user input
def handle_input():
    global algorithm, network_graph
    focused_node = network_graph.get_focused_node(pygame.mouse.get_pos())  # get the node that is currently focused
    if focused_node is not None:
        focused_node.hover()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # end application
        if event.type == pygame.MOUSEBUTTONDOWN:
            if focused_node is not None:  # mouse is placed on a node
                focused_node.click()
            elif network_graph.has_node_near_pos(pygame.mouse.get_pos()):  # mouse is placed close to another node
                print("Nodes too close to another node!")
            else:  # mouse in free space --> node can be created
                network_graph.add_node(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # 's' --> mark start node
                if focused_node is not None:
                    network_graph.set_start_node(focused_node)
            elif event.key == pygame.K_e:  # 'e' --> mark end node
                if focused_node is not None:
                    network_graph.set_end_node(focused_node)
            elif event.key == pygame.K_c:  # 'c' --> connect selected nodes
                network_graph.connect_selected_nodes()
            elif event.key == pygame.K_d:   # 'd' --> disconnect selected nodes
                network_graph.disconnect_selected_nodes()
            elif event.key == pygame.K_r:   # 'r' --> remove node
                if focused_node is not None:
                    network_graph.remove_node(focused_node)
            elif event.key == pygame.K_1:   # '1' --> start bfs
                if network_graph.get_start_node() is None or network_graph.get_end_node() is None:
                    print("You have to specify start and end node to start the algorithm!")
                else:
                    print("Started BreadFirst Algorithm. This returns the shortest path in an unweighted graph.")
                    algorithm = BreadthFirst(network_graph, network_graph.get_start_node(), network_graph.get_end_node())
            elif event.key == pygame.K_2:
                if network_graph.get_start_node() is None or network_graph.get_end_node() is None:
                    print("You have to specify start and end node to start the algorithm!")
                else:
                    algorithm = DepthFirst(network_graph, network_graph.get_start_node(), network_graph.get_end_node())
                    print("Started DepthFirst Algorithm. This does NOT return the shortest path (tree structure excepted).")
            elif event.key == pygame.K_SPACE: # 'SPACE' --> reset graph
                algorithm = None
                network_graph.reset_states()


# method for updating the algorithm state
def update():
    global time_elapsed, algorithm, clock
    if algorithm is not None:
        time_elapsed += clock.tick()
        if time_elapsed > 500:  # perform step every 500 milliseconds
            if not algorithm.has_finished():
                algorithm.step()
                time_elapsed = 0


# method for display the updates on canvas
def draw():
    global network_graph
    # override canvas
    screen.fill(Colors.WHITE)
    # draw everything on white canvas
    network_graph.draw(screen)
    # make the updates visible
    pygame.display.update()


########################################################################################################################
# "Game" loop
########################################################################################################################
while True:
    handle_input()
    update()
    draw()
