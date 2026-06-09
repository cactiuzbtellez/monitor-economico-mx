import json, os, re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import feedparser
import urllib.request

TZ_MX = ZoneInfo("America/Mexico_City")

FEEDS = [
    {"fuente": "Expansión", "seccion": "Economía", "color": "#C8102E",
     "url": "https://expansion.mx/rss/economia"},
    {"fuente": "Expansión", "seccion": "Empresas", "color": "#C8102E",
     "url": "https://expansion.mx/rss/empresas"},
    {"fuente": "Expansión", "seccion": "Mercados", "color": "#C8102E",
     "url": "https://expansion.mx/rss/mercados-financieros"},
    {"fuente": "El Universal", "seccion": "Finanzas", "color": "#E87722",
     "url": "https://www.eluniversal.com.mx/rss/finanzas.xml"},
    {"fuente": "El Universal", "seccion": "Cartera", "color": "#E87722",
     "url": "https://www.eluniversal.com.mx/rss/cartera.xml"},
    {"fuente": "Reforma", "seccion": "Negocios", "color": "#2563EB",
     "url": "https://reforma.com/rss/negocios.xml"},
]

MAX_POR_FEED = 8
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}

def parsear_fecha(entry):
    try:
        t = entry.get("published_parsed") or entry.get("updated_parsed")
        if t:
            dt = datetime(*t[:6], tzinfo=timezone.utc).astimezone(TZ_MX)
            return dt.strftime("%d %b %Y, %H:%M hrs")
    except: pass
    return ""

def limpiar(texto):
    texto = re.sub(r"<[^>]+>", "", texto or "").strip()
    return texto[:200] + "…" if len(texto) > 200 else texto

def fetch_feed(cfg):
    noticias = []
    try:
        req = urllib.request.Request(cfg["url"], headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            contenido = resp.read()
        d = feedparser.parse(contenido)
        print(f"  status: {d.get('status','?')} | entries: {len(d.entries)}")
        for entry in d.entries[:MAX_POR_FEED]:
            noticias.append({
                "fuente":  cfg["fuente"],
                "seccion": cfg["seccion"],
                "color":   cfg["color"],
                "titulo":  entry.get("title", "").strip(),
                "resumen": limpiar(entry.get("summary", "")),
                "link":    entry.get("link", ""),
                "fecha":   parsear_fecha(entry),
            })
        print(f"  ✓ {cfg['fuente']} / {cfg['seccion']}: {len(noticias)} noticias")
    except Exception as e:
        print(f"  ✗ ERROR {cfg['fuente']} / {cfg['seccion']}: {e}")
    return noticias

def main():
    todas = []
    for cfg in FEEDS:
        print(f"\n→ {cfg['fuente']} / {cfg['seccion']}")
        todas.extend(fetch_feed(cfg))

    salida = {
        "actualizado": datetime.now(TZ_MX).strftime("%d/%m/%Y %H:%M hrs"),
        "total": len(todas),
        "noticias": todas,
    }
    os.makedirs("data", exist_ok=True)
    with open("data/noticias.json", "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)
    print(f"\n✅ noticias.json → {len(todas)} noticias")

if __name__ == "__main__":
    main()
