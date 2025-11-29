#ifndef GRAFO_DISPERSO_H
#define GRAFO_DISPERSO_H

#include "GrafoBase.h"
#include <vector>
#include <string>
#include <map>

/**
 * Implementación de grafo usando formato CSR (Compressed Sparse Row)
 * Optimizado para grafos dispersos con millones de nodos
 */
class GrafoDisperso : public GrafoBase {
private:
    // Formato CSR para matriz de adyacencia dispersa
    std::vector<int> row_ptr;        // Punteros a inicio de cada fila
    std::vector<int> col_indices;    // Índices de columnas (vecinos)
    std::vector<int> values;         // Valores (1 para grafo no ponderado)
    
    int numNodos;                    // Número total de nodos
    int numAristas;                  // Número total de aristas
    
    // Mapeo de IDs de nodos originales a índices internos
    std::map<int, int> nodoAIndice;
    std::map<int, int> indiceANodo;
    
    // Grados de entrada y salida para cada nodo
    std::vector<int> gradosSalida;
    std::vector<int> gradosEntrada;
    
    /**
     * Construye la estructura CSR a partir de lista de aristas
     * @param aristas Vector de pares (origen, destino)
     */
    void construirCSR(const std::vector<std::pair<int, int>>& aristas);
    
    /**
     * Imprime mensaje de log con prefijo [C++ Core]
     * @param mensaje Mensaje a imprimir
     */
    void log(const std::string& mensaje);
    
public:
    GrafoDisperso();
    ~GrafoDisperso();
    
    // Implementación de métodos abstractos
    bool cargarDatos(const std::string& nombreArchivo) override;
    std::vector<std::pair<int, int>> BFS(int nodoInicio, int profundidadMax = -1) override;
    std::vector<int> DFS(int nodoInicio) override;
    int obtenerGrado(int nodo) override;
    std::vector<int> getVecinos(int nodo) override;
    int getNumNodos() const override;
    int getNumAristas() const override;
    std::pair<int, int> getNodoMayorGrado() override;
    
    /**
     * Obtiene la memoria estimada usada por la estructura CSR
     * @return Memoria en bytes
     */
    size_t getMemoriaEstimada() const;
    
    /**
     * Obtiene todas las aristas del grafo
     * @return Vector de pares (origen, destino)
     */
    std::vector<std::pair<int, int>> getAristas() const;
};

#endif // GRAFO_DISPERSO_H
