from pathlib import Path
import chromadb

# IMPORTS DEL PIPELINE DE INGESTA
# OJO: según cómo ejecutes el código, quizá tengas que ajustar estas rutas
from backend.ingest.normalize import normalize_file
from backend.ingest.split_articles import process_file


def get_client():
    """
    Crea un cliente simple de Chroma (base de datos vectorial local).
    """
    client = chromadb.Client()
    return client


def get_collection(name: str = "infolex_articles"):
    client = get_client()
    collection = client.get_or_create_collection(name=name)
    return collection


def index_file(path: Path, materia: str = "desconocida"):
    """
    1) Normaliza el texto crudo.
    2) Lo parte en artículos.
    3) Mete cada artículo como documento en Chroma.
    """
    print(f"[INDEX] Procesando archivo: {path}")

    # 1. Normalizar
    normalized_path = normalize_file(path)
    print(f"[INDEX] Normalizado en: {normalized_path}")

    # 2. Partir en artículos
    articulos = process_file(normalized_path)
    print(f"[INDEX] Encontrados {len(articulos)} artículos")

    # 3. Insertar en Chroma
    collection = get_collection()
    docs = []
    metadatas = []
    ids = []

    for i, art in enumerate(articulos, start=1):
        contenido = art["contenido"]
        titulo = art["articulo"]

        docs.append(contenido)
        metadatas.append({
            "materia": materia,
            "articulo": titulo,
            "source_file": str(path)
        })
        ids.append(f"{path.stem}_{i}")

    if docs:
        collection.add(documents=docs, metadatas=metadatas, ids=ids)
        print(f"[INDEX] Indexados {len(docs)} artículos de {path}")


def index_folder(folder: Path, materia: str):
    """
    Indexa todos los .txt de una carpeta.
    Ejemplo: data/raw/dof/2025-01-01
    """
    txt_files = list(folder.glob("*.txt"))
    print(f"[INDEX] Encontrados {len(txt_files)} archivos en {folder}")

    for path in txt_files:
        index_file(path, materia=materia)


if __name__ == "__main__":
    # EJEMPLO DE USO:
    # Supón que ya corriste el scraper del DOF para un día concreto
    ejemplo_carpeta = Path("data/raw/dof/2025-01-01")
    if ejemplo_carpeta.exists():
        index_folder(ejemplo_carpeta, materia="desconocida")
    else:
        print("[INDEX] No existe la carpeta de ejemplo:", ejemplo_carpeta)
