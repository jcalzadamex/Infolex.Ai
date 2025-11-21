from pathlib import Path
import chromadb

# Importamos la normalización y el split en artículos
from backend.ingest.normalize import normalize_file
from backend.ingest.split_articles import process_file


def get_client():
    """
    Crea un cliente simple de Chroma (BD vectorial local).
    """
    client = chromadb.Client()
    return client


def get_collection(name: str = "infolex_articles"):
    """
    Obtiene (o crea, si no existe) la colección principal de Infolex.
    """
    client = get_client()
    collection = client.get_or_create_collection(name=name)
    return collection


def index_file(path: Path, materia: str = "desconocida", ley: str | None = None):
    """
    Indexa un solo archivo .txt:

    1) Normaliza el texto crudo (normalize_file).
    2) Lo parte en artículos (process_file).
    3) Inserta cada artículo como documento en Chroma, con metadata:

        - materia: fiscal, laboral, civil, etc.
        - ley: nombre corto de la ley (o derivado del nombre del archivo).
        - articulo: "Artículo 1", "Artículo 2", etc.
        - source_file: ruta original del archivo.

    Esto permite luego filtrar por materia y/o ley en las consultas.
    """
    print(f"[INDEX] Procesando archivo: {path}")

    # 1. Normalizar
    normalized_path = normalize_file(path)
    print(f"[INDEX] Normalizado en: {normalized_path}")

    # 2. Partir en artículos
    articulos = process_file(normalized_path)
    print(f"[INDEX] Encontrados {len(articulos)} artículos")

    # 3. Determinar nombre de la ley si no se pasa explícitamente
    if ley is None:
        # Ejemplo: "LEY DEL IMPUESTO AL VALOR AGREGADO.txt"
        # -> "ley_del_impuesto_al_valor_agregado"
        ley = path.stem.lower().replace(" ", "_")

    # 4. Insertar en Chroma
    collection = get_collection()
    docs: list[str] = []
    metadatas: list[dict] = []
    ids: list[str] = []

    for i, art in enumerate(articulos, start=1):
        contenido = art["contenido"]
        titulo = art["articulo"]

        docs.append(contenido)
        metadatas.append(
            {
                "materia": materia,
                "ley": ley,
                "articulo": titulo,
                "source_file": str(path),
            }
        )
        ids.append(f"{ley}_{i}")

    if docs:
        collection.add(documents=docs, metadatas=metadatas, ids=ids)
        print(f"[INDEX] Indexados {len(docs)} artículos de {path}")


def index_folder(folder: Path, materia: str = "desconocida", ley: str | None = None):
    """
    Indexa todos los .txt de una carpeta.

    Si se pasa 'ley', se usará el mismo nombre de ley para todos los archivos.
    Si no, cada archivo derivará su propio nombre de ley a partir del nombre
    del fichero (path.stem).
    """
    txt_files = list(folder.glob("*.txt"))
    print(f"[INDEX] Encontrados {len(txt_files)} archivos en {folder}")

    for path in txt_files:
        index_file(path, materia=materia, ley=ley)


if __name__ == "__main__":
    # Ejemplo de uso manual:
    #   python -m backend.rag.index
    #
    # Puedes ajustar esta ruta a alguna carpeta concreta que quieras indexar.
    ejemplo_carpeta = Path("data/raw/dof")
    if ejemplo_carpeta.exists():
        index_folder(ejemplo_carpeta, materia="desconocida")
    else:
        print("[INDEX] No existe la carpeta de ejemplo:", ejemplo_carpeta)
