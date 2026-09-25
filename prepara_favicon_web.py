#!/usr/bin/env python3
"""Anade el favicon a las dos paginas."""
from pathlib import Path

BASE = Path('/home/davidos/clients/el-huerto-iberum')
ENLACES = (
    '<link rel="icon" href="assets/favicon-32.png" sizes="32x32">\n'
    '<link rel="apple-touch-icon" href="assets/favicon.png">\n'
)

for pagina in ('index.html', 'legal.html'):
    f = BASE / pagina
    t = f.read_text()
    if 'favicon-32.png' in t:
        print(pagina, 'ya lo tenia')
        continue
    t = t.replace('<link rel="stylesheet" href="styles.css">',
                  ENLACES + '<link rel="stylesheet" href="styles.css">', 1)
    f.write_text(t)
    print(pagina, 'favicon anadido')
