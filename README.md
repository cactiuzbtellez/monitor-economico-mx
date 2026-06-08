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

---

## 🚀 Cómo publicar paso a paso

### 1. Crear el repositorio en GitHub
- Ve a [github.com/new](https://github.com/new)
- Ponle nombre, ej: `monitor-economico-mx`
- Déjalo **público** (GitHub Pages gratis solo funciona en repos públicos con plan Free)
- **No** inicialices con README (subiremos los archivos manualmente)

### 2. Subir los archivos
```bash
git init
git add .
git commit -m "feat: dashboard monitor económico MX"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/monitor-economico-mx.git
git push -u origin main
```

### 3. Activar GitHub Pages
1. Ve a tu repo → **Settings** → **Pages**
2. En *Source* selecciona: **Deploy from a branch**
3. Branch: `main` / Folder: `/ (root)`
4. Guarda → en ~1 minuto tendrás tu URL:
   `https://TU_USUARIO.github.io/monitor-economico-mx/`

### 4. Dar permisos de escritura al Action
El Action necesita hacer `git push` para actualizar `noticias.json`:
1. Ve a **Settings** → **Actions** → **General**
2. Baja a *Workflow permissions*
3. Selecciona **Read and write permissions**
4. Guarda

### 5. Correr el Action por primera vez
1. Ve a **Actions** → `Fetch RSS Noticias Económicas`
2. Click en **Run workflow** → **Run workflow**
3. Espera ~30 segundos → verás `noticias.json` actualizado en `data/`
4. Recarga tu URL de GitHub Pages → aparecerán las noticias

---

## ⏱ Frecuencia de actualización
El Action corre automáticamente **cada hora** (cron `0 * * * *`).  
Si quieres más frecuencia, cambia a `*/30 * * * *` (cada 30 min) en `fetch-rss.yml`.

---

## 🖥 Embeber en Looker Studio (Data Studio)

1. Copia tu URL de GitHub Pages
2. En Looker Studio → **Añadir un elemento** → **URL embed** (o componente HTML)
3. Pega la URL
4. Ajusta el tamaño del iframe al área deseada

---

## ➕ Agregar más fuentes RSS

Edita `scripts/fetch_rss.py` y agrega entradas al array `FEEDS`:

```python
{
    "fuente": "Expansión",
    "seccion": "Economía",
    "color": "#7B2FBE",
    "url": "https://expansion.mx/rss/economia",
},
```

---

## 🛠 Dependencias Python
- `feedparser` — parseo de RSS
- `requests` — (incluido por si necesitas fetch directo)

Instaladas automáticamente por el GitHub Action via `pip install feedparser requests`.
