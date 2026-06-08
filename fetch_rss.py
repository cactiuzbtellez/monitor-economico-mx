"""
fetch_rss.py
Descarga los RSS feeds de El Financiero y El Economista
y genera data/noticias.json para el dashboard.
"""

import json
import os
from datetime import datetime, timezone
import feedparser

# ── Fuentes RSS ────────────────────────────────────────────────────────────────
FEEDS = [
    {
        "fuente": "El Financiero",
        "seccion": "Economía",
        "color": "#C8102E",
        "url": "https://www.elfinanciero.com.mx/arc/outboundfeeds/rss/category/economia/",
    },
    {
        "fuente": "El Financiero",
        "seccion": "Mercados",
        "color": "#C8102E",
        "url": "https://www.elfinanciero.com.mx/arc/outboundfeeds/rss/category/mercados/",
    },
    {
        "fuente": "El Financiero",
        "seccion": "Empresas",
        "color": "#C8102E",
        "url": "https://www.elfinanciero.com.mx/arc/outboundfeeds/rss/category/empresas/",
    },
    {
        "fuente": "El Economista",
        "seccion": "Finanzas",
        "color": "#E87722",
        "url": "https://www.eleconomista.com.mx/rss/finanzas/",
    },
    {
        "fuente": "El Economista",
        "seccion": "Mercados",
        "color": "#E87722",
        "url": "https://www.eleconomista.com.mx/rss/mercados/",
    },
    {
        "fuente": "El Economista",
        "seccion": "Tecnología",
        "color": "#E87722",
        "url": "https://www.eleconomista.com.mx/rss/tecnologia/",
    },
]

MAX_POR_FEED = 8   # Noticias máximas por sección


def parsear_fecha(entry):
    """Extrae fecha legible del entry RSS."""
    try:
        t = entry.get("published_parsed") or entry.get("updated_parsed")
        if t:
            dt = datetime(*t[:6], tzinfo=timezone.utc)
            return dt.strftime("%d %b %Y, %H:%M UTC")
    except Exception:
        pass
    return ""


def limpiar_resumen(texto: str) -> str:
    """Elimina HTML básico y trunca a 200 caracteres."""
    import re
    texto = re.sub(r"<[^>]+>", "", texto or "")
    texto = texto.strip()
    return texto[:200] + "…" if len(texto) > 200 else texto


def fetch_feed(feed_cfg: dict) -> list:
    noticias = []
    try:
        d = feedparser.parse(feed_cfg["url"])
        for entry in d.entries[:MAX_POR_FEED]:
            noticias.append({
                "fuente":  feed_cfg["fuente"],
                "seccion": feed_cfg["seccion"],
                "color":   feed_cfg["color"],
                "titulo":  entry.get("title", "Sin título").strip(),
                "resumen": limpiar_resumen(entry.get("summary", "")),
                "link":    entry.get("link", ""),
                "fecha":   parsear_fecha(entry),
            })
        print(f"  ✓ {feed_cfg['fuente']} / {feed_cfg['seccion']}: {len(noticias)} noticias")
    except Exception as e:
        print(f"  ✗ Error en {feed_cfg['url']}: {e}")
    return noticias


def main():
    todas = []
    print("Descargando feeds RSS…")
    for cfg in FEEDS:
        todas.extend(fetch_feed(cfg))

    salida = {
        "actualizado": datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC"),
        "total": len(todas),
        "noticias": todas,
    }

    os.makedirs("data", exist_ok=True)
    with open("data/noticias.json", "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    print(f"\nGenerado data/noticias.json → {len(todas)} noticias totales")


if __name__ == "__main__":
    main()
