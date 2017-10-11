"""
Searches module defines all different search algorithms
"""
import math

def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    distance_of = {}
    parent_of = {}
    edge_to = {}

    q = []
    q.append((0, initial_node));

    distance_of[initial_node] = 0

    while len(q) > 0:
        u = q.pop()[1]

        for node in graph.neighbors(u):
            if node not in distance_of:
                edge_to[node] = graph.distance(u, node)
                distance_of[node] = distance_of[u] + edge_to[node].weight
                parent_of[node] = u

                # continue to enqueue if we haven't reached the end
                if node != dest_node:
                    q.append((distance_of[node], node))

        # sort priority
        q = sorted(q, key=lambda x:x[0])
        q.reverse()

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

    while len(q) > 0:
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
        q = sorted(q, key=lambda x:x[0])
        q.reverse()
    
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
    #print("finding %s to %s" % (initial_node, dest_node))
    explored_set = []
    unexplored_set = [(0, initial_node)]
    parent_of = {}
    edge_of = {}

    gScore = {}
    gScore[initial_node] = 0

    fScore = {}
    fScore[initial_node] = heuristic(initial_node, dest_node)

    while len(unexplored_set) > 0:
        u = unexplored_set.pop()[1]
        #print("explored %i nodes, currently %s" % (len(explored_set) + 1, u))

        # if we found the end node
        if u == dest_node:
            #print("\nu is actually the destination! reconstructing path...")
            current_node = u
            actions = []
            while current_node in parent_of:
                actions.append(edge_of[current_node])
                current_node = parent_of[current_node]
            actions.reverse()
            return actions

        explored_set.append(u)

        for node in graph.neighbors(u):
            if node not in explored_set:
                edge = graph.distance(u, node)
                tempGScore = gScore[u] + edge.weight
                if node not in gScore:
                    unexplored_set.append((float('inf'), node))
                    gScore[node] = float('inf')
                    fScore[node] = float('inf')
                if tempGScore < gScore[node]:
                    unexplored_set.remove((fScore[node], node))

                    parent_of[node] = u
                    edge_of[node] = edge

                    gScore[node] = tempGScore
                    fScore[node] = tempGScore + heuristic(node, dest_node)
                    unexplored_set.append((fScore[node], node))

        # sort the priority queue
        unexplored_set = sorted(unexplored_set, key=lambda x:x[0])
        unexplored_set.reverse()
    return []

def heuristic(node, goal):
    dx = node.data.x - goal.data.x
    dy = node.data.y - goal.data.y
    return 2*math.sqrt(dx * dx + dy * dy)