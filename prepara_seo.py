#!/usr/bin/env python3
"""Crea el favicon (monograma EH en oro sobre fondo oscuro) y los ficheros de SEO."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DESTINO = Path('/home/davidos/clients/el-huerto-iberum')
ASSETS = DESTINO / 'assets'

NEGRO = (10, 13, 11, 255)
ORO = (201, 162, 39, 255)

fuentes = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
]
fuente = None
for ruta in fuentes:
    if Path(ruta).exists():
        fuente = ruta
        break

for medida in (180, 32):
    im = Image.new('RGBA', (medida, medida), NEGRO)
    d = ImageDraw.Draw(im)
    # filo dorado interior para que respire
    d.rectangle([2, 2, medida - 3, medida - 3], outline=(201, 162, 39, 90), width=max(1, medida // 90))
    if fuente:
        f = ImageFont.truetype(fuente, int(medida * 0.52))
    else:
        f = ImageFont.load_default()
    texto = 'EH'
    caja = d.textbbox((0, 0), texto, font=f)
    x = (medida - (caja[2] - caja[0])) / 2 - caja[0]
    y = (medida - (caja[3] - caja[1])) / 2 - caja[1]
    d.text((x, y), texto, font=f, fill=ORO)
    nombre = 'favicon.png' if medida == 180 else 'favicon-32.png'
    im.save(ASSETS / nombre)
    print(nombre, im.size, (ASSETS / nombre).stat().st_size, 'bytes')

(DESTINO / 'robots.txt').write_text(
    'User-agent: *\n'
    'Allow: /\n'
    'Disallow: /legal.html\n\n'
    'Sitemap: https://el-huerto-iberum.neolabs.me/sitemap.xml\n'
)

(DESTINO / 'sitemap.xml').write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    '  <url>\n'
    '    <loc>https://el-huerto-iberum.neolabs.me/</loc>\n'
    '    <changefreq>monthly</changefreq>\n'
    '    <priority>1.0</priority>\n'
    '  </url>\n'
    '</urlset>\n'
)
print('robots.txt y sitemap.xml escritos')
