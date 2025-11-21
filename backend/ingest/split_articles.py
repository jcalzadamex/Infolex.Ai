import re
from pathlib import Path

ARTICULO_REGEX = re.compile(
    r"(Artículo\s*[0-9]+[A-Za-zº\.]*)", 
    flags=re.IGNORECASE
)

def split_into_articles(texto: str) -> list[dict]:
    """
    Recibe el texto completo de una ley/documento y lo separa 
    en artículos usando una expresión regular.

    Devuelve una lista de dicts:
    [
        {
            "articulo": "Artículo 1",
            "contenido": "Texto del artículo 1..."
        },
        ...
    ]
    """

    # Encuentra todas las coincidencias del patrón
    coincidencias = list(ARTICULO_REGEX.finditer(texto))

    if not coincidencias:
        return [{"articulo": "DOCUMENTO_COMPLETO", "contenido": texto}]

    articulos = []

    for i, match in enumerate(coincidencias):
        titulo = match.group(1)
        inicio = match.start()

        # Fin = inicio del siguiente artículo o fin del documento
        if i + 1 < len(coincidencias):
            fin = coincidencias[i + 1].start()
        else:
            fin = len(texto)

        contenido = texto[inicio:fin].strip()
