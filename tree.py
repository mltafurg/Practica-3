from collections import deque
import subprocess
import os
import sys

class Jugada:
    def __init__(self, notacion):
        self.notacion = notacion
        self.texto = notacion  # Para compatibilidad

class Turno:
    def __init__(self, numero):
        self.numero = numero
        self.jugada_blanca = None
        self.jugada_negra = None
    
    def set_jugada_blanca(self, jugada):
        self.jugada_blanca = jugada
    
    def set_jugada_negra(self, jugada):
        self.jugada_negra = jugada

class Nodo:
    def __init__(self, id, jugada, padre=None, es_jugada_blanca=None):
        self.id = id
        self.jugada = jugada
        self.padre = padre
        self.hijos = []
        self.es_jugada_blanca = es_jugada_blanca  # True=blancas, False=negras, None=inicio

class ArbolPartida:
    def __init__(self):
        self.id_counter = 0
        self.raiz = Nodo(self._nuevo_id(), "Inicio", es_jugada_blanca=None)
        self.turnos = []  
        self.jugadas_lineales = ["Inicio"]  # Lista lineal de jugadas
        self.colores_jugadas = [None]  # None=inicio, True=blancas, False=negras

    def _nuevo_id(self):
        self.id_counter += 1
        return f"n{self.id_counter}"

    def _construir_arbol_binario(self):
        """Construye un árbol binario a partir de la lista lineal de jugadas"""
        if not self.jugadas_lineales:
            return
        
        # Crear todos los nodos con información de color
        nodos = []
        for i, (jugada, es_blanca) in enumerate(zip(self.jugadas_lineales, self.colores_jugadas)):
            nodo = Nodo(self._nuevo_id(), jugada, es_jugada_blanca=es_blanca)
            nodos.append(nodo)
        
        # Establecer relaciones padre-hijo siguiendo estructura de árbol binario
        for i in range(len(nodos)):
            hijo_izq_idx = i * 2 + 1
            hijo_der_idx = i * 2 + 2
            
            if hijo_izq_idx < len(nodos):
                nodos[hijo_izq_idx].padre = nodos[i]
                nodos[i].hijos.append(nodos[hijo_izq_idx])
            
            if hijo_der_idx < len(nodos):
                nodos[hijo_der_idx].padre = nodos[i]
                nodos[i].hijos.append(nodos[hijo_der_idx])
        
        self.raiz = nodos[0] if nodos else None

    def agregar_turno(self, numero_turno, jugada_blanca, jugada_negra=None):
        """Método para compatibilidad con GUI original"""
        # Crear objetos de turno
        turno = Turno(numero_turno)
        turno.set_jugada_blanca(Jugada(jugada_blanca))
        if jugada_negra:
            turno.set_jugada_negra(Jugada(jugada_negra))
        
        self.turnos.append(turno)
        
        # Actualizar lista lineal con colores
        self.jugadas_lineales.append(jugada_blanca)
        self.colores_jugadas.append(True)  # Blancas
        
        if jugada_negra:
            self.jugadas_lineales.append(jugada_negra)
            self.colores_jugadas.append(False)  # Negras
        
        # Reconstruir árbol
        self._construir_arbol_binario()

    def exportar_dot(self):
        """Exporta el árbol a formato DOT con colores diferenciados para blancas y negras"""
        dot = ["digraph G {"]
        dot.append("  rankdir=TB;")
        dot.append("  node [shape=circle, style=filled, fontname=\"Arial\", fontsize=12];")
        dot.append("  edge [fontname=\"Arial\", fontsize=10];")
        dot.append("  bgcolor=white;")

        if not self.raiz:
            dot.append("}")
            return "\n".join(dot)

        # Recorrer el árbol usando BFS
        cola = deque([self.raiz])
        while cola:
            actual = cola.popleft()
            label = actual.jugada.replace("\"", "'")
            
            # Colores según el tipo de jugada
            if actual.es_jugada_blanca is None:  # Nodo inicio
                color = "lightblue"
                fontcolor = "black"
            elif actual.es_jugada_blanca:  # Jugadas blancas
                color = "white"
                fontcolor = "black"
            else:  # Jugadas negras
                color = "black"
                fontcolor = "white"

            dot.append(f'  {actual.id} [label="{label}", fillcolor="{color}", fontcolor="{fontcolor}"];')
            
            # Agregar conexiones a hijos
            for hijo in actual.hijos:
                dot.append(f"  {actual.id} -> {hijo.id};")
                cola.append(hijo)

        dot.append("}")
        return "\n".join(dot)

def _verificar_graphviz():
    """Verifica si Graphviz está instalado"""
    try:
        subprocess.run(["dot", "-V"], capture_output=True, check=True, text=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def _generar_png_desde_dot():
    """Genera PNG desde el archivo DOT usando Graphviz"""
    try:
        if not os.path.exists("arbol.dot"):
            return False

        if not _verificar_graphviz():
            return False
        
        result = subprocess.run(
            ["dot", "-Tpng", "arbol.dot", "-o", "arbol.png"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        return result.returncode == 0 and os.path.exists("arbol.png")
            
    except Exception:
        return False

def exportar_arbol_graphviz(arbol):
   
    try:
        # Generar archivo DOT
        dot_content = arbol.exportar_dot()
        
        with open("arbol.dot", "w", encoding="utf-8") as f:
            f.write(dot_content)
        
        # Intentar generar PNG automáticamente
        _generar_png_desde_dot()
        
        return True
        
    except Exception:
        return False

if __name__ == "__main__":
    # Importar chessp para la prueba
    try:
        from chessp import parse_turns, is_valid_move
        
        print("Probando árbol con chessp...")
        
        # Texto de prueba
        texto_partida = "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6"
        
        # Usar chessp para parsear
        turns = parse_turns(texto_partida)
        arbol = ArbolPartida()
        
        for t in turns:
            partes = t.split()
            if len(partes) >= 2:
                jugada_blanca = partes[1]
                jugada_negra = partes[2] if len(partes) == 3 else None
                turno_numero = partes[0].replace(".", "")
                
                if is_valid_move(jugada_blanca):
                    if jugada_negra is None or is_valid_move(jugada_negra):
                        arbol.agregar_turno(turno_numero, jugada_blanca, jugada_negra)
        
        # Exportar
        if exportar_arbol_graphviz(arbol):
            print("Archivos generados: arbol.dot y arbol.png")
        else:
            print("Error al generar archivos")
            
    except ImportError:
        print("No se pudo importar chessp para la prueba")
    
    # Mantener consola abierta en Windows
    if sys.platform.startswith('win'):
        input("\nPresiona Enter para salir...")
