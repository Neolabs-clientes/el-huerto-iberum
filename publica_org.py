#!/usr/bin/env python3
"""Mueve la demo al espacio de demos de clientes (Neolabs-clientes) y activa GitHub Pages.

Si la cuenta no puede crear repositorios en esa organizacion, deja el repo donde esta
y activa Pages alli, para no quedarnos sin demo publicada.
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

DEMO = Path('/home/davidos/clients/el-huerto-iberum')
OTRA = Path('/home/davidos/clients/divine-peluqueros')
NOMBRE = 'el-huerto-iberum'
ORG = 'Neolabs-clientes'


def datos_git():
    cfg = (OTRA / '.git' / 'config').read_text()
    m = re.search(r'https://x-access-token:([^@]+)@github\.com/([^/]+)/([^.\s]+)', cfg)
    if not m:
        sys.exit('sin token de referencia')
    return m.group(1), m.group(2), m.group(3)


def gh(token, metodo, ruta, datos=None):
    args = ['curl', '-s', '-m', '60', '-X', metodo,
            '-H', f'Authorization: Bearer {token}',
            '-H', 'Accept: application/vnd.github+json',
            '-H', 'X-GitHub-Api-Version: 2022-11-28']
    if datos is not None:
        args += ['-d', json.dumps(datos)]
    args.append('https://api.github.com' + ruta)
    r = subprocess.run(args, capture_output=True, text=True)
    try:
        return json.loads(r.stdout or '{}')
    except Exception:
        return {'crudo': r.stdout[:300]}


def activa_pages(token, cuenta, nombre):
    r = gh(token, 'POST', f'/repos/{cuenta}/{nombre}/pages',
           {'source': {'branch': 'main', 'path': '/'}})
    if r.get('html_url'):
        print('Pages activado:', r['html_url'], '| estado:', r.get('status'))
        return True
    r2 = gh(token, 'GET', f'/repos/{cuenta}/{nombre}/pages')
    if r2.get('html_url'):
        print('Pages ya estaba:', r2['html_url'], '| estado:', r2.get('status'))
        return True
    print('Pages no se pudo activar:', json.dumps(r)[:300])
    return False


def main():
    token, cuenta_otra, repo_otra = datos_git()
    print('token del espacio:', cuenta_otra, '| demo de referencia:', repo_otra)

    # 1) intento crear el repositorio en la organizacion de demos
    org_ok = False
    r = gh(token, 'GET', f'/repos/{ORG}/{NOMBRE}')
    if r.get('full_name'):
        print('ya existe en la organizacion:', r['full_name'])
        org_ok = True
    else:
        r = gh(token, 'POST', f'/orgs/{ORG}/repos', {
            'name': NOMBRE,
            'description': 'Web de El Huerto Iberum (Illescas) · vista previa de NEO Labs',
            'private': False,
            'has_issues': False, 'has_wiki': False, 'has_projects': False,
        })
        if r.get('full_name'):
            print('creado en la organizacion:', r['full_name'])
            org_ok = True
        else:
            print('no puedo crear en la organizacion:', json.dumps(r)[:220])

    destino = ORG if org_ok else 'magodago'
    clon = f'https://github.com/{destino}/{NOMBRE}.git'
    print('destino final:', destino)

    # 2) subir el contenido alli
    subprocess.run(['git', 'remote', 'remove', 'origin'], cwd=DEMO, capture_output=True, text=True)
    with_token = clon.replace('https://', f'https://x-access-token:{token}@')
    subprocess.run(['git', 'remote', 'add', 'origin', with_token], cwd=DEMO, capture_output=True, text=True)
    p = subprocess.run(['git', 'push', '-u', 'origin', 'main', '--force'], cwd=DEMO,
                       capture_output=True, text=True)
    print('push a', destino, ':', 'ok' if p.returncode == 0 else 'fallo')
    if p.returncode != 0:
        print((p.stderr or '')[-260:])

    # 3) activar Pages
    time.sleep(6)
    ok = activa_pages(token, destino, NOMBRE)

    # 4) si se creo en el sitio bueno, borro el repo de mi cuenta para no dejar duplicados
    if destino == ORG and ok:
        d = gh(token, 'DELETE', f'/repos/magodago/{NOMBRE}')
        print('borrado magodago/' + NOMBRE + ':', 'si' if not d.get('message') else d.get('message'))

    print('DIRECCION:', f'https://{destino.lower()}.github.io/{NOMBRE}/')


if __name__ == '__main__':
    main()
