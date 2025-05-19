import re

def parse_turns(san_text):
    """
    Recibe el texto completo de la partida SAN y retorna una lista con los turnos.
    Cada turno es una cadena como '1. d4 d5'
    """

    # Eliminamos saltos de línea extra y espacios duplicados
    san_text = san_text.replace("\n", " ")
    san_text = re.sub(r'\s+', ' ', san_text).strip()

    # Expresión regular para capturar los turnos (ej. 1. e4 e5)
    pattern = r'\d+\.\s*\S+(?:\s+\S+)?'

    # Busca todas las coincidencias
    turns = re.findall(pattern, san_text)

    return turns

def is_valid_move(move):
    """
    Verifica si una jugada individual es válida según la gramática BNF.
    """
   ## import re

    # Enroques
    if move == "O-O" or move == "O-O-O":
        return True

    # Movimiento de pieza: K, Q, R, B, N + [desambiguación] + [x] + casilla + [=promoción] + [+|#]
    pieza_regex = r"^[KQRBN]([a-h1-8]?)(x)?[a-h][1-8](=[QRBN])?[\+#]?$"

    # Movimiento de peón simple (avance): casilla + promoción opcional + jaque/mate
    peon_avance = r"^[a-h][1-8](=[QRBN])?[\+#]?$"

    # Movimiento de peón captura: letra x casilla + promoción opcional + jaque/mate
    peon_captura = r"^[a-h]x[a-h][1-8](=[QRBN])?[\+#]?$"

    # Verifica si alguna coincide
    if re.match(pieza_regex, move):
        return True
    if re.match(peon_avance, move):
        return True
    if re.match(peon_captura, move):
        return True

    # Si no cumple nada, es inválida
    return False
