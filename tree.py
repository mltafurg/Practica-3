from graphviz import Digraph

class Jugada:
    def __init__(self, color, texto):
        self.color = color  # "blancas" o "negras"
        self.texto = texto  # por ejemplo: "e4", "Nf6"

    def __str__(self):
        return f"{self.color}: {self.texto}"

class NodoTurno:
    def __init__(self, numero_turno, jugada_blanca=None, jugada_negra=None):
        self.numero = numero_turno
        self.jugada_blanca = jugada_blanca  # Nodo izquierdo
        self.jugada_negra = jugada_negra    # Nodo derecho

    def __str__(self):
        return f"Turno {self.numero}"

class ArbolPartida:
    def __init__(self):
        self.raiz = "Partida"
        self.turnos = []  # Lista de NodoTurno

    def agregar_turno(self, numero, blanca, negra=None):
        jugada_blanca = Jugada("blancas", blanca)
        jugada_negra = Jugada("negras", negra) if negra else None
        turno = NodoTurno(numero, jugada_blanca, jugada_negra)
        self.turnos.append(turno)

    def imprimir_arbol(self):
        print(f"\n=== Árbol de la partida ===")
        print(f"Raíz: {self.raiz}")
        for nodo in self.turnos:
            print(f"\n{nodo}")
            if nodo.jugada_blanca:
                print(f"  {nodo.jugada_blanca}")
            if nodo.jugada_negra:
                print(f"  {nodo.jugada_negra}")

                

from graphviz import Digraph
import os

from graphviz import Digraph

def exportar_arbol_graphviz(arbol, nombre_archivo="arbol_partida"):
    dot = Digraph(comment='Árbol de la Partida de Ajedrez')

    dot.attr(rankdir='TB', size='10,8')
    dot.attr('node', shape='circle', style='filled', color='#FFA500', fontname='Arial', fontsize='8')
    dot.attr('edge', fontname='Arial', fontsize='7')

    # Nodo raíz
    dot.node("Partida", "Partida", fillcolor='#FFD700', fontcolor='black')

    for idx, turno in enumerate(arbol.turnos):
        nombre_turno = f"Turno {turno.numero}"

        # Color alternado para turnos
        color_turno = '#FFF8DC' if idx % 2 == 0 else '#D3D3D3'
        dot.node(nombre_turno, nombre_turno, fillcolor=color_turno, fontcolor='black', color='#FFA500')

        # Conectar Turno con la raíz "Partida"
        dot.edge("Partida", nombre_turno, style='solid')

        # Jugada Blanca (nodo hijo izquierdo)
        if turno.jugada_blanca:
            id_blanca = f"{nombre_turno}_blanca"
            dot.node(id_blanca, turno.jugada_blanca.texto, fillcolor='white', fontcolor='black', color='#FFA500')
            dot.edge(nombre_turno, id_blanca, label='blancas', style='solid')

        # Jugada Negra (nodo hijo derecho)
        if turno.jugada_negra:
            id_negra = f"{nombre_turno}_negra"
            dot.node(id_negra, turno.jugada_negra.texto, fillcolor='#696969', fontcolor='white', color='#FFA500')
            dot.edge(nombre_turno, id_negra, label='negras', style='dashed')

    try:
        nombre_completo = f"{nombre_archivo}.pdf"
        dot.render(nombre_completo, format='pdf', cleanup=True)
        print(f" PDF generado correctamente: '{nombre_completo}'")
        return nombre_completo
    except Exception as e:
        print(f" Error al generar el PDF: {e}")
        return None



    # --- Bloque con manejo de errores ---
    try:
        # Asegura que el nombre tenga extensión .pdf
        nombre_completo = f"{nombre_archivo}.pdf"
        dot.render(nombre_completo, format='pdf', cleanup=True)
        print(f" PDF generado correctamente: '{nombre_completo}'")
    except Exception as e:
        print(f" Error al generar el PDF: {e}")
        return False  # Opcional: Retorna False para indicar fallo

    return True  # Opcional: Retorna True para indicar éxito