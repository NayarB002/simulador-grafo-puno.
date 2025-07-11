import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from matplotlib.offsetbox import TextArea, AnnotationBbox

# 1. Lugares populares de Puno con coordenadas (lat, lon)
lugares = {
    'Plaza de Armas': (-15.840221, -70.021880),
    'Parque Pino': (-15.841800, -70.022000),
    'Terminal Terrestre': (-15.836800, -70.012900),
    'Terminal Zonal': (-15.836200, -70.014500),
    'Universidad Nacional del Altiplano (UNA)': (-15.827800, -70.021200),
    'Hospital Regional': (-15.841900, -70.018900),
    'Mirador Kuntur Wasi': (-15.832900, -70.025800),
    'Mercado Central': (-15.841000, -70.022800),
    'Puerto de Puno': (-15.840900, -70.028200),
    'Museo Carlos Dreyer': (-15.840000, -70.021400),
    'Estadio Torres Belón': (-15.842800, -70.025200),
    'Plaza San Juan': (-15.842200, -70.019800),
    'Plaza Zela': (-15.839200, -70.019200),
    'Parque Mariátegui': (-15.837900, -70.019900),
    'Plaza Vea': (-15.834900, -70.012200),
    'Iglesia San Juan Bautista': (-15.841600, -70.021100),
    'Real Plaza Puno': (-15.834000, -70.012000),
    'Parque Huajsapata': (-15.841000, -70.024800),
    'Colegio San Carlos': (-15.841400, -70.020800),
    'Terminal Zonal Juliaca': (-15.836000, -70.011000),
    'UANCV': (-15.827000, -70.017000)
}

# 2. Conexiones principales (simulando calles y rutas principales)
conexiones = [
    ('Plaza de Armas', 'Parque Pino'),
    ('Plaza de Armas', 'Mercado Central'),
    ('Plaza de Armas', 'Museo Carlos Dreyer'),
    ('Plaza de Armas', 'Iglesia San Juan Bautista'),
    ('Plaza de Armas', 'Parque Huajsapata'),
    ('Parque Pino', 'Mercado Central'),
    ('Parque Pino', 'Estadio Torres Belón'),
    ('Parque Pino', 'Plaza San Juan'),
    ('Mercado Central', 'Hospital Regional'),
    ('Mercado Central', 'Parque Huajsapata'),
    ('Museo Carlos Dreyer', 'Plaza Zela'),
    ('Plaza Zela', 'Parque Mariátegui'),
    ('Parque Mariátegui', 'Plaza Vea'),
    ('Plaza Vea', 'Terminal Terrestre'),
    ('Terminal Terrestre', 'Terminal Zonal'),
    ('Terminal Terrestre', 'Terminal Zonal Juliaca'),
    ('Terminal Terrestre', 'Real Plaza Puno'),
    ('Terminal Zonal', 'Real Plaza Puno'),
    ('Real Plaza Puno', 'UANCV'),
    ('UANCV', 'Universidad Nacional del Altiplano (UNA)'),
    ('Universidad Nacional del Altiplano (UNA)', 'Mirador Kuntur Wasi'),
    ('Mirador Kuntur Wasi', 'Puerto de Puno'),
    ('Puerto de Puno', 'Estadio Torres Belón'),
    ('Estadio Torres Belón', 'Parque Huajsapata'),
    ('Hospital Regional', 'Colegio San Carlos'),
    ('Colegio San Carlos', 'Iglesia San Juan Bautista'),
    ('Plaza San Juan', 'Hospital Regional'),
    ('Plaza San Juan', 'Plaza Zela'),
]

# 3. Construir el grafo con distancias geodésicas
G = nx.Graph()
for lugar, coord in lugares.items():
    G.add_node(lugar, pos=coord)
for a, b in conexiones:
    dist = geodesic(lugares[a], lugares[b]).meters
    G.add_edge(a, b, weight=dist)

print("\n=== SIMULADOR DE CAMINOS EN PUNO (SOLO PYTHON) ===\n")
lugares_ordenados = sorted(lugares.keys())
print("Lugares disponibles:")
for i, lugar in enumerate(lugares_ordenados, 1):
    print(f"  {i}. {lugar}")
def pedir_lugar(mensaje):
    while True:
        entrada = input(mensaje).strip()
        if entrada in lugares:
            return entrada
        else:
            print("[!] Nombre no válido. Intente de nuevo (respetando mayúsculas/minúsculas).\n")
origen = pedir_lugar("\nIngrese el nombre exacto del lugar de origen: ")
destino = pedir_lugar("Ingrese el nombre exacto del lugar de destino: ")

camino_corto = nx.shortest_path(G, source=origen, target=destino, weight='weight')
distancia_corta = nx.shortest_path_length(G, source=origen, target=destino, weight='weight')
all_paths = list(nx.all_simple_paths(G, source=origen, target=destino))
if all_paths:
    camino_largo = max(all_paths, key=lambda path: sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path)-1)))
    distancia_larga = sum(G[camino_largo[i]][camino_largo[i+1]]['weight'] for i in range(len(camino_largo)-1))
else:
    camino_largo = None
    distancia_larga = None

print("\n--- RESULTADOS ---\n")
velocidad_kmh = 5  # velocidad promedio caminando
velocidad_ms = velocidad_kmh * 1000 / 3600

tiempo_corto_horas = distancia_corta / 1000 / velocidad_kmh
minutos_corto = tiempo_corto_horas * 60
print(f"Camino más corto: {' → '.join(camino_corto)}\n  Distancia: {distancia_corta:.0f} metros\n  Tiempo estimado: {minutos_corto:.1f} min ({tiempo_corto_horas:.2f} h)")
if camino_largo and camino_largo != camino_corto:
    tiempo_largo_horas = distancia_larga / 1000 / velocidad_kmh
    minutos_largo = tiempo_largo_horas * 60
    print(f"Camino más largo: {' → '.join(camino_largo)}\n  Distancia: {distancia_larga:.0f} metros\n  Tiempo estimado: {minutos_largo:.1f} min ({tiempo_largo_horas:.2f} h)")
else:
    print("No existe un camino simple más largo distinto al más corto entre estos lugares.")

# Visualización profesional con matplotlib
def visualizar_grafo(G, camino_corto=None, camino_largo=None, origen=None, destino=None):
    import datetime
    pos = {n: (c[1], c[0]) for n, c in nx.get_node_attributes(G, 'pos').items()}
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
    ax.set_facecolor('white')
    nx.draw_networkx_nodes(G, pos, node_color='#e3f2fd', node_size=1100, edgecolors='#1565c0', linewidths=2, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', font_color='#0d47a1', ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='#bdbdbd', width=2, alpha=0.5, ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels_fmt = {k: f"{v:.0f}m" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_fmt, font_color='#616161', font_size=10, ax=ax, bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.7))
    if camino_corto:
        path_edges_corto = list(zip(camino_corto, camino_corto[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges_corto, edge_color='#e53935', width=4, arrows=True, arrowstyle='-|>', arrowsize=28, ax=ax, connectionstyle='arc3,rad=0.08')
        nx.draw_networkx_nodes(G, pos, nodelist=camino_corto, node_color='#ffcc80', node_size=1200, ax=ax, edgecolors='#e65100', linewidths=2)
    if camino_largo and camino_largo != camino_corto:
        path_edges_largo = list(zip(camino_largo, camino_largo[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges_largo, edge_color='#1e88e5', width=4, style='dashed', arrows=True, arrowstyle='-|>', arrowsize=28, ax=ax, connectionstyle='arc3,rad=0.08')
        nx.draw_networkx_nodes(G, pos, nodelist=camino_largo, node_color='#b3e5fc', node_size=1200, ax=ax, edgecolors='#0288d1', linewidths=2)
    if origen:
        nx.draw_networkx_nodes(G, pos, nodelist=[origen], node_color='#43a047', node_size=1400, ax=ax, edgecolors='#1b5e20', linewidths=3)
    if destino:
        nx.draw_networkx_nodes(G, pos, nodelist=[destino], node_color='#8e24aa', node_size=1400, ax=ax, edgecolors='#4a148c', linewidths=3)
    # Título profesional
    plt.suptitle(f"Simulación de Rutas entre Escuelas\nOrigen: {origen}   →   Destino: {destino}", fontsize=20, fontweight='bold', color='#263238', y=0.97)
    # Texto adicional en la gráfica
    plt.text(0.5, 1.04, f"Ruta: {origen} → {destino}", fontsize=15, ha='center', va='center', transform=ax.transAxes, color='#263238', bbox=dict(facecolor='white', alpha=0.8, edgecolor='#bdbdbd'))
    # Distancia y tiempo estimado
    velocidad_kmh = 5
    if camino_corto:
        distancia_corta = sum(G[camino_corto[i]][camino_corto[i+1]]['weight'] for i in range(len(camino_corto)-1))
        tiempo_corto_horas = distancia_corta / 1000 / velocidad_kmh
        minutos_corto = tiempo_corto_horas * 60
        texto_corto = f"Más corto: {distancia_corta:.0f} m, {minutos_corto:.1f} min ({tiempo_corto_horas:.2f} h)"
    else:
        texto_corto = ""
    if camino_largo and camino_largo != camino_corto:
        distancia_larga = sum(G[camino_largo[i]][camino_largo[i+1]]['weight'] for i in range(len(camino_largo)-1))
        tiempo_largo_horas = distancia_larga / 1000 / velocidad_kmh
        minutos_largo = tiempo_largo_horas * 60
        texto_largo = f"Más largo: {distancia_larga:.0f} m, {minutos_largo:.1f} min ({tiempo_largo_horas:.2f} h)"
    else:
        texto_largo = "No existe un camino simple más largo distinto al más corto."
    # Crear el texto de información
    info_text = f"{texto_corto}\n{texto_largo}"
    text_area = TextArea(info_text, textprops=dict(color='#37474f', fontsize=13, fontweight='normal', bbox=dict(facecolor='white', alpha=0.8, edgecolor='#bdbdbd')))
    ab = AnnotationBbox(text_area, (0.98, 0.98), xycoords='axes fraction', box_alignment=(1,1), frameon=False)
    ax.add_artist(ab)
    ab.draggable()
    import matplotlib.patches as mpatches
    legend_elements = [
        mpatches.Patch(color='#ffcc80', label='Lugares en el trayecto más corto.'),
        mpatches.Patch(color='#e53935', label='Rutas del trayecto más corto.'),
        mpatches.Patch(color='#b3e5fc', label='Lugares en el trayecto más largo.'),
        mpatches.Patch(color='#1e88e5', label='Rutas del trayecto más largo.'),
        mpatches.Patch(color='#43a047', label='Origen: Lugar de inicio.'),
        mpatches.Patch(color='#8e24aa', label='Destino: Lugar de destino.')
    ]
    leg = plt.legend(handles=legend_elements, loc='upper left', fontsize=11, title='Leyenda de colores', title_fontsize=13, frameon=True, fancybox=True, borderpad=1)
    leg.set_draggable(True)
    fecha = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    plt.figtext(0.5, 0.01, f"Simulador de Caminos - UNA Puno | Generado: {fecha}", ha='center', fontsize=10, color='#607d8b', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    plt.axis('off')
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()

visualizar_grafo(G, camino_corto, camino_largo, origen, destino) 