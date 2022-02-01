# Threading https://stackoverflow.com/a/2906014/14058946

from pathfinding_visualizer.ColorCollection import Colors
from pathfinding_visualizer.Graph import NetworkGraph
from pathfinding_visualizer.Pathfinding import BreadthFirst
import pygame
import sys

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
print("\n#############################  CONTROLS  #############################")
print("'mouse_left_click'               --> create OR select node")
print("'mouse_cursor_on_node'  +  's'   --> mark node as start node")
print("'mouse_cursor_on_node'  +  'e'   --> mark node as end node")
print("'mouse_cursor_on_node'  +  'r'   --> remove node")
print("'c'                              --> connect all selected nodes (to select a node, click on it)")
print("'d'                              --> disconnect all selected nodes (to select a node, click on it)")
print("'1'                              --> start bread-first algorithm")
print("'2'                              --> start depth-first algorithm")
print("'3'                              --> start dijkstra algorithm")
print("'SPACE'                          --> reset the graph\n")


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
                    pass
                    print("Started DepthFirst Algorithm. This does NOT return the shortest path (tree structure excepted).")
                    #algorithm = BreadthFirst(network_graph, network_graph.get_start_node(), network_graph.get_end_node())
            elif event.key == pygame.K_3:
                if network_graph.get_start_node() is None or network_graph.get_end_node() is None:
                    print("You have to specify start and end node to start the algorithm!")
                else:
                    pass
                    print("Started Dijkstra Algorithm. This returns the shortest path in a weighted graph.")
                    #algorithm = BreadthFirst(network_graph, network_graph.get_start_node(), network_graph.get_end_node())
            elif event.key == pygame.K_SPACE: # 'SPACE' --> reset graph
                algorithm = None
                network_graph.reset_states()


# method for updating the algorithm state
def update():
    global time_elapsed, algorithm, clock
    if algorithm is not None:
        time_elapsed += clock.tick()
        if time_elapsed > 2000:  # perform step every 500 milliseconds
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
