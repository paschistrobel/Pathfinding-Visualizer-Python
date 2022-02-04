class BreadthFirst:
    def __init__(self, graph, start, end):
        self.graph = graph
        self.start_node = start
        self.end_node = end
        self.queue = []
        self.prev = {node: None for node in
                     self.graph.get_nodes()}  # dict for keeping track of what the previous node of a node was
        self.queue.append(self.start_node)  # add start node to queue
        self.finished = False
        self.previous_node = None

    def has_finished(self):
        return self.finished

    def step(self):
        if len(self.queue) > 0:
            curr_node = self.queue.pop(0)  # FIFO principal

            # mark the node and its incoming connection from previous step as visited
            if self.previous_node is not None:
                self.previous_node.visited_from(self.prev[self.previous_node])

            # mark current node as the inspected one (as well as its incoming connection if there is one)
            curr_node.inspected_from(self.prev[curr_node])

            if curr_node.is_end_node():  # target found
                self.reconstruct_path()
                self.finished = True  # algorithm finished
                return
            for neighbour in curr_node.get_neighbours():

                if not neighbour.already_visited():  # check if neighbour was already visited
                    self.queue.append(neighbour)
                    neighbour.enqueued_from(curr_node)  # mark the current node and its incoming connection as "is on waitlist"
                    self.prev[neighbour] = curr_node
            self.previous_node = curr_node
        else:  # no nodes in queue left and target was not found --> start and end not connected
            self.finished = True  # algorithm finished but not successful
            print("\nSTART AND END NODE ARE NOT CONNECTED --> NO PATH CAN BE FOUND")

    def reconstruct_path(self):
        path = []
        curr_node = self.end_node
        while curr_node is not None:
            path.append(curr_node)
            curr_node = self.prev[curr_node]
        path.reverse()
        self.graph.highlight_final_path(path)
        print("PATH FOUND AND HIGHLIGHTED")


class DepthFirst:
    def __init__(self, graph, start, end):
        self.graph = graph
        self.start_node = start
        self.end_node = end
        self.stack = []
        self.stack.append(self.start_node)
        self.finished = False
        self.prev = {node: None for node in self.graph.get_nodes()}
        self.previous_node = None

    def has_finished(self):
        return self.finished

    def step(self):
        if len(self.stack) > 0: # check if there are nodes left to check
            curr_node = self.stack.pop()

            if self.previous_node is not None:
                self.previous_node.visited_from(self.prev[self.previous_node])

            curr_node.inspected_from(self.prev[curr_node])

            if curr_node.is_end_node():
                self.reconstruct_path()
                self.finished = True
                return
            for neighbour in curr_node.get_neighbours():
                if not neighbour.already_visited():
                    self.stack.append(neighbour)
                    neighbour.enqueued_from(curr_node)
                    self.prev[neighbour] = curr_node
            self.previous_node = curr_node
        else:
            self.finished = True
            print("\nSTART AND END NODE ARE NOT CONNECTED --> NO PATH CAN BE FOUND")

    def reconstruct_path(self):
        path = []
        curr_node = self.end_node
        while curr_node is not None:
            path.append(curr_node)
            curr_node = self.prev[curr_node]
        path.reverse()
        self.graph.highlight_final_path(path)
        print("PATH FOUND AND HIGHLIGHTED")