import textwrap

from backend.ingest.normalize import basic_normalize
from backend.ingest.split_articles import split_into_articles


def test_basic_normalize_elimina_espacios_y_lineas_vacias():
    raw = "  Línea 1   \n\n\nLínea   2\t\t  \n\n"
    norm = basic_normalize(raw)

    # No debe haber más de una línea vacía seguida
    lineas = norm.split("\n")
    assert lineas[0] == "Línea 1"
    assert lineas[1] == "Línea 2"
    assert len(lineas) == 2


def test_split_into_articles_encuentra_articulos_simples():
    texto = textwrap.dedent(
        """
        Artículo 1. Este es el primer artículo de prueba.
        Tiene varias líneas,
        pero sigue siendo el mismo artículo.

        Artículo 2. Este es el segundo artículo.
        """
    ).strip()

    articulos = split_into_articles(texto)

    assert len(articulos) == 2

    titulos = [a["articulo"] for a in articulos]
    assert "Artículo 1" in titulos[0]
    assert "Artículo 2" in titulos[1]

    # El contenido del primer artículo debe contener su texto
    assert "primer artículo de prueba" in articulos[0]["contenido"]
    assert "segundo artículo" in articulos[1]["contenido"]


def test_split_into_articles_sin_articulos_devuelve_documento_completo():
    texto = "Este texto no tiene artículos marcados."
    articulos = split_into_articles(texto)

    assert len(articulos) == 1
    assert articulos[0]["articulo"] == "DOCUMENTO_COMPLETO"
    assert "no tiene artículos" in articulos[0]["contenido"]
