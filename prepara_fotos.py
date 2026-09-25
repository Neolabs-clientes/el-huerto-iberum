#!/usr/bin/env python3
"""Prepara las imagenes del cliente para la web: recorta, redimensiona y comprime.
Genera versiones grande y pequena de cada foto, mas el logo en blanco.
"""
from pathlib import Path

from PIL import Image, ImageOps

BASE = Path('/home/davidos/clients/el-huerto-iberum/assets')
SALIDA = BASE

# foto original -> (nombre base, ancho grande, ancho pequeno, recorte alto/ancho o None)
PLAN = [
    ('fachada.jpg', 'cartel', 2000, 900, None),
    ('local2.jpg', 'barra', 1600, 800, None),
    ('local1.jpg', 'langostinos', 1400, 700, None),
    ('plato1.jpg', 'calamares', 1200, 600, None),
    ('plato2.jpg', 'timbal', 1200, 600, None),
    ('terraza1.jpg', 'ensalada', 1200, 600, None),
]

def guarda(im, ruta, calidad=82):
    im.save(ruta, 'JPEG', quality=calidad, optimize=True, progressive=True)
    return ruta.stat().st_size // 1024

for origen, nombre, ancho_g, ancho_p, _ in PLAN:
    f = BASE / origen
    if not f.exists():
        print('FALTA', origen)
        continue
    im = Image.open(f).convert('RGB')
    im = ImageOps.exif_transpose(im)
    for ancho, sufijo in ((ancho_g, ''), (ancho_p, '-s')):
        if im.width <= ancho and sufijo == '-s':
            continue
        r = im.copy()
        r.thumbnail((ancho, ancho * 3), Image.LANCZOS)
        kb = guarda(r, SALIDA / f'{nombre}{sufijo}.jpg')
        print(f'{nombre}{sufijo}.jpg  {r.width}x{r.height}  {kb} KB')

# logo: ya viene en blanco y con transparencia
logo = Image.open(BASE / 'logo.png')
print('logo.png', logo.size, logo.mode, (BASE / 'logo.png').stat().st_size // 1024, 'KB')
print('cartel.jpg ancho real:', Image.open(SALIDA / 'cartel.jpg').size)
