# 📊 Archivos de Prueba - Guía de Uso

## 🎯 Archivos Disponibles

| Archivo | Nodos | Aristas | Tamaño | Uso Recomendado |
|---------|-------|---------|--------|-----------------|
| `test_100.txt` | 100 | 150 | ~1 KB | ✅ Demos y presentaciones |
| `test_500.txt` | 500 | 667 | ~6 KB | ✅ Pruebas normales |
| `test_1000.txt` | 1,000 | 1,496 | ~13 KB | ✅ Grafos medianos |
| `test_5000.txt` | 5,000 | 6,645 | ~69 KB | ⚠️ Pruebas de estrés |
| `test_10000.txt` | 10,000 | 11,195 | ~118 KB | ⚠️ Límite visual |
| `test_500k.txt` | 500,000 | 505,489 | ~5.3 MB | 🔥 **SOLO PROCESAMIENTO** |

---

## 🟢 Archivos para Visualización (100 - 1000 nodos)

### **test_100.txt** - Ideal para Demos
```
✅ Visualización instantánea
✅ Perfecto para mostrar algoritmos
✅ Claridad máxima
```

**Uso típico:**
- Presentaciones y demos
- Entender BFS/DFS visualmente
- Pruebas rápidas

---

### **test_500.txt** - Balance Perfecto
```
✅ Buena velocidad
✅ Complejidad moderada
✅ Visualización clara
```

**Uso típico:**
- Desarrollo y pruebas
- Validar algoritmos
- Análisis de componentes

---

### **test_1000.txt** - Límite Cómodo
```
✅ Últimos dígitos antes de saturación visual
⚠️ NetworkX ~2-3 segundos
✅ Algoritmos C++ siguen rápidos
```

**Uso típico:**
- Pruebas de rendimiento básicas
- Grafos de tamaño real pequeños

---

## 🟡 Archivos de Estrés (5000 - 10000 nodos)

### **test_5000.txt** - Prueba de Estrés
```
⚠️ Visualización muy saturada
⚠️ NetworkX ~10-15 segundos
✅ C++ procesa en milisegundos
```

**Uso típico:**
- **NO RECOMENDADO para visualización completa**
- Usar con profundidad limitada (ej: profundidad 10)
- Ver rendimiento de algoritmos C++

---

### **test_10000.txt** - MÁXIMO Visual
```
🔴 NO visualizar completo
⚠️ NetworkX puede congelarse (+30s)
✅ BFS/DFS en C++ aún rápidos
```

**Uso típico:**
- **SOLO ejecutar algoritmos SIN dibujar**
- Benchmarks de rendimiento C++
- Límite absoluto para visualización

---

## 🔥 Archivo Masivo (500,000 nodos)

### **test_500k.txt** - SOLO PROCESAMIENTO C++

```
❌ NUNCA intentar visualizar completo
❌ NetworkX fallará o tardará horas
✅ C++ procesa en milisegundos
```

**⚠️ ADVERTENCIAS CRÍTICAS:**
- **NO cargar en visualización sin límite de profundidad**
- **NO ejecutar DFS completo** (visitará todos los nodos)
- **SÍ ejecutar BFS con profundidad limitada** (ej: 10-20)

**Uso correcto:**
```
BFS - Nodo Inicio: 0
Profundidad Máxima: 10  ← IMPORTANTE: Limitar profundidad
```

Esto procesará ~10-100 nodos (dependiendo de la estructura), que SÍ se pueden visualizar.

---

## 💡 Recomendaciones de Uso

### Para Visualización:
1. **Empieza con test_100.txt**
2. Si funciona bien → test_500.txt
3. Si aún fluido → test_1000.txt
4. **EVITA test_5000+** para visualización completa

### Para Probar Rendimiento C++:
1. **test_5000.txt**: Con profundidad limitada (10-20)
2. **test_10000.txt**: Con profundidad muy limitada (5-10)
3. **test_500k.txt**: Con profundidad MUY limitada (5) o sin visualizar

### Profundidad Recomendada por Archivo:

| Archivo | Profundidad Segura | Nodos Esperados |
|---------|-------------------|-----------------|
| test_100.txt | 50-100 | ~100 |
| test_500.txt | 50-100 | ~500 |
| test_1000.txt | 50-100 | ~1000 |
| test_5000.txt | 10-20 | ~100-500 |
| test_10000.txt | 5-10 | ~50-200 |
| test_500k.txt | 3-10 | ~10-100 |

---

## 🎯 Ejemplos de Uso

### ✅ CORRECTO - Grafo grande con límite:
```
Archivo: test_500k.txt
BFS - Nodo: 0
Profundidad: 10
→ Procesa ~100 nodos en milisegundos
→ Visualiza perfectamente
```

### ❌ INCORRECTO - Sin límite:
```
Archivo: test_500k.txt
BFS - Nodo: 0
Profundidad: 1000
→ Intentará procesar 500K nodos
→ Congelará la visualización
```

---

## 🚀 Capacidades del Sistema

### **Procesamiento C++ (Backend):**
- ✅ Puede manejar **millones de nodos**
- ✅ BFS/DFS en **milisegundos**
- ✅ Memoria ultra-eficiente (CSR)

### **Visualización NetworkX (Frontend):**
- ✅ Óptimo: < 1,000 nodos
- ⚠️ Aceptable: 1,000 - 5,000 nodos
- 🔴 Problemático: > 10,000 nodos
- ❌ Imposible: > 50,000 nodos

---

## 📝 Notas Técnicas

**¿Por qué esta diferencia?**

```
C++ (Procesamiento)    vs    NetworkX (Visualización)
├─ Optimizado          vs    ├─ Python puro
├─ Estructuras CSR     vs    ├─ Cálculos de layout
├─ Sin interfaz        vs    ├─ Dibuja cada nodo/arista
└─ Ultra rápido        vs    └─ Lento con muchos elementos
```

**La solución:**
- **Usa C++ para procesar** (rápido, millones de nodos)
- **Limita lo que visualizas** (solo lo necesario)
- **Mejor de ambos mundos**: Velocidad + Visualización clara

---

## 🏆 Mejores Prácticas

1. **Siempre empieza con archivos pequeños** (test_100.txt)
2. **Incrementa gradualmente** el tamaño
3. **Para grafos grandes**: Usa profundidad limitada
4. **Si se congela**: Reduce profundidad o usa archivo más pequeño
5. **Para benchmarks**: Usa test_500k.txt sin visualizar (solo mide tiempo)

---

**¡Disfruta explorando grafos masivos con NeuroNet!** 🚀
