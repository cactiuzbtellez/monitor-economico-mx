# 📊 Monitor Económico MX

Dashboard de noticias en tiempo real de **El Financiero** y **El Economista**, desplegado en GitHub Pages y alimentado automáticamente via GitHub Actions cada hora.

---

## 🗂 Estructura del proyecto

```
├── index.html                        # Dashboard (GitHub Pages)
├── data/
│   └── noticias.json                 # Generado automáticamente por el Action
├── scripts/
│   └── fetch_rss.py                  # Script Python que parsea los RSS
└── .github/
    └── workflows/
        └── fetch-rss.yml             # GitHub Action (corre cada hora)
```


