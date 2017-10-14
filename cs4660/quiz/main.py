"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
import codecs

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.

    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urlopen(req, jsondataasbytes)
    reader = codecs.getreader('utf-8')
    return json.load(reader(response))

def bfs(init_id, dest_id):
    """
    Breadth First Search
    queries the game to do search from the init_id to dest_id
    returns a list of actions going from the init_id to dest_id
    """
    distance_of = {}
    parent_of = {}
    edge_to = {}

    q = []
    q.append((0, init_id));

    distance_of[init_id] = 0

    while len(q) > 0:
        u = get_state(q.pop()[1])
        neighbors = u['neighbors']

        for i in range(len(neighbors)):
            v = neighbors[i]
            if v['id'] not in distance_of:
                edge = transition_state(u['id'], v['id'])
                edge_to[v['id']] = edge
                distance_of[v['id']] = distance_of[u['id']] + 1
                parent_of[v['id']] = u['id']

                # continue to enqueue if we haven't reached the end
                if v['id'] != dest_id:
                    q.append((distance_of[v['id']], v['id']))

        # sort priority
        q = sorted(q, key=lambda x:x[0])
        q.reverse()

    # actions is a list of edges
    actions = []
    node_id = dest_id

    while node_id in parent_of:
        actions.append(edge_to[node_id])
        node_id = parent_of[node_id]

    # reverse the list of edges
    actions.reverse()

    return actions

def dijkstra(init_id, dest_id):
    """
    Dijkstra Search
    queries the game to do search from the init_node to dest_node
    returns a list of actions going from the init_node to dest_node
    """
    distance_of = {}
    previous_of = {}
    edge_to = {}

    distance_of[init_id] = 0

    q = []
    q.append((0, init_id))
    visited = []

    while len(q) > 0:
        u = get_state(q.pop()[1])
        visited.append(u['id'])
        neighbors = u['neighbors']

        for i in range(len(neighbors)):
            v = neighbors[i]
            edge = transition_state(u['id'], v['id'])
            alt = distance_of[u['id']] + edge['event']['effect']

            if v['id'] not in visited and (v['id'] not in distance_of or alt > distance_of[v['id']]):
                # reassign priority
                if v['id'] in distance_of:
                    q.remove((distance_of[v['id']], v['id']))
                # enqueue v for further evaluations
                q.append((alt, v['id']))

                distance_of[v['id']] = alt
                previous_of[v['id']] = u['id']
                edge_to[v['id']] = edge

        # sort priority
        q = sorted(q, key=lambda x:x[0])
    
    actions = []
    node_id = dest_id

    while node_id in previous_of:
        actions.append(edge_to[node_id])
        node_id = previous_of[node_id]

    actions.reverse()

    return actions

def print_actions(actions, init_id):
    prev_id = init_id
    total = 0
    for i in range(len(actions)):
        prev_node = get_state(prev_id)
        next_id = actions[i]['id']
        total += actions[i]['event']['effect']
        print("%s(%s):%s(%s):%i" % (prev_node['location']['name'], prev_id, actions[i]['action'], actions[i]['id'], actions[i]['event']['effect']))
        prev_id = next_id
    print("\nTotal HP: %i" % total)

if __name__ == "__main__":
    # Your code starts here
    #empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    #print(empty_room)
    #print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id']))
    init_id = '7f3dc077574c013d98b2de8f735058b4'
    dest_id = 'f1f131f647621a4be7c71292e79613f9'
    
    actions = bfs(init_id, dest_id)
    print("\nBFS Path:")
    print_actions(actions, init_id)

    actions = dijkstra(init_id, dest_id)
    print("\nDijkstra Path:")
    print_actions(actions, init_id)
