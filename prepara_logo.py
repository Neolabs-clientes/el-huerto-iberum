#!/usr/bin/env python3
"""Compone el logo del cliente sobre fondo oscuro para poder verlo y saca su paleta real."""
from collections import Counter

from PIL import Image

im = Image.open('/home/davidos/clients/el-huerto-iberum/assets/logo.png').convert('RGBA')
fondo = Image.new('RGBA', (im.width + 60, im.height + 60), (20, 26, 22, 255))
fondo.alpha_composite(im, (30, 30))
fondo.convert('RGB').save('/tmp/logo_sobre_negro.png')

opacos = [p for p in im.getdata() if p[3] > 60]
conteo = Counter((p[0] // 16 * 16, p[1] // 16 * 16, p[2] // 16 * 16) for p in opacos)
print('pixeles opacos:', len(opacos), 'de', im.width * im.height)
print('color mas comun:', ['#%02x%02x%02x' % k for k, _ in conteo.most_common(4)])
