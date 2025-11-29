# distutils: language = c++
# cython: language_level=3

from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.pair cimport pair

# Declaración de la clase C++ GrafoDisperso
cdef extern from "../include/GrafoDisperso.h":
    cdef cppclass GrafoDisperso:
        GrafoDisperso() except +
        
        bint cargarDatos(const string& nombreArchivo)
        vector[pair[int, int]] BFS(int nodoInicio, int profundidadMax)
        vector[int] DFS(int nodoInicio)
        int obtenerGrado(int nodo)
        vector[int] getVecinos(int nodo)
        int getNumNodos()
        int getNumAristas()
        pair[int, int] getNodoMayorGrado()
        size_t getMemoriaEstimada()
        vector[pair[int, int]] getAristas()

# Wrapper Python de la clase C++
cdef class PyGrafoDisperso:
    cdef GrafoDisperso* c_grafo  # Puntero a la instancia C++
    
    def __cinit__(self):
        """Constructor: crea instancia C++"""
        self.c_grafo = new GrafoDisperso()
    
    def __dealloc__(self):
        """Destructor: libera memoria C++"""
        del self.c_grafo
    
    def cargar_datos(self, str nombre_archivo):
        """
        Carga datos desde un archivo Edge List
        
        Args:
            nombre_archivo: Ruta al archivo de datos
            
        Returns:
            True si la carga fue exitosa, False en caso contrario
        """
        cdef string archivo_cpp = nombre_archivo.encode('utf-8')
        return self.c_grafo.cargarDatos(archivo_cpp)
    
    def bfs(self, int nodo_inicio, int profundidad_max=-1):
        """
        Ejecuta búsqueda en anchura (BFS)
        
        Args:
            nodo_inicio: Nodo desde donde iniciar
            profundidad_max: Profundidad máxima (-1 para ilimitada)
            
        Returns:
            Lista de tuplas (nodo, nivel)
        """
        cdef vector[pair[int, int]] resultado_cpp = self.c_grafo.BFS(nodo_inicio, profundidad_max)
        
        # Convertir vector C++ a lista Python
        resultado_py = []
        cdef int i
        for i in range(resultado_cpp.size()):
            resultado_py.append((resultado_cpp[i].first, resultado_cpp[i].second))
        
        return resultado_py
    
    def dfs(self, int nodo_inicio):
        """
        Ejecuta búsqueda en profundidad (DFS)
        
        Args:
            nodo_inicio: Nodo desde donde iniciar
            
        Returns:
            Lista de nodos visitados
        """
        cdef vector[int] resultado_cpp = self.c_grafo.DFS(nodo_inicio)
        
        # Convertir vector C++ a lista Python
        resultado_py = []
        cdef int i
        for i in range(resultado_cpp.size()):
            resultado_py.append(resultado_cpp[i])
        
        return resultado_py
    
    def obtener_grado(self, int nodo):
        """
        Obtiene el grado de un nodo
        
        Args:
            nodo: ID del nodo
            
        Returns:
            Grado del nodo (número de conexiones)
        """
        return self.c_grafo.obtenerGrado(nodo)
    
    def get_vecinos(self, int nodo):
        """
        Obtiene los vecinos de un nodo
        
        Args:
            nodo: ID del nodo
            
        Returns:
            Lista de IDs de nodos vecinos
        """
        cdef vector[int] vecinos_cpp = self.c_grafo.getVecinos(nodo)
        
        # Convertir vector C++ a lista Python
        vecinos_py = []
        cdef int i
        for i in range(vecinos_cpp.size()):
            vecinos_py.append(vecinos_cpp[i])
        
        return vecinos_py
    
    def get_num_nodos(self):
        """Retorna el número total de nodos"""
        return self.c_grafo.getNumNodos()
    
    def get_num_aristas(self):
        """Retorna el número total de aristas"""
        return self.c_grafo.getNumAristas()
    
    def get_nodo_mayor_grado(self):
        """
        Encuentra el nodo con mayor grado
        
        Returns:
            Tupla (nodo_id, grado)
        """
        cdef pair[int, int] resultado_cpp = self.c_grafo.getNodoMayorGrado()
        return (resultado_cpp.first, resultado_cpp.second)
    
    def get_memoria_estimada(self):
        """
        Obtiene la memoria estimada usada por la estructura CSR
        
        Returns:
            Memoria en bytes
        """
        return self.c_grafo.getMemoriaEstimada()
    
    def get_aristas(self):
        """
        Obtiene todas las aristas del grafo
        
        Returns:
            Lista de tuplas (origen, destino)
        """
        cdef vector[pair[int, int]] aristas_cpp = self.c_grafo.getAristas()
        
        # Convertir vector C++ a lista Python
        aristas_py = []
        cdef int i
        for i in range(aristas_cpp.size()):
            aristas_py.append((aristas_cpp[i].first, aristas_cpp[i].second))
        
        return aristas_py
