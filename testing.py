import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import heapq

# definisi graf
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

# informasi kendaraan
vehicles = {
    'car': 60,  
    'motorcycle': 40,
    'bicycle': 15,
    'walk': 5
}

# algoritma Dijkstra
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

# perhitungan THR
def calculate_thr(family_info):
    thr_data = {}
    for family, info in family_info.items():
        if info['pendapatan'] > 10_000_000 and info['anak'] > 0:
            thr_data[family] = info['anak'] * 50_000
        else:
            thr_data[family] = 0
    return thr_data

# jadwal kunjungan
def create_schedule(graph, route, family_info, vehicle_type):
    schedule = []
    current_time = 0  
    vehicle_speed = vehicles[vehicle_type] * 1000 / 60  

    for i, house in enumerate(route):
        travel_time = 0
        if i > 0:  
            distance = graph[route[i - 1]].get(house, 0)  
            travel_time = distance / vehicle_speed  

        visit_time = 30 if family_info[house]['level'] == 0 else 15 

        current_time += travel_time
        arrival_time = f"{int(current_time // 60):02}:{int(current_time % 60):02}"  
        current_time += visit_time

        schedule.append({
            'house': house,
            'arrival_time': arrival_time,
            'menu': family_info[house]['menu'],
            'total_time': current_time
        })

    return schedule

# Visualisasi rute pergi dan pulang
def plot_combined_route(graph, route, return_route):
    G = nx.DiGraph()  
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)
    
    pos = nx.spring_layout(G, seed=42)  
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=2000, font_size=10, font_weight="bold", arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), font_color='red')
    
    # jalur pergi dan pulang
    edges_in_route = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
    edges_in_return = [(return_route[i], return_route[i + 1]) for i in range(len(return_route) - 1)]
    
    # jalur pergi 
    nx.draw_networkx_edges(G, pos, edgelist=edges_in_route, edge_color='blue', width=2.5, style='solid', label="Rute Pergi")
    
    # jalur pulang
    nx.draw_networkx_edges(G, pos, edgelist=edges_in_return, edge_color='green', width=2.5, style='dashed', label="Rute Pulang")
    
    # Tambahkan garis manual untuk legenda
    legend_elements = [
        Line2D([0], [1], color='blue', lw=2.5, label="Rute Pergi"),
        Line2D([0], [1], color='green', lw=2.5, linestyle='dashed', label="Rute Pulang")
    ]
    plt.legend(handles=legend_elements, loc="upper left")
    
    plt.title("Rute Kunjungan Pergi dan Pulang", fontsize=16)
    plt.show()

# Input pengguna
vehicle_type = input("Masukkan jenis kendaraan (car/motorcycle/bicycle/walk): ").strip().lower()
start_node = input("Masukkan titik awal keberangkatan: ").strip()
end_node = input("Masukkan tujuan akhir keberangkatan: ").strip()

if start_node not in graph or end_node not in graph:
    print("Titik awal atau tujuan akhir tidak valid. Program dihentikan.")
else:
    # Algoritma Dijkstra untuk jalur pergi
    distances, paths = dijkstra(graph, start_node)
    route = [start_node] + paths[end_node]

    # Jalur pulang
    return_distances, return_paths = dijkstra(graph, end_node)
    return_route = [end_node] + return_paths[start_node]

    # Jadwal pergi
    schedule = create_schedule(graph, route, family_info, vehicle_type)

    # Jadwal pulang
    return_schedule = create_schedule(graph, return_route, family_info, vehicle_type)

    # THR
    thr_data = calculate_thr(family_info)

    # Output THR
    print("\nTHR Per Keluarga:")
    for family, thr in thr_data.items():
        print(f"{family}: Rp {thr:,}")

    # Jadwal pergi
    print("\nJadwal Kunjungan Pergi:")
    for visit in schedule:
        print(f"Rumah: {visit['house']}, Waktu Tiba: {visit['arrival_time']}, Menu: {visit['menu']}")
    print(f"Total waktu perjalanan pergi: {schedule[-1]['total_time']} menit")

    # Jadwal pulang
    print("\nJadwal Kunjungan Pulang:")
    for visit in return_schedule:
        print(f"Rumah: {visit['house']}, Waktu Tiba: {visit['arrival_time']}, Menu: {visit['menu']}")
    print(f"Total waktu perjalanan pulang: {return_schedule[-1]['total_time']} menit")

    # Plot rute gabungan
    plot_combined_route(graph, route, return_route)