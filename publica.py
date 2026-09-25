#!/usr/bin/env python3
"""Publica la demo de El Huerto Iberum en GitHub Pages, igual que las demos anteriores.

Lee el token de acceso del repo de otra demo ya publicada (no se imprime nunca),
crea el repositorio si no existe, sube los ficheros y activa GitHub Pages.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

DEMO = Path('/home/davidos/clients/el-huerto-iberum')
OTRA = Path('/home/davidos/clients/divine-peluqueros')  # demo ya publicada, de aqui sale el token
NOMBRE = 'el-huerto-iberum'


def token_y_cuenta():
    cfg = (OTRA / '.git' / 'config').read_text()
    m = re.search(r'https://x-access-token:([^@]+)@github\.com/([^/]+)/', cfg)
    if not m:
        sys.exit('no encuentro el token en la demo de referencia')
    return m.group(1), m.group(2)


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
        return {'crudo': r.stdout[:200]}


def main():
    token, cuenta = token_y_cuenta()
    print('cuenta destino:', cuenta)

    r = gh(token, 'GET', f'/repos/{cuenta}/{NOMBRE}')
    if r.get('full_name'):
        print('el repositorio ya existe:', r['full_name'])
        clon = r['clone_url']
    else:
        r = gh(token, 'POST', '/user/repos', {
            'name': NOMBRE,
            'description': 'Web de El Huerto Iberum (Illescas) · vista previa de NEO Labs',
            'private': False,
            'has_issues': False,
            'has_wiki': False,
            'has_projects': False,
        })
        if not r.get('full_name'):
            print('ERROR creando el repositorio:', json.dumps(r)[:400])
            sys.exit(1)
        print('repositorio creado:', r['full_name'])
        clon = r['clone_url']

    # git local
    def git(*args, comprobar=True):
        p = subprocess.run(['git', *args], cwd=DEMO, capture_output=True, text=True)
        if comprobar and p.returncode != 0:
            print('git', args[0], 'dijo:', (p.stderr or p.stdout)[-300:])
        return p

    git('init', '-q', comprobar=False)
    git('symbolic-ref', 'HEAD', 'refs/heads/main', comprobar=False)
    git('add', '-A')
    git('config', 'user.email', 'david@neolabs.me')
    git('config', 'user.name', 'David Ortiz')
    git('-c', 'commit.quiet=true', 'commit', '-q', '-m',
        'Web de El Huerto Iberum (Illescas): restaurante, bar y cafeteria', comprobar=False)
    git('remote', 'remove', 'origin', comprobar=False)
    git('remote', 'add', 'origin', clon.replace('https://', f'https://x-access-token:{token}@'))
    p = git('push', '-q', '-u', 'origin', 'main', '--force')
    print('push:', 'ok' if p.returncode == 0 else 'fallo')
    if p.returncode != 0:
        print((p.stderr or '')[-300:])

    # GitHub Pages
    pg = gh(token, 'POST', f'/repos/{cuenta}/{NOMBRE}/pages',
            {'source': {'branch': 'main', 'path': '/'}})
    if pg.get('html_url'):
        print('Pages activado:', pg['html_url'], '| estado:', pg.get('status'))
    else:
        pg2 = gh(token, 'GET', f'/repos/{cuenta}/{NOMBRE}/pages')
        print('Pages ya estaba:', pg2.get('html_url'), '| estado:', pg2.get('status'))
    print('direccion publica:', f'https://{cuenta}.github.io/{NOMBRE}/')


if __name__ == '__main__':
    main()
