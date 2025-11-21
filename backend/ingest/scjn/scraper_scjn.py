from pathlib import Path
import time
import requests
from bs4 import BeautifulSoup

def fetch_html(url: str) -> str:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.text

def parse_tesis_page(html: str) -> str:
    """
    Extrae el texto completo de una tesis o jurisprudencia de la SCJN.
    Luego afinaremos para separar rubro, texto, considerandos, etc.
    """
    soup = BeautifulSoup(html, "lxml")
    texto = soup.get_text(separator="\n", strip=True)
    return texto

def save_text(content: str, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

def scrape_tesis_list(urls: list[str], nombre_lote: str = "lote_manual"):
    base_dir = Path("data/raw/scjn") / nombre_lote
    base_dir.mkdir(parents=True, exist_ok=True)

    for i, url in enumerate(urls, start=1):
        try:
            print(f"[SCJN] ({i}/{len(urls)}) {url}")
            html = fetch_html(url)
            texto = parse_tesis_page(html)
            filename = base_dir / f"tesis_{i:03d}.txt"
            save_text(texto, filename)
            time.sleep(1)
        except Exception as e:
            print(f"[SCJN] Error con {url}: {e}")

if __name__ == "__main__":
    # Aquí puedes poner 1-2 enlaces de tesis reales para probar:
    urls_ejemplo = [
        # "https://www2.scjn.gob.mx/SCJN/detalleTesis?Id=XXXXX",
    ]
    scrape_tesis_list(urls_ejemplo, nombre_lote="pruebas_iniciales")
