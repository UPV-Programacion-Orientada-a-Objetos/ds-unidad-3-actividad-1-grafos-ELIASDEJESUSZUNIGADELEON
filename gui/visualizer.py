"""
Módulo de visualización de grafos usando NetworkX
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')


class VisualizadorGrafo:
    """Clase para visualizar grafos usando NetworkX"""
    
    def __init__(self, canvas_frame):
        """
        Inicializa el visualizador
        
        Args:
            canvas_frame: Frame de Tkinter donde se dibujará el grafo
        """
        self.canvas_frame = canvas_frame
        self.figura = None
        self.canvas = None
    
    def visualizar_subgrafo(self, nodos_niveles, aristas, titulo="Subgrafo"):
        """
        Visualiza un subgrafo resultante de BFS/DFS
        
        Args:
            nodos_niveles: Lista de tuplas (nodo, nivel) o lista de nodos
            aristas: Lista de tuplas (origen, destino)
            titulo: Título del gráfico
        """
        # Limpiar visualización anterior
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        # Crear grafo dirigido
        G = nx.DiGraph()
        
        # Determinar si tenemos información de niveles
        tiene_niveles = isinstance(nodos_niveles[0], tuple)
        
        if tiene_niveles:
            # Extraer nodos y niveles
            nodos = [n for n, _ in nodos_niveles]
            niveles = {n: nivel for n, nivel in nodos_niveles}
        else:
            nodos = nodos_niveles
            niveles = None
        
        # Agregar nodos
        G.add_nodes_from(nodos)
        
        # Agregar solo las aristas que conectan nodos en el subgrafo
        aristas_subgrafo = [(o, d) for o, d in aristas if o in nodos and d in nodos]
        G.add_edges_from(aristas_subgrafo)
        
        # Crear figura
        self.figura = plt.Figure(figsize=(8, 6), dpi=100)
        ax = self.figura.add_subplot(111)
        
        # Elegir layout según tamaño del grafo
        if len(nodos) < 50:
            pos = nx.spring_layout(G, k=1, iterations=50)
        elif len(nodos) < 200:
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.circular_layout(G)
        
        # Colorear nodos según nivel (si disponible)
        if niveles:
            max_nivel = max(niveles.values())
            colores = [niveles[n] / max(max_nivel, 1) for n in G.nodes()]
            cmap = plt.cm.viridis
        else:
            colores = 'lightblue'
            cmap = None
        
        # Dibujar grafo
        nx.draw_networkx_nodes(
            G, pos, 
            node_color=colores,
            node_size=300,
            cmap=cmap,
            ax=ax
        )
        
        nx.draw_networkx_edges(
            G, pos,
            edge_color='gray',
            arrows=True,
            arrowsize=10,
            ax=ax,
            alpha=0.5
        )
        
        # Etiquetas de nodos (solo si no son demasiados)
        if len(nodos) < 100:
            nx.draw_networkx_labels(
                G, pos,
                font_size=8,
                font_weight='bold',
                ax=ax
            )
        
        ax.set_title(titulo, fontsize=12, fontweight='bold')
        ax.axis('off')
        
        # Agregar leyenda si hay niveles
        if niveles:
            sm = plt.cm.ScalarMappable(
                cmap=cmap,
                norm=plt.Normalize(vmin=0, vmax=max_nivel)
            )
            sm.set_array([])
            cbar = self.figura.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
            cbar.set_label('Nivel/Profundidad', rotation=270, labelpad=15)
        
        # Crear canvas de Tkinter
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def limpiar(self):
        """Limpia la visualización actual"""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        if self.figura:
            plt.close(self.figura)
            self.figura = None
