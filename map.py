import networkx as nx
import matplotlib.pyplot as plt
import heapq

# definisi
graph = {
    'Buyut Sutarji': {'Kakek Jais': 10, 'Kakek Suwito': 15},
    'Kakek Jais': {'Pak Joko': 5, 'Pak Toni': 12},
    'Kakek Suwito': {'Bu Ani': 8, 'Pak Budi': 20},
    'Pak Joko': {'Mbah Painem': 7},
    'Pak Toni': {'Mbah Sutini': 10},
    'Bu Ani': {'Pakde Sunaryo': 12},
    'Pak Budi': {'Pakde Sunaryo': 9},
    'Mbah Painem': {},
    'Mbah Sutini': {},
    'Pakde Sunaryo': {}
}

# informasi keluarga
family_info = {
    'Buyut Sutarji': {'level': 0, 'menu': 'Nasi Tumpeng', 'pendapatan': 12_000_000, 'anak': 3},
    'Kakek Jais': {'level': 1, 'menu': 'Soto Ayam', 'pendapatan': 10_000_000, 'anak': 1},
    'Kakek Suwito': {'level': 1, 'menu': 'Gudeg', 'pendapatan': 14_000_000, 'anak': 2},
    'Pak Joko': {'level': 2, 'menu': 'Rawon', 'pendapatan': 8_000_000, 'anak': 2},
    'Pak Toni': {'level': 2, 'menu': 'Sate', 'pendapatan': 12_000_000, 'anak': 0},
    'Bu Ani': {'level': 2, 'menu': 'Lontong Sayur', 'pendapatan': 15_000_000, 'anak': 1},
    'Pak Budi': {'level': 2, 'menu': 'Bakso', 'pendapatan': 9_000_000, 'anak': 0},
    'Mbah Painem': {'level': 3, 'menu': 'Soto Ayam', 'pendapatan': 8_000_000, 'anak': 0},
    'Mbah Sutini': {'level': 3, 'menu': 'Nasi Tumpeng', 'pendapatan': 15_000_000, 'anak': 1},
    'Pakde Sunaryo': {'level': 3, 'menu': 'Gado-Gado', 'pendapatan': 5_000_000, 'anak': 0}
}

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    path = {node: [] for node in graph}
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                path[neighbor] = path[current_node] + [neighbor]
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances, path

def calculate_thr(family_info):
    thr_data = {}
    for family, info in family_info.items():
        if info['pendapatan'] > 10_000_000 and info['anak'] > 0:
            thr_data[family] = info['anak'] * 50_000
        else:
            thr_data[family] = 0
    return thr_data

def create_schedule(graph, route, family_info):
    schedule = []
    current_time = 0  
    
    for i, house in enumerate(route):
        travel_time = graph[route[i - 1]].get(house, 0) if i > 0 else 0
        visit_time = 30 if family_info[house]['level'] == 0 else 15
        
        current_time += travel_time
        arrival_time = f"{current_time // 60:02}:{current_time % 60:02}" 
        current_time += visit_time
        
        schedule.append({
            'house': house,
            'arrival_time': arrival_time,
            'menu': family_info[house]['menu']
        })
    
    return schedule

def plot_route(graph, route):
    G = nx.DiGraph()  
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)
    
    pos = nx.spring_layout(G, seed=42) 
    
    color_map = ['skyblue' if node in route else 'lightgray' for node in G.nodes]
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=2000, font_size=10, font_weight="bold", arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), font_color='red')
    
    edges_in_route = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=edges_in_route, edge_color='blue', width=2.5)
    
    plt.title("Rute Kunjungan Keluarga", fontsize=16)
    plt.show()

start_node = 'Buyut Sutarji'
distances, paths = dijkstra(graph, start_node)
route = [start_node] + paths[max(paths, key=lambda k: distances[k])]
thr_data = calculate_thr(family_info)
schedule = create_schedule(graph, route, family_info)

print("THR Per Keluarga:")
for family, thr in thr_data.items():
    print(f"{family}: Rp {thr:,}")

print("\nJadwal Kunjungan:")
for visit in schedule:
    print(f"Rumah: {visit['house']}, Waktu Tiba: {visit['arrival_time']}, Menu: {visit['menu']}")

plot_route(graph, route)


#kendaraan dan kecepatan 
#titik awal 
# jenis kendaraan
# akumulasi waktu
# jalur pulang