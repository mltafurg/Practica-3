from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt5.QtGui import QFont
import sys

from chess_parser import parse_turns, is_valid_move
from tree import ArbolPartida, exportar_arbol_graphviz

class ChessApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visor de Partida de Ajedrez")
        self.setGeometry(100, 100, 700, 600)

        layout = QVBoxLayout()

        self.label = QLabel("Ingresa la partida SAN (por ejemplo: 1. e4 e5 2. Nf3 Nc6...)")
        self.label.setFont(QFont("Arial", 12))
        layout.addWidget(self.label)

        self.text_area = QTextEdit()
        self.text_area.setFont(QFont("Courier", 11))
        layout.addWidget(self.text_area)

        self.button = QPushButton("Analizar partida y generar árbol")
        self.button.clicked.connect(self.cargar_partida)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def cargar_partida(self):
        san_text = self.text_area.toPlainText().strip()

        if not san_text:
            self.text_area.setText("Por favor, escribe o pega una partida en notación SAN.")
            return

        turns = parse_turns(san_text)
        errores = []
        arbol = ArbolPartida()

        for t in turns:
            partes = t.split()
            if len(partes) < 2:
                errores.append(f"[X] Turno incompleto: {t}")
                continue

            jugada_blanca = partes[1]
            if not is_valid_move(jugada_blanca):
                errores.append(f"[X] Jugada blanca inválida en turno {partes[0]}: {jugada_blanca}")
                continue

            jugada_negra = None
            if len(partes) == 3:
                jugada_negra = partes[2]
                if not is_valid_move(jugada_negra):
                    errores.append(f"[X] Jugada negra inválida en turno {partes[0]}: {jugada_negra}")
                    continue

            turno_numero = partes[0].replace(".", "")
            arbol.agregar_turno(turno_numero, jugada_blanca, jugada_negra)

        if errores:
            salida = "Se encontraron errores en la partida:\n\n"
            salida += "\n".join(errores)
            salida += "\n\nEl árbol no será generado."
            self.text_area.setText(salida)
        else:
            salida = "Partida válida. Árbol generado:\n"
            for nodo in arbol.turnos:
                salida += f"\nTurno {nodo.numero}\n"
                if nodo.jugada_blanca:
                    salida += f"  |- blancas: {nodo.jugada_blanca.texto}\n"
                if nodo.jugada_negra:
                    salida += f"  |- negras: {nodo.jugada_negra.texto}\n"

            self.text_area.setText(salida)
            exportar_arbol_graphviz(arbol)

def main():
    app = QApplication(sys.argv)
    ventana = ChessApp()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
