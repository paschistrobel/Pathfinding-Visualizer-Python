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
        self.successful = False
        self.previous_node = None

    def has_finished(self):
        return self.finished

    def was_successful(self):
        return self.successful

    def step(self):  # returns w
        if len(self.queue) > 0:
            curr_node = self.queue.pop(0)  # FIFO principal

            if self.previous_node is not None:
                if self.previous_node in self.prev:
                    self.previous_node.visited_from(self.prev[self.previous_node])
                else:
                    self.previous_node.visited_from(None)

            # mark current node as the inspected one (as well as it's previous connection if there is one)
            if curr_node in self.prev:
                curr_node.inspected_from(self.prev[curr_node])
            else:
                curr_node.inspected_from(None)

            if curr_node.is_end_node():  # target found
                self.reconstruct_path()
                self.finished = True  # algorithm finished
            else:
                neighbours = curr_node.get_neighbours()
                for neighbour in neighbours:
                    if not neighbour.already_visited():  # check if neighbour was already visited
                        self.queue.append(neighbour)
                        neighbour.enqueued_from(curr_node)
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
