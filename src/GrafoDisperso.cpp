#include "../include/GrafoDisperso.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <queue>
#include <stack>
#include <set>
#include <chrono>

GrafoDisperso::GrafoDisperso() : numNodos(0), numAristas(0) {
    log("Inicializando GrafoDisperso...");
}

GrafoDisperso::~GrafoDisperso() {
    // Limpieza automática de vectores
}

void GrafoDisperso::log(const std::string& mensaje) {
    std::cout << "[C++ Core] " << mensaje << std::endl;
}

bool GrafoDisperso::cargarDatos(const std::string& nombreArchivo) {
    log("Cargando dataset '" + nombreArchivo + "'...");
    
    std::ifstream archivo(nombreArchivo);
    if (!archivo.is_open()) {
        log("ERROR: No se pudo abrir el archivo");
        return false;
    }
    
    std::vector<std::pair<int, int>> aristas;
    std::set<int> nodosUnicos;
    std::string linea;
    int lineaNum = 0;
    
    // Leer archivo línea por línea
    while (std::getline(archivo, linea)) {
        lineaNum++;
        
        // Ignorar líneas vacías y comentarios
        if (linea.empty() || linea[0] == '#' || linea[0] == '%') {
            continue;
        }
        
        std::istringstream iss(linea);
        int origen, destino;
        
        if (iss >> origen >> destino) {
            aristas.push_back({origen, destino});
            nodosUnicos.insert(origen);
            nodosUnicos.insert(destino);
        }
    }
    
    archivo.close();
    
    numNodos = nodosUnicos.size();
    numAristas = aristas.size();
    
    // Crear mapeo de IDs originales a índices consecutivos
    int indice = 0;
    for (int nodo : nodosUnicos) {
        nodoAIndice[nodo] = indice;
        indiceANodo[indice] = nodo;
        indice++;
    }
    
    // Construir estructura CSR
    construirCSR(aristas);
    
    log("Carga completa. Nodos: " + std::to_string(numNodos) + 
        " | Aristas: " + std::to_string(numAristas));
    
    size_t memoriaBytes = getMemoriaEstimada();
    double memoriaMB = memoriaBytes / (1024.0 * 1024.0);
    log("Estructura CSR construida. Memoria estimada: " + 
        std::to_string(memoriaMB) + " MB.");
    
    return true;
}

void GrafoDisperso::construirCSR(const std::vector<std::pair<int, int>>& aristas) {
    // Inicializar vectores
    row_ptr.resize(numNodos + 1, 0);
    gradosSalida.resize(numNodos, 0);
    gradosEntrada.resize(numNodos, 0);
    
    // Contar grados de salida para cada nodo
    for (const auto& arista : aristas) {
        int origenIdx = nodoAIndice[arista.first];
        int destinoIdx = nodoAIndice[arista.second];
        gradosSalida[origenIdx]++;
        gradosEntrada[destinoIdx]++;
    }
    
    // Construir row_ptr (suma acumulativa de grados)
    row_ptr[0] = 0;
    for (int i = 0; i < numNodos; i++) {
        row_ptr[i + 1] = row_ptr[i] + gradosSalida[i];
    }
    
    // Reservar espacio para columnas y valores
    col_indices.resize(numAristas);
    values.resize(numAristas, 1);
    
    // Llenar col_indices
    std::vector<int> contadores(numNodos, 0);
    for (const auto& arista : aristas) {
        int origenIdx = nodoAIndice[arista.first];
        int destinoIdx = nodoAIndice[arista.second];
        
        int pos = row_ptr[origenIdx] + contadores[origenIdx];
        col_indices[pos] = destinoIdx;
        contadores[origenIdx]++;
    }
    
    // Ordenar vecinos de cada nodo para búsquedas más eficientes
    for (int i = 0; i < numNodos; i++) {
        std::sort(col_indices.begin() + row_ptr[i], 
                  col_indices.begin() + row_ptr[i + 1]);
    }
}

std::vector<std::pair<int, int>> GrafoDisperso::BFS(int nodoInicio, int profundidadMax) {
    log("Ejecutando BFS nativo desde nodo " + std::to_string(nodoInicio) + "...");
    
    auto inicio = std::chrono::high_resolution_clock::now();
    
    std::vector<std::pair<int, int>> resultado;
    
    // Verificar que el nodo existe
    if (nodoAIndice.find(nodoInicio) == nodoAIndice.end()) {
        log("ERROR: Nodo " + std::to_string(nodoInicio) + " no existe en el grafo");
        return resultado;
    }
    
    int nodoInicioIdx = nodoAIndice[nodoInicio];
    
    // Cola manual para BFS
    std::queue<std::pair<int, int>> cola; // (índice_nodo, nivel)
    std::vector<bool> visitado(numNodos, false);
    
    cola.push({nodoInicioIdx, 0});
    visitado[nodoInicioIdx] = true;
    
    while (!cola.empty()) {
        auto [nodoActualIdx, nivel] = cola.front();
        cola.pop();
        
        // Agregar a resultado (convertir índice a ID original)
        int nodoOriginal = indiceANodo[nodoActualIdx];
        resultado.push_back({nodoOriginal, nivel});
        
        // Si alcanzamos la profundidad máxima, no expandir más
        if (profundidadMax != -1 && nivel >= profundidadMax) {
            continue;
        }
        
        // Explorar vecinos
        int inicio = row_ptr[nodoActualIdx];
        int fin = row_ptr[nodoActualIdx + 1];
        
        for (int i = inicio; i < fin; i++) {
            int vecinoIdx = col_indices[i];
            
            if (!visitado[vecinoIdx]) {
                visitado[vecinoIdx] = true;
                cola.push({vecinoIdx, nivel + 1});
            }
        }
    }
    
    auto fin = std::chrono::high_resolution_clock::now();
    auto duracion = std::chrono::duration_cast<std::chrono::microseconds>(fin - inicio);
    
    log("Nodos encontrados: " + std::to_string(resultado.size()) + 
        ". Tiempo ejecución: " + std::to_string(duracion.count() / 1000.0) + "ms.");
    
    return resultado;
}

std::vector<int> GrafoDisperso::DFS(int nodoInicio) {
    log("Ejecutando DFS nativo desde nodo " + std::to_string(nodoInicio) + "...");
    
    std::vector<int> resultado;
    
    // Verificar que el nodo existe
    if (nodoAIndice.find(nodoInicio) == nodoAIndice.end()) {
        log("ERROR: Nodo " + std::to_string(nodoInicio) + " no existe en el grafo");
        return resultado;
    }
    
    int nodoInicioIdx = nodoAIndice[nodoInicio];
    
    // Stack manual para DFS
    std::stack<int> pila;
    std::vector<bool> visitado(numNodos, false);
    
    pila.push(nodoInicioIdx);
    
    while (!pila.empty()) {
        int nodoActualIdx = pila.top();
        pila.pop();
        
        if (visitado[nodoActualIdx]) {
            continue;
        }
        
        visitado[nodoActualIdx] = true;
        
        // Agregar a resultado (convertir índice a ID original)
        int nodoOriginal = indiceANodo[nodoActualIdx];
        resultado.push_back(nodoOriginal);
        
        // Explorar vecinos (en orden inverso para mantener orden correcto)
        int inicio = row_ptr[nodoActualIdx];
        int fin = row_ptr[nodoActualIdx + 1];
        
        for (int i = fin - 1; i >= inicio; i--) {
            int vecinoIdx = col_indices[i];
            
            if (!visitado[vecinoIdx]) {
                pila.push(vecinoIdx);
            }
        }
    }
    
    log("Nodos visitados: " + std::to_string(resultado.size()));
    
    return resultado;
}

int GrafoDisperso::obtenerGrado(int nodo) {
    if (nodoAIndice.find(nodo) == nodoAIndice.end()) {
        return 0;
    }
    
    int idx = nodoAIndice[nodo];
    // Grado total = grado de salida + grado de entrada
    return gradosSalida[idx] + gradosEntrada[idx];
}

std::vector<int> GrafoDisperso::getVecinos(int nodo) {
    std::vector<int> vecinos;
    
    if (nodoAIndice.find(nodo) == nodoAIndice.end()) {
        return vecinos;
    }
    
    int idx = nodoAIndice[nodo];
    int inicio = row_ptr[idx];
    int fin = row_ptr[idx + 1];
    
    for (int i = inicio; i < fin; i++) {
        int vecinoIdx = col_indices[i];
        int vecinoOriginal = indiceANodo[vecinoIdx];
        vecinos.push_back(vecinoOriginal);
    }
    
    return vecinos;
}

int GrafoDisperso::getNumNodos() const {
    return numNodos;
}

int GrafoDisperso::getNumAristas() const {
    return numAristas;
}

std::pair<int, int> GrafoDisperso::getNodoMayorGrado() {
    int maxGrado = -1;
    int nodoMaxGrado = -1;
    
    for (int i = 0; i < numNodos; i++) {
        int grado = gradosSalida[i] + gradosEntrada[i];
        if (grado > maxGrado) {
            maxGrado = grado;
            nodoMaxGrado = indiceANodo[i];
        }
    }
    
    return {nodoMaxGrado, maxGrado};
}

size_t GrafoDisperso::getMemoriaEstimada() const {
    size_t memoria = 0;
    
    // Vectores CSR
    memoria += row_ptr.size() * sizeof(int);
    memoria += col_indices.size() * sizeof(int);
    memoria += values.size() * sizeof(int);
    
    // Grados
    memoria += gradosSalida.size() * sizeof(int);
    memoria += gradosEntrada.size() * sizeof(int);
    
    // Mapeos (aproximado)
    memoria += nodoAIndice.size() * (sizeof(int) * 2 + 32); // overhead de map
    memoria += indiceANodo.size() * (sizeof(int) * 2 + 32);
    
    return memoria;
}

std::vector<std::pair<int, int>> GrafoDisperso::getAristas() const {
    std::vector<std::pair<int, int>> aristas;
    
    for (int i = 0; i < numNodos; i++) {
        int nodoOrigen = indiceANodo.at(i);
        int inicio = row_ptr[i];
        int fin = row_ptr[i + 1];
        
        for (int j = inicio; j < fin; j++) {
            int vecinoIdx = col_indices[j];
            int nodoDestino = indiceANodo.at(vecinoIdx);
            aristas.push_back({nodoOrigen, nodoDestino});
        }
    }
    
    return aristas;
}
