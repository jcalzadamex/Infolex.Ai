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

    coincidencias = list(ARTICULO_REGEX.finditer(texto))

    if not coincidencias:
        return [{"articulo": "DOCUMENTO_COMPLETO", "contenido": texto}]

    articulos = []

    for i, match in enumerate(coincidencias):
        titulo = match.group(1)
        inicio = match.start()

        if i + 1 < len(coincidencias):
            fin = coincidencias[i + 1].start()
        else:
            fin = len(texto)

        contenido = texto[inicio:fin].strip()

        articulos.append({
            "articulo": titulo,
            "contenido": contenido
        })

    return articulos


def process_file(path: Path) -> list[dict]:
    """
    Recibe la ruta a un .txt y devuelve la lista de artículos segmentados.
    """
    texto = path.read_text(encoding="utf-8", errors="ignore")
    return split_into_articles(texto)


if __name__ == "__main__":
    test_path = Path("data/raw/dof/ejemplo.txt")
    if test_path.exists():
        resultado = process_file(test_path)
        for art in resultado:
            print("====", art["articulo"], "====")
            print(art["contenido"][:200], "...\n")
    else:
        print("No existe el archivo data/raw/dof/ejemplo.txt")
