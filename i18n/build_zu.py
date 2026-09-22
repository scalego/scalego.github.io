# -*- coding: utf-8 -*-
import sys, re, os
sys.path.insert(0,'/home/sandbox/i18n')
from strings_ig import IG
from strings_zu import ZU
from glosses_zu import GLOSSES

ROOT = '/home/sandbox/portal'
BASE = ROOT + '/ingles/verbos-irregulares'

# 1. Build zu/index.html from ig template
html = open(BASE + '/ig/index.html', encoding='utf-8').read()
pairs = [(IG[k], ZU[k]) for k in IG if k in ZU and IG[k] and IG[k] != ZU[k]]
pairs.sort(key=lambda p: -len(p[0]))
for a, b in pairs:
    if a not in html:
        print('WARN missing in template:', a[:60])
    html = html.replace(a, b)
html = html.replace('/ingles/verbos-irregulares/ig/', '/ingles/verbos-irregulares/zu/')
html = html.replace('html lang="ig"', 'html lang="zu"')
html = html.replace('<strong>Igbo</strong></p>',
    '<a href="/ingles/verbos-irregulares/ig/">Igbo</a> · <strong>Zulu</strong></p>')
assert '<strong>Igbo</strong>' not in html, 'strong not swapped'
assert '<strong>Zulu</strong>' in html and html.count('/ig/') == 1, 'footer swap wrong'
assert 'lang="zu"' in html
os.makedirs(BASE + '/zu', exist_ok=True)
open(BASE + '/zu/index.html', 'w', encoding='utf-8').write(html)

# 2. Build zu/catalog.js from ig catalog (replace "es" in order)
cat = open(BASE + '/ig/catalog.js', encoding='utf-8').read()
i = 0
def repl(m):
    global i
    g = GLOSSES[i]; i += 1
    return '{"es":' + __import__('json').dumps(g, ensure_ascii=False) + ','
cat = re.sub(r'\{"es":"(?:[^"\\]|\\.)*",', repl, cat)
assert i == 145, f'only {i} glosses swapped'
open(BASE + '/zu/catalog.js', 'w', encoding='utf-8').write(cat)

# 3. Footer link on every other page
count = 0
for d in os.listdir(BASE):
    p = os.path.join(BASE, d, 'index.html')
    if d == 'zu' or not os.path.isfile(p): continue
    s = open(p, encoding='utf-8').read()
    if '/zu/' in s: continue
    if 'Igbo</a></p>' in s:
        s = s.replace('Igbo</a></p>', 'Igbo</a> · <a href="/ingles/verbos-irregulares/zu/">Zulu</a></p>')
        open(p, 'w', encoding='utf-8').write(s); count += 1
    elif '<strong>Igbo</strong></p>' in s:
        s = s.replace('<strong>Igbo</strong></p>', '<strong>Igbo</strong> · <a href="/ingles/verbos-irregulares/zu/">Zulu</a></p>')
        open(p, 'w', encoding='utf-8').write(s); count += 1
p = BASE + '/index.html'
s = open(p, encoding='utf-8').read()
if '/zu/' not in s and 'Igbo</a></p>' in s:
    s = s.replace('Igbo</a></p>', 'Igbo</a> · <a href="/ingles/verbos-irregulares/zu/">Zulu</a></p>')
    open(p, 'w', encoding='utf-8').write(s); count += 1
print('footer-updated pages:', count)

# 4. Counters 53 -> 54
for f in ['404.html', 'ingles/index.html', 'index.html']:
    p = ROOT + '/' + f
    s = open(p, encoding='utf-8').read()
    s = s.replace('53 IDIOMAS', '54 IDIOMAS').replace('53 idiomas', '54 idiomas')
    open(p, 'w', encoding='utf-8').write(s)
print('done')
