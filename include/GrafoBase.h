#ifndef GRAFO_BASE_H
#define GRAFO_BASE_H

#include <vector>
#include <string>
#include <utility>

/**
 * Clase abstracta que define la interfaz para grafos
 * Todos los grafos deben heredar de esta clase e implementar sus métodos
 */
class GrafoBase {
public:
    virtual ~GrafoBase() {}
    
    /**
     * Carga datos desde un archivo en formato Edge List
     * @param nombreArchivo Ruta al archivo de datos
     * @return true si la carga fue exitosa, false en caso contrario
     */
    virtual bool cargarDatos(const std::string& nombreArchivo) = 0;
    
    /**
     * Realiza una búsqueda en anchura (BFS) desde un nodo inicial
     * @param nodoInicio Nodo desde donde iniciar la búsqueda
     * @param profundidadMax Profundidad máxima de búsqueda (-1 para ilimitada)
     * @return Vector de pares (nodo, nivel) visitados
     */
    virtual std::vector<std::pair<int, int>> BFS(int nodoInicio, int profundidadMax = -1) = 0;
    
    /**
     * Realiza una búsqueda en profundidad (DFS) desde un nodo inicial
     * @param nodoInicio Nodo desde donde iniciar la búsqueda
     * @return Vector de nodos visitados en orden DFS
     */
    virtual std::vector<int> DFS(int nodoInicio) = 0;
    
    /**
     * Obtiene el grado de un nodo (número de conexiones)
     * @param nodo ID del nodo
     * @return Grado del nodo
     */
    virtual int obtenerGrado(int nodo) = 0;
    
    /**
     * Obtiene los vecinos de un nodo
     * @param nodo ID del nodo
     * @return Vector con los IDs de los nodos vecinos
     */
    virtual std::vector<int> getVecinos(int nodo) = 0;
    
    /**
     * Obtiene el número total de nodos en el grafo
     * @return Número de nodos
     */
    virtual int getNumNodos() const = 0;
    
    /**
     * Obtiene el número total de aristas en el grafo
     * @return Número de aristas
     */
    virtual int getNumAristas() const = 0;
    
    /**
     * Encuentra el nodo con mayor grado
     * @return Par (nodoID, grado)
     */
    virtual std::pair<int, int> getNodoMayorGrado() = 0;
};

#endif // GRAFO_BASE_H
