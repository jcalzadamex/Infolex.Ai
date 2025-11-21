import chromadb
from chromadb.config import Settings

def get_collection(name: str = "infolex_articles"):
    client = chromadb.Client(Settings())
    return client.get_collection(name=name)


def search_similar(pregunta: str, n_results: int = 5):
    """
    Devuelve los fragmentos más similares a la pregunta, usando Chroma.
    """
    collection = get_collection()
    res = collection.query(
        query_texts=[pregunta],
        n_results=n_results
    )
    return res


def answer_question(pregunta: str) -> dict:
    """
    Versión sencilla:
    - Busca artículos similares.
    - Devuelve los textos y metadatos.
    Más adelante aquí llamaremos al LLM (GPT/Claude) para redactar
    la respuesta clara estilo Infolex.
    """
    resultados = search_similar(pregunta)

    documentos = resultados.get("documents", [[]])[0]
    metadatas = resultados.get("metadatas", [[]])[0]

    fragmentos = []
    for doc, meta in zip(documentos, metadatas):
        fragmentos.append({
            "texto": doc,
            "materia": meta.get("materia"),
            "articulo": meta.get("articulo"),
            "source_file": meta.get("source_file")
        })

    respuesta = {
        "respuesta_clara": (
            "Prototipo: aquí iría la respuesta generada por IA, "
            "usando los artículos que ves en 'fragmentos'."
        ),
        "fragmentos": fragmentos
    }
    return respuesta


if __name__ == "__main__":
    demo = answer_question("¿Qué dice la ley sobre salarios mínimos?")
    print(demo["respuesta_clara"])
    for frag in demo["fragmentos"]:
        print("===", frag["articulo"], "===")
        print(frag["texto"][:300], "...\n")
