import networkx as nx
import matplotlib.pyplot as plt
from netgraph import Graph
import json


def build_graph(data):
    G = nx.Graph()

    # Create dictionaries to map device and interface IDs to their properties
    device_id_to_hostname = {device['deviceID']: device['hostname'] for device in data['devices']}
    interface_to_device = {interface['interfaceID']: interface['deviceID'] for interface in data['interfaces']}
    interface_id_to_ip = {interface['interfaceID']: interface['ipAddress'] for interface in data['interfaces']}

    # Add nodes (devices) to the graph
    for device in data['devices']:
        G.add_node(device['hostname'], **device)

    # Add edges (links) to the graph
    for link in data['links']:
        try:
            source_device = device_id_to_hostname[interface_to_device[link["sourceInterfaceID"]]]
            dest_device = device_id_to_hostname[interface_to_device[link["destinationInterfaceID"]]]
            G.add_edge(source_device, dest_device, **link)
        except KeyError as e:
            print(f"Error: {e} not found. Check if all interfaces in links are correctly defined in the interfaces section.")

    return G


def display(G):
    pos = nx.spring_layout(G)

    fig = plt.figure(1, figsize=(20, 19), dpi=140)

    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='red', node_size=1000, width=3, font_size=20)
    edge_weight = nx.get_edge_attributes(G, 'bandwidth')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weight, font_weight='bold', font_size=11.5)

    plt.show()


def display_highlight(G, a, b):
    pos = nx.spring_layout(G)

    fig = plt.figure(1, figsize=(25, 24), dpi=140)

    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=1000, width=3, font_size=19)
    edge_weight = nx.get_edge_attributes(G, 'bandwidth')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weight, font_weight='bold', font_size=11.5)
    plot_instance = Graph(G,
                          node_layout=pos,
                          node_size=1,
                          node_edge_width=0.01,
                          edge_width=0.1
                          )

    path = nx.shortest_path(G, a, b, weight='bandwidth')
    print('shortest_path:', path)

    for node in path:
        plot_instance.node_artists[node].radius = 2. * 1e-2
        plot_instance.node_artists[node].set_color('blue')

    for ii, node_1 in enumerate(path[:-1]):
        node_2 = path[ii + 1]
        if (node_1, node_2) in plot_instance.edges:
            edge = (node_1, node_2)
        else:  # the edge is specified in reverse node order
            edge = (node_2, node_1)
        plot_instance.edge_artists[edge].update_width(.55 * 1e-2)
        plot_instance.edge_artists[edge].set_color('green')
        plot_instance.edge_artists[edge].set_alpha(1)

    plt.show()


# Load input data
with open('input_file.json') as f:
    input_data = json.load(f)

# Build the graph from the input data
G = build_graph(input_data)

# Display the full network topology
print('map')
display(G)

# List of nodes (device hostnames) in the graph
node_list = [device['hostname'] for device in input_data['devices']]
print('list of place in the map')
print('\n')
print(node_list)

# Input source and destination nodes for highlighting the shortest path
a = input('enter the from location: ')
b = input('enter the to location: ')
display_highlight(G, a, b)
