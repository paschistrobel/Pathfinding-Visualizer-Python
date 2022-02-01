import pygame
from pathfinding_visualizer.ColorCollection import Colors
from enum import Enum
import math

NODE_RADIUS = 20  # radius of nodes
MAX_NODES = 20  # max 20 nodes can be displayed
HOVER_RADIUS_DECREASE = 3

pygame.font.init()
font = pygame.font.SysFont(None, 30)


# type of node
class Type(Enum):
    DEFAULT = 0  # default node
    START = 1  # start node
    END = 2  # target/end node


# state of node
class State(Enum):
    DEFAULT = 0
    ENQUEUED = 1  # node waiting in queue
    VISITED = 2  # node was already looked at
    INSPECTED = 3  # actively looked at from pathfinding algorithm
    FINAL = 4


# class for representing a single node
class Node:
    def __init__(self, pos, label=""):
        self.pos = pos  # tuple (x, y)
        self.label = label  # label of node --> ASCII character
        self.type = Type.DEFAULT  # what kind of node is it
        self.state = State.DEFAULT  # state of the node
        self.radius = NODE_RADIUS  # radius of the node
        self.color = Colors.BLACK  # color of node --> dependent on state
        self.hovered = False  # is node currently hovered on
        self.selected = False  # is node currently selected
        self.neighbours = {}  # dict that has all nodes that are connected with this node

    # add a neighbour node and it's connection
    def add_neighbour(self, neighbour, connection):
        if neighbour in self.neighbours.keys():
            print(f"Connection from {self} to {neighbour} already exists!")
        else:
            self.neighbours[neighbour] = connection

    # remove neighbour from the neighbour list/dict
    def remove_neighbour(self, neighbour):
        if neighbour in self.neighbours.keys():
            del self.neighbours[neighbour]
        else:
            print("There is no connection that could be removed...")

    # make the node to start node or revoke this status
    def make_start_node(self, make_start=True):
        self.type = Type.START if make_start else Type.DEFAULT

    # make the node to start node or revoke this status
    def make_end_node(self, make_end=True):
        self.type = Type.END if make_end else Type.DEFAULT

    # add hover effect
    def hover(self):
        self.hovered = True

    # node is put in queue from another node
    def enqueued_from(self, node):  # node was added to queue from a node
        self.state = State.ENQUEUED
        self.neighbours[node].set_enqueued(True)
        self.adjust_color()

    def inspected_from(self, node=None):
        if node is not None:
            self.neighbours[node].set_inspected(True)
        self.state = State.INSPECTED
        self.adjust_color()

    def visited_from(self, node=None):
        if node is not None:
            self.neighbours[node].set_visited(True)
        self.state = State.VISITED
        self.adjust_color()

    def already_visited(self):
        return self.state == State.VISITED or self.state == State.ENQUEUED or self.state == State.INSPECTED

    def highlight_path_to_node(self, node=None):
        self.color = Colors.PINK
        self.state = State.FINAL
        self.adjust_color()
        if node is not None:
            self.neighbours[node].highlight_as_final_path()

    # reset node state to DEFAULT, as well as all outgoing connections
    def reset_state(self):
        self.state = State.DEFAULT
        for connection in self.neighbours.values():
            connection.reset()
        self.adjust_color()

    def is_start_node(self):
        return self.type == Type.START

    def is_end_node(self):
        return self.type == Type.END

    def is_selected(self):
        return self.selected

    def adjust_color(self):
        if self.state == State.DEFAULT:
            if self.selected:
                self.color = Colors.BLUE
            else:
                self.color = Colors.BLACK
        elif self.state == State.ENQUEUED:
            self.color = Colors.GREY
        elif self.state == State.INSPECTED:
            self.color = Colors.LIME
        elif self.state == State.VISITED:
            self.color = Colors.PURPLE
        elif self.state == State.FINAL:
            self.color == Colors.PINK

    def click(self):
        self.selected = not self.selected  # inverse the selection
        self.adjust_color()

    def get_neighbours(self):
        return self.neighbours.keys()

    def get_pos(self):
        return self.pos

    def get_label(self):
        return self.label

    def draw_connections(self, screen):
        for node, connection in self.neighbours.items():
            connection.draw(screen)

    def draw(self, screen):  # draw node and its connections on screen
        if self.type == Type.START:  # draw one outer ring around start node
            pygame.draw.circle(screen, self.color, self.pos,
                               self.radius - HOVER_RADIUS_DECREASE + 5 if self.hovered else self.radius + 5, 2)
        elif self.type == Type.END:  # draw two outer rings around start node
            pygame.draw.circle(screen, self.color, self.pos,
                               self.radius - HOVER_RADIUS_DECREASE + 5 if self.hovered else self.radius + 5, 2)
            pygame.draw.circle(screen, self.color, self.pos,
                               self.radius - HOVER_RADIUS_DECREASE + 10 if self.hovered else self.radius + 10, 2)
        pygame.draw.circle(screen, self.color, self.pos,
                           self.radius - HOVER_RADIUS_DECREASE if self.hovered else self.radius)
        self.hovered = False  # reset hover effect
        # draw label onto the node
        img = font.render(self.label, True, Colors.WHITE)
        screen.blit(img, (self.pos[0] - 7, self.pos[1] - 7))

    def __str__(self):
        return self.label


class Connection:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.weight = math.dist(start_pos, end_pos)  # weight = distance
        self.color = Colors.BLACK
        self.enqueued = False
        self.part_of_final_path = False
        self.inspected = False
        self.visited = False

    def set_enqueued(self, enqueued):
        self.enqueued = enqueued

    def set_inspected(self, inspected):
        self.inspected = inspected

    def set_visited(self, visited):
        self.visited = visited

    def highlight_as_final_path(self):
        self.part_of_final_path = True

    def reset(self):
        self.visited = False
        self.inspected = False
        self.enqueued = False
        self.part_of_final_path = False

    def get_weight(self):
        return self.weight

    def draw(self, screen):  # draw connection on screen
        if self.part_of_final_path:
            pygame.draw.line(screen, Colors.PINK, self.start_pos, self.end_pos, 3)
        elif self.visited:
            pygame.draw.line(screen, Colors.PURPLE, self.start_pos, self.end_pos, 3)
        elif self.inspected:
            pygame.draw.line(screen, Colors.LIME, self.start_pos, self.end_pos, 3)
        elif self.enqueued:
            pygame.draw.line(screen, Colors.GREY, self.start_pos, self.end_pos, 3)
        else:
            pygame.draw.line(screen, Colors.BLACK, self.start_pos, self.end_pos, 3)


# collection of nodes that are connected
class NetworkGraph:
    def __init__(self):
        self.nodes = set()  # collection of all nodes that are part of the graph
        self.node_count = 0  # nodes that are currently part of the graph
        self.start_node = None  # node marked as start node
        self.end_node = None  # node marked as end/target node
        self.total_nodes_created = 0  # total number of nodes that were created (deleted ones inclusive)

    # add new node to graph at coordinate (pos)
    def add_node(self, pos):
        if self.node_count < MAX_NODES:
            node = Node(pos, chr(
                65 + self.total_nodes_created))  # label of node is character (alphabetical order --> Ascii char 65 = 'A')
            self.nodes.add(node)
            self.node_count += 1
            self.total_nodes_created += 1
        else:
            print(f"You can not create more than {MAX_NODES} nodes!")

    # connect two nodes
    def connect_nodes(self, node1, node2):
        connection = Connection(node1.get_pos(), node2.get_pos())
        node1.add_neighbour(node2, connection)
        node2.add_neighbour(node1, connection)

    # disconnect two nodes
    def disconnect_nodes(self, node1, node2):
        node1.remove_neighbour(node2)
        node2.remove_neighbour(node1)

    # check if the graph has a node near a certain position, so that a new node would not overlap
    def has_node_near_pos(self, pos):
        for node in self.nodes:
            if math.dist(node.get_pos(), pos) <= 2 * NODE_RADIUS:
                return True
        return False

    # get the node that is currently focused with the mouse; None otherwise
    def get_focused_node(self, mouse_pos):
        for node in self.nodes:
            if math.dist(mouse_pos, node.get_pos()) <= NODE_RADIUS:
                return node
        return None

    # reset states of all nodes
    def reset_states(self):
        for node in self.nodes:
            node.reset_state()

    # get all the nodes that are part of the graph
    def get_nodes(self):
        return self.nodes

    # get the start node of the graph
    def get_start_node(self):
        return self.start_node

    # mark a node of the graph as start node
    def set_start_node(self, node):
        if node.is_end_node():  # user wants to change current end node to start node
            self.end_node = None    # reset end node to None
        if self.start_node is not None:  # start node already exists
            self.start_node.make_start_node(False)  # reset previous start node
        node.make_start_node()
        self.start_node = node

    # get the end node of the graph
    def get_end_node(self):
        return self.end_node

    # mark a node of the graph as end node
    def set_end_node(self, node):
        if node.is_start_node():  # user wants to change current start node to end node
            self.start_node = None  # reset start node to None
        if self.end_node is not None:  # end node already exists
            self.end_node.make_end_node(False)  # reset previous end node
        node.make_end_node()
        self.end_node = node

    # return the current number of nodes in the graph
    def get_node_count(self):
        return self.node_count

    # highlight the final path from start to end node; final_path = list of nodes
    def highlight_final_path(self, final_path):
        i = 0
        while i < len(final_path):  # iterate over every node in final_path
            if i == len(final_path) - 1:
                final_path[i].highlight_path_to_node() # last node in path has no connection --> only highlight the node
            else:
                final_path[i].highlight_path_to_node(final_path[i + 1]) # highlight node and the connection to next one
            i += 1

    # connect all nodes that were selected by user
    def connect_selected_nodes(self):
        selected_nodes = [node for node in self.nodes if node.is_selected()]    # get all selected nodes
        while len(selected_nodes) > 0:
            n = selected_nodes.pop()    # pop last node
            for node in selected_nodes: # connect every other node with the popped node
                self.connect_nodes(n, node)
            n.click()  # deselect node

    # disconnect all nodes that were selected by user
    def disconnect_selected_nodes(self):
        selected_nodes = [node for node in self.nodes if node.is_selected()]    # get all selected nodes
        while len(selected_nodes) > 0:
            n = selected_nodes.pop()    # pop last node
            for node in selected_nodes: # disconnect every other node
                self.disconnect_nodes(n, node)
            n.click()   # deselect node

    # remove a single node (and all it's connections) from graph
    def remove_node(self, node):
        self.nodes.remove(node)
        self.node_count -= 1
        for neighbour in node.get_neighbours(): # remove node from all the neighbours' nodes lists
            neighbour.remove_neighbour(node)
        if node == self.start_node:
            self.start_node = None
        if node == self.end_node:
            self.end_node = None
        del node

    # draw the network with all its nodes and connections
    def draw(self, screen):
        for node in self.nodes:  # draw all connections first so they appear in background
            node.draw_connections(screen)
        for node in self.nodes:  # draw nodes on top
            node.draw(screen)