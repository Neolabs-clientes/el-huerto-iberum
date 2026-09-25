#!/usr/bin/env python3
"""Borra el repositorio duplicado que se creo por error en la cuenta personal."""
import json
import re
import subprocess
from pathlib import Path

cfg = Path('/home/davidos/.git-credentials').read_text()
m = re.search(r'https://[^:]*:([^@]+)@github\.com', cfg)
if not m:
    print('sin token en .git-credentials')
    raise SystemExit(0)
token = m.group(1)

r = subprocess.run(
    ['curl', '-s', '-m', '60', '-X', 'GET', '-H', f'Authorization: Bearer {token}',
     'https://api.github.com/user'], capture_output=True, text=True)
try:
    quien = json.loads(r.stdout).get('login')
except Exception:
    quien = None
print('ese token es de:', quien)

if quien == 'magodago':
    d = subprocess.run(
        ['curl', '-s', '-m', '60', '-X', 'DELETE', '-H', f'Authorization: Bearer {token}',
         'https://api.github.com/repos/magodago/el-huerto-iberum'], capture_output=True, text=True)
    print('borrado:', 'ok' if d.returncode == 0 and not d.stdout.strip() else d.stdout[:200])
else:
    print('no puedo borrarlo con este token, lo dejo (es publico pero sin Pages)')
