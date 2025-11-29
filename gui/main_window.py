"""
NeuroNet - Interfaz Gráfica Principal
Sistema de Análisis y Visualización de Grafos Masivos
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sys
import os
import time

# Agregar el directorio raíz al path para importar el módulo compilado
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from grafo_wrapper import PyGrafoDisperso
    MODULO_DISPONIBLE = True
except ImportError:
    MODULO_DISPONIBLE = False
    print("ADVERTENCIA: Módulo grafo_wrapper no encontrado. Compile primero con: python setup.py build_ext --inplace")

from gui.visualizer import VisualizadorGrafo


class NeuroNetGUI:
    """Interfaz gráfica principal de NeuroNet"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet - Análisis de Grafos Masivos")
        self.root.geometry("1200x800")
        
        # Instancia del grafo (None hasta que se cargue)
        self.grafo = None
        self.archivo_actual = None
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Verificar que el módulo esté disponible
        if not MODULO_DISPONIBLE:
            self.log_mensaje("ERROR: Módulo C++ no compilado. Ejecute: python setup.py build_ext --inplace", "error")
            messagebox.showerror(
                "Módulo no compilado",
                "El módulo C++ no está compilado.\n\n"
                "Por favor ejecute:\n"
                "python setup.py build_ext --inplace"
            )
    
    def configurar_estilo(self):
        """Configura el estilo visual de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores
        style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Segoe UI', 10, 'bold'), foreground='#34495e')
        style.configure('Info.TLabel', font=('Segoe UI', 9), foreground='#7f8c8d')
        style.configure('Success.TLabel', font=('Segoe UI', 9), foreground='#27ae60')
        style.configure('Error.TLabel', font=('Segoe UI', 9), foreground='#e74c3c')
    
    def crear_interfaz(self):
        """Crea todos los componentes de la interfaz"""
        
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar expansión
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # === SECCIÓN 1: TÍTULO ===
        titulo_frame = ttk.Frame(main_frame)
        titulo_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(
            titulo_frame,
            text="🧠 NeuroNet - Análisis de Grafos Masivos",
            style='Title.TLabel'
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            titulo_frame,
            text="Backend C++ | Interfaz Python",
            style='Info.TLabel'
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # === SECCIÓN 2: PANEL DE CONTROL (IZQUIERDA) ===
        control_frame = ttk.LabelFrame(main_frame, text="Panel de Control", padding="10")
        control_frame.grid(row=1, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Botón cargar archivo
        ttk.Button(
            control_frame,
            text="📁 Cargar Dataset",
            command=self.cargar_archivo,
            width=25
        ).pack(pady=5, fill=tk.X)
        
        # Información del grafo
        info_frame = ttk.LabelFrame(control_frame, text="Información del Grafo", padding="10")
        info_frame.pack(pady=10, fill=tk.X)
        
        self.lbl_archivo = ttk.Label(info_frame, text="Archivo: Ninguno", style='Info.TLabel')
        self.lbl_archivo.pack(anchor=tk.W)
        
        self.lbl_nodos = ttk.Label(info_frame, text="Nodos: 0", style='Info.TLabel')
        self.lbl_nodos.pack(anchor=tk.W)
        
        self.lbl_aristas = ttk.Label(info_frame, text="Aristas: 0", style='Info.TLabel')
        self.lbl_aristas.pack(anchor=tk.W)
        
        self.lbl_memoria = ttk.Label(info_frame, text="Memoria: 0 MB", style='Info.TLabel')
        self.lbl_memoria.pack(anchor=tk.W)
        
        self.lbl_mayor_grado = ttk.Label(info_frame, text="Mayor grado: -", style='Info.TLabel')
        self.lbl_mayor_grado.pack(anchor=tk.W)
        
        # Controles de algoritmos
        algo_frame = ttk.LabelFrame(control_frame, text="Algoritmos de Búsqueda", padding="10")
        algo_frame.pack(pady=10, fill=tk.X)
        
        # BFS
        ttk.Label(algo_frame, text="BFS - Nodo Inicio:", style='Info.TLabel').pack(anchor=tk.W)
        self.entry_bfs_nodo = ttk.Entry(algo_frame, width=15)
        self.entry_bfs_nodo.pack(fill=tk.X, pady=(0, 5))
        self.entry_bfs_nodo.insert(0, "0")
        
        ttk.Label(algo_frame, text="Profundidad Máxima:", style='Info.TLabel').pack(anchor=tk.W)
        self.entry_bfs_prof = ttk.Entry(algo_frame, width=15)
        self.entry_bfs_prof.pack(fill=tk.X, pady=(0, 5))
        self.entry_bfs_prof.insert(0, "2")
        
        ttk.Button(
            algo_frame,
            text="▶ Ejecutar BFS",
            command=self.ejecutar_bfs
        ).pack(fill=tk.X, pady=5)
        
        ttk.Separator(algo_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # DFS
        ttk.Label(algo_frame, text="DFS - Nodo Inicio:", style='Info.TLabel').pack(anchor=tk.W)
        self.entry_dfs_nodo = ttk.Entry(algo_frame, width=15)
        self.entry_dfs_nodo.pack(fill=tk.X, pady=(0, 5))
        self.entry_dfs_nodo.insert(0, "0")
        
        ttk.Button(
            algo_frame,
            text="▶ Ejecutar DFS",
            command=self.ejecutar_dfs
        ).pack(fill=tk.X, pady=5)
        
        # Botón limpiar
        ttk.Button(
            control_frame,
            text="🗑️ Limpiar Visualización",
            command=self.limpiar_visualizacion
        ).pack(pady=10, fill=tk.X)
        
        # === SECCIÓN 3: PANEL DE MÉTRICAS (SUPERIOR DERECHA) ===
        metricas_frame = ttk.LabelFrame(main_frame, text="Métricas y Estado", padding="10")
        metricas_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Área de log
        self.log_text = scrolledtext.ScrolledText(
            metricas_frame,
            height=10,
            width=60,
            font=('Consolas', 9),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='white'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Tags para colores
        self.log_text.tag_config('info', foreground='#3498db')
        self.log_text.tag_config('success', foreground='#2ecc71')
        self.log_text.tag_config('error', foreground='#e74c3c')
        self.log_text.tag_config('warning', foreground='#f39c12')
        
        self.log_mensaje("Sistema NeuroNet iniciado", "info")
        self.log_mensaje("Esperando carga de dataset...", "info")
        
        # === SECCIÓN 4: VISUALIZACIÓN (INFERIOR DERECHA) ===
        viz_frame = ttk.LabelFrame(main_frame, text="Visualización de Grafo", padding="10")
        viz_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Canvas para el grafo
        self.canvas_frame = ttk.Frame(viz_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Inicializar visualizador
        self.visualizador = VisualizadorGrafo(self.canvas_frame)
        
        # Mensaje inicial
        lbl_inicial = ttk.Label(
            self.canvas_frame,
            text="Cargue un dataset y ejecute un algoritmo para visualizar el grafo",
            style='Info.TLabel'
        )
        lbl_inicial.pack(expand=True)
    
    def log_mensaje(self, mensaje, tipo='info'):
        """
        Agrega un mensaje al log
        
        Args:
            mensaje: Texto del mensaje
            tipo: 'info', 'success', 'error', 'warning'
        """
        timestamp = time.strftime("%H:%M:%S")
        linea = f"[{timestamp}] {mensaje}\n"
        
        self.log_text.insert(tk.END, linea, tipo)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def cargar_archivo(self):
        """Abre diálogo para cargar archivo de dataset"""
        if not MODULO_DISPONIBLE:
            messagebox.showerror("Error", "Módulo C++ no compilado")
            return
        
        archivo = filedialog.askopenfilename(
            title="Seleccionar Dataset",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ],
            initialdir=os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        )
        
        if not archivo:
            return
        
        self.log_mensaje(f"Cargando archivo: {os.path.basename(archivo)}", "info")
        
        try:
            # Crear instancia del grafo
            self.grafo = PyGrafoDisperso()
            
            # Cargar datos
            inicio = time.time()
            exito = self.grafo.cargar_datos(archivo)
            fin = time.time()
            
            if exito:
                self.archivo_actual = archivo
                tiempo_carga = (fin - inicio) * 1000  # ms
                
                # Obtener métricas
                num_nodos = self.grafo.get_num_nodos()
                num_aristas = self.grafo.get_num_aristas()
                memoria_bytes = self.grafo.get_memoria_estimada()
                memoria_mb = memoria_bytes / (1024 * 1024)
                nodo_max, grado_max = self.grafo.get_nodo_mayor_grado()
                
                # Actualizar interfaz
                self.lbl_archivo.config(text=f"Archivo: {os.path.basename(archivo)}")
                self.lbl_nodos.config(text=f"Nodos: {num_nodos:,}")
                self.lbl_aristas.config(text=f"Aristas: {num_aristas:,}")
                self.lbl_memoria.config(text=f"Memoria: {memoria_mb:.2f} MB")
                self.lbl_mayor_grado.config(text=f"Mayor grado: Nodo {nodo_max} ({grado_max} conexiones)")
                
                self.log_mensaje(f"✓ Carga exitosa en {tiempo_carga:.2f}ms", "success")
                self.log_mensaje(f"  Nodos: {num_nodos:,} | Aristas: {num_aristas:,}", "success")
                
                messagebox.showinfo(
                    "Carga Exitosa",
                    f"Dataset cargado correctamente\n\n"
                    f"Nodos: {num_nodos:,}\n"
                    f"Aristas: {num_aristas:,}\n"
                    f"Tiempo: {tiempo_carga:.2f}ms"
                )
            else:
                self.log_mensaje("✗ Error al cargar el archivo", "error")
                messagebox.showerror("Error", "No se pudo cargar el archivo")
        
        except Exception as e:
            self.log_mensaje(f"✗ Excepción: {str(e)}", "error")
            messagebox.showerror("Error", f"Error al cargar archivo:\n{str(e)}")
    
    def ejecutar_bfs(self):
        """Ejecuta algoritmo BFS y visualiza resultado"""
        if not self.grafo:
            messagebox.showwarning("Advertencia", "Primero cargue un dataset")
            return
        
        try:
            nodo_inicio = int(self.entry_bfs_nodo.get())
            prof_max = int(self.entry_bfs_prof.get())
            
            self.log_mensaje(f"Ejecutando BFS desde nodo {nodo_inicio} (profundidad {prof_max})...", "info")
            
            # Ejecutar BFS
            inicio = time.time()
            resultado = self.grafo.bfs(nodo_inicio, prof_max)
            fin = time.time()
            
            tiempo_ms = (fin - inicio) * 1000
            
            self.log_mensaje(f"✓ BFS completado: {len(resultado)} nodos encontrados en {tiempo_ms:.3f}ms", "success")
            
            # Obtener aristas para visualización
            aristas = self.grafo.get_aristas()
            
            # Visualizar
            self.visualizador.visualizar_subgrafo(
                resultado,
                aristas,
                f"BFS desde nodo {nodo_inicio} (profundidad {prof_max})"
            )
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos")
        except Exception as e:
            self.log_mensaje(f"✗ Error en BFS: {str(e)}", "error")
            messagebox.showerror("Error", f"Error al ejecutar BFS:\n{str(e)}")
    
    def ejecutar_dfs(self):
        """Ejecuta algoritmo DFS y visualiza resultado"""
        if not self.grafo:
            messagebox.showwarning("Advertencia", "Primero cargue un dataset")
            return
        
        try:
            nodo_inicio = int(self.entry_dfs_nodo.get())
            
            self.log_mensaje(f"Ejecutando DFS desde nodo {nodo_inicio}...", "info")
            
            # Ejecutar DFS
            inicio = time.time()
            resultado = self.grafo.dfs(nodo_inicio)
            fin = time.time()
            
            tiempo_ms = (fin - inicio) * 1000
            
            self.log_mensaje(f"✓ DFS completado: {len(resultado)} nodos visitados en {tiempo_ms:.3f}ms", "success")
            
            # Obtener aristas para visualización
            aristas = self.grafo.get_aristas()
            
            # Visualizar
            self.visualizador.visualizar_subgrafo(
                resultado,
                aristas,
                f"DFS desde nodo {nodo_inicio}"
            )
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido")
        except Exception as e:
            self.log_mensaje(f"✗ Error en DFS: {str(e)}", "error")
            messagebox.showerror("Error", f"Error al ejecutar DFS:\n{str(e)}")
    
    def limpiar_visualizacion(self):
        """Limpia la visualización actual"""
        self.visualizador.limpiar()
        self.log_mensaje("Visualización limpiada", "info")


def main():
    """Función principal"""
    root = tk.Tk()
    app = NeuroNetGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
