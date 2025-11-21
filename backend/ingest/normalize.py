import re
from pathlib import Path

def basic_normalize(texto: str) -> str:
    """
    Normalización básica:
    - Convierte saltos de línea múltiples en uno solo.
    - Limpia espacios repetidos.
    - Elimina líneas totalmente vacías al inicio y final.
    """

    # Unificar saltos de línea tipo Windows/Mac
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")

    # Quitar caracteres de espacio raro
    texto = texto.replace("\u00a0", " ")  # espacio no separable

    # Eliminar espacios en blanco al inicio y fin de cada línea
    lineas = [line.strip() for line in texto.split("\n")]

    # Eliminar líneas totalmente vacías consecutivas (dejamos a lo sumo 1)
    salida = []
    empty_streak = 0
    for linea in lineas:
        if linea == "":
            empty_streak += 1
            if empty_streak > 1:
                continue
        else:
            empty_streak = 0
        salida.append(linea)

    texto = "\n".join(salida).strip()

    # Colapsar espacios múltiples dentro de una misma línea
    texto = re.sub(r"[ \t]+", " ", texto)

    return texto

def normalize_file(input_path: Path, output_path: Path | None = None) -> Path:
    """
    Lee un .txt, lo normaliza y guarda el resultado.
    Si no se da output_path, se guarda en data/processed con el mismo nombre.
    """
    raw = input_path.read_text(encoding="utf-8", errors="ignore")
    norm = basic_normalize(raw)

    if output_path is None:
        # Ej: data/raw/dof/2025-01-01/publicacion_001.txt
        # -> data/processed/dof/2025-01-01/publicacion_001.normalized.txt
        parts = list(input_path.parts)
        try:
            idx = parts.index("raw")
            parts[idx] = "processed"
        except ValueError:
            # si no encontramos "raw", lo metemos todo en data/processed
            processed_root = Path("data/processed")
            output_path = processed_root / input_path.name
        else:
            processed_root = Path(*parts[:-1])
            processed_root.mkdir(parents=True, exist_ok=True)
            stem = input_path.stem
            output_path = processed_root / f"{stem}.normalized.txt"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(norm, encoding="utf-8")
    return output_path

if __name__ == "__main__":
    # Ejemplo de uso manual:
    ejemplo = Path("data/raw/dof/ejemplo.txt")
    if ejemplo.exists():
        out = normalize_file(ejemplo)
        print(f"Archivo normalizado en: {out}")
    else:
        print("No se encontró data/raw/dof/ejemplo.txt para la prueba.")

