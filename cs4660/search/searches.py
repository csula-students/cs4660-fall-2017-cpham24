"""
Searches module defines all different search algorithms
"""
from Queue import PriorityQueue

def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    distance_of = {}
    parent_of = {}
    edge_to = {}

    q = PriorityQueue()
    q.put((0, initial_node));

    distance_of[initial_node] = 0

    while not q.empty():
        u = q.get()[1]

        for node in graph.neighbors(u):
            if node not in distance_of:
                edge_to[node] = graph.distance(u, node)
                distance_of[node] = distance_of[u] + edge_to[node].weight
                parent_of[node] = u

                # continue to enqueue if we haven't reached the end
                if node != dest_node:
                    q.put((distance_of[node], node))

    # actions is a list of edges
    actions = []
    end_node = dest_node

    while end_node in parent_of:
        actions.append(edge_to[end_node])
        end_node = parent_of[end_node]

    # reverse the list of edges
    actions.reverse()

    return actions

def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """

    # search all children
    for node in graph.neighbors(initial_node):
        if node == dest_node:
            # if we found our destination, just return it!
            return [graph.distance(initial_node, dest_node)]
        else:
            # call dfs recursively and return path if not empty
            paths = dfs(graph, node, dest_node)
            if paths != []:
                actions = [graph.distance(initial_node, node)]
                actions.extend(paths)
                return actions
    return []

def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    distance_of = {}
    previous_of = {}
    edge_to = {}

    distance_of[initial_node] = 0

    q = []
    q.append((0, initial_node))

    while q != []:
        u = q.pop()[1]

        for v in graph.neighbors(u):
            edge = graph.distance(u, v)
            alt = distance_of[u] + edge.weight

            if v not in distance_of or alt < distance_of[v]:
                # reassign priority
                if v in distance_of:
                    q.remove((distance_of[v], v))
                # enqueue v for further evaluations
                q.append((alt, v))

                distance_of[v] = alt
                previous_of[v] = u
                edge_to[v] = edge

        # sort priority
        q.sort(reverse=True)
    
    actions = []
    current_node = dest_node

    while current_node in previous_of:
        actions.append(edge_to[current_node])
        current_node = previous_of[current_node]

    actions.reverse()

    return actions


def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    pass
