import heapq
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Definisi graf
graph = {
    'Buyut Sutarji': {'Kakek Jais': 10, 'Kakek Suwito': 15},
    'Kakek Jais': {'Pak Joko': 5, 'Pak Toni': 12},
    'Kakek Suwito': {'Bu Ani': 30, 'Pak Budi': 20},
    'Pak Joko': {'Mbah Painem': 25},
    'Pak Toni': {'Mbah Sutini': 10},
    'Bu Ani': {'Pakde Sunaryo': 12},
    'Pak Budi': {'Pakde Sunaryo': 9},
    'Mbah Painem': {},
    'Mbah Sutini': {},
    'Pakde Sunaryo': {}
}

# Informasi kendaraan
vehicles = {
    'mobil': 30,
    'motor': 15,
    'sepeda': 40,
    'jalan': 60
}

# Algoritma Dijkstra
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    path = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                path[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, path

# Rute terpendek
def shortest_path(path, start, end):
    route = []
    current = end
    while current is not None:
        route.append(current)
        current = path[current]
    return route[::-1]

def plot_graph(graph, shortest_route=None, start_node=None, end_node=None):
    G = nx.DiGraph()
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.shell_layout(G)

    # Plot graf
    plt.figure(figsize=(14, 10))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight="bold", arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), font_color='red')

    if shortest_route:
        route_edges = list(zip(shortest_route, shortest_route[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color='green', width=3)

    # titik awal dan titik tujuan
    if start_node:
        nx.draw_networkx_nodes(G, pos, nodelist=[start_node], node_color='yellow', node_size=500, label="Titik Awal")
    if end_node:
        nx.draw_networkx_nodes(G, pos, nodelist=[end_node], node_color='red', node_size=500, label="Titik Tujuan")

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=10, label='Titik Awal'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Titik Tujuan'),
        Line2D([0], [0], color='green', lw=3, label='Rute Terdekat')
    ]
    plt.legend(handles=legend_elements, loc='upper left')

    plt.title("Graf Perjalanan Keluarga (Rute Terdekat)", fontsize=16)
    plt.show()

def interactive_travel(graph, vehicle_type, start_node):
    current_node = start_node

    print(f"\nMemulai perjalanan dari: {current_node}")
    print("\nRute terdekat ke semua titik dihitung terlebih dahulu.\n")
    distances, path = dijkstra(graph, current_node)
    
    plot_graph(graph, start_node=current_node)

    while True:
        print(f"\nAnda sekarang di: {current_node}")
        print("Apakah Anda ingin:")
        print("1. Melanjutkan perjalanan")
        print("2. Pulang")
        choice = input("Masukkan pilihan Anda (1/2): ").strip()

        if choice == "1":
            print("Pilih tujuan berikut:")
            neighbors = graph[current_node]
            for i, neighbor in enumerate(neighbors.keys(), start=1):
                print(f"{i}. {neighbor}")

            try:
                next_choice = int(input("Masukkan nomor tujuan: ").strip())
                next_node = list(neighbors.keys())[next_choice - 1]
            except (ValueError, IndexError):
                print("Pilihan tidak valid. Silakan coba lagi.")
                continue

            # rute ke tujuan berikutnya
            distances, path = dijkstra(graph, current_node)
            shortest_route = shortest_path(path, current_node, next_node)
            print(f"Rute ke {next_node}: {' -> '.join(shortest_route)}")
            plot_graph(graph, shortest_route, current_node, next_node)

            current_node = next_node

        elif choice == "2":
            print("Anda memilih pulang.")
            print("Pilih titik akhir pulang dari daftar berikut:")
            for i, node in enumerate(graph.keys(), start=1):
                print(f"{i}. {node}")

            try:
                end_choice = int(input("Masukkan nomor titik akhir pulang: ").strip())
                end_node = list(graph.keys())[end_choice - 1]
            except (ValueError, IndexError):
                print("Pilihan tidak valid. Program dihentikan.")
                break

            # rute pulang
            print(f"Menentukan rute pulang dari {current_node} ke {end_node}...")
            distances, path = dijkstra(graph, current_node)
            shortest_route = shortest_path(path, current_node, end_node)

            print(f"Rute pulang: {' -> '.join(shortest_route)}")
            plot_graph(graph, shortest_route, start_node, end_node)
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Input kendaraan dan titik awal
vehicle_type = input("Masukkan jenis kendaraan (mobil/motor/sepeda/jalan): ").strip().lower()
start_node = input("Masukkan titik awal keberangkatan: ").strip()

# Validasi input
if start_node not in graph:
    print("Titik awal tidak valid. Program dihentikan.")
else:
    interactive_travel(graph, vehicle_type, start_node)
