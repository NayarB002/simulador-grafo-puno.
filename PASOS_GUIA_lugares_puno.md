# Simulador de Caminos en Puno

Este proyecto permite simular rutas entre los lugares más populares de la ciudad de Puno usando Python y NetworkX.

## Archivos principales
- `camino_mas_corto_puno.py`: Script principal del simulador.
- `lugares_puno.txt`: Lista de los lugares más populares de Puno (uno por línea).

## Requisitos previos
- Python 3.x instalado
- Instalar dependencias:
  ```
  pip install networkx matplotlib geopy
  ```

## Paso a paso para usar el simulador

1. **Verifica los archivos**
   - Asegúrate de tener `camino_mas_corto_puno.py` y `lugares_puno.txt` en la misma carpeta.

2. **Revisa o edita la lista de lugares**
   - Puedes abrir `lugares_puno.txt` para ver o modificar los lugares que se usan como nodos en el grafo.

3. **Ejecuta el simulador**
   - Abre una terminal en la carpeta del proyecto.
   - Ejecuta:
     ```
     python camino_mas_corto_puno.py
     ```

4. **Selecciona origen y destino**
   - El programa mostrará la lista de lugares disponibles.
   - Escribe el nombre exacto del lugar de origen y luego el de destino.

5. **Resultados y visualización**
   - El simulador mostrará en consola:
     - El camino más corto y más largo (si existe)
     - Distancia y tiempo estimado para cada ruta
   - Se abrirá una ventana con el mapa del grafo, rutas resaltadas, leyenda y recuadro de información movible.

## Personalización
- Puedes agregar, quitar o cambiar lugares en `lugares_puno.txt` y adaptar el script para leerlos automáticamente.
- Puedes modificar las conexiones en el script para reflejar nuevas rutas o calles.

## Autor
- NayarB002
