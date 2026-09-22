# -*- coding: utf-8 -*-
import sys, re, os
sys.path.insert(0,'/home/sandbox/i18n')
from strings_zu import ZU as IG
from strings_sr import SR as ZU
from glosses_sr import GLOSSES

ROOT = '/home/sandbox/portal'
BASE = ROOT + '/ingles/verbos-irregulares'

# 1. Build zu/index.html from ig template
html = open(BASE + '/zu/index.html', encoding='utf-8').read()
pairs = [(IG[k], ZU[k]) for k in IG if k in ZU and k != 'LANG' and IG[k] and IG[k] != ZU[k]]
pairs.sort(key=lambda p: -len(p[0]))
for a, b in pairs:
    if a not in html:
        print('WARN missing in template:', a[:60])
    html = html.replace(a, b)
html = html.replace('/ingles/verbos-irregulares/zu/', '/ingles/verbos-irregulares/sr/')
html = html.replace('html lang="zu"', 'html lang="sr"')
html = html.replace('<strong>Zulu</strong></p>',
    '<a href="/ingles/verbos-irregulares/zu/">Zulu</a> · <strong>Српски</strong></p>')
assert '<strong>Zulu</strong>' not in html, 'strong not swapped'
assert '<strong>Српски</strong>' in html and html.count('/zu/') == 1, 'footer swap wrong'
assert 'lang="sr"' in html
os.makedirs(BASE + '/sr', exist_ok=True)
open(BASE + '/sr/index.html', 'w', encoding='utf-8').write(html)

# 2. Build zu/catalog.js from ig catalog (replace "es" in order)
cat = open(BASE + '/zu/catalog.js', encoding='utf-8').read()
i = 0
def repl(m):
    global i
    g = GLOSSES[i]; i += 1
    return '{"es":' + __import__('json').dumps(g, ensure_ascii=False) + ','
cat = re.sub(r'\{"es":"(?:[^"\\]|\\.)*",', repl, cat)
assert i == 145, f'only {i} glosses swapped'
open(BASE + '/sr/catalog.js', 'w', encoding='utf-8').write(cat)

# 3. Footer link on every other page
count = 0
for d in os.listdir(BASE):
    p = os.path.join(BASE, d, 'index.html')
    if d == 'sr' or not os.path.isfile(p): continue
    s = open(p, encoding='utf-8').read()
    if '/sr/' in s: continue
    if 'Zulu</a></p>' in s:
        s = s.replace('Zulu</a></p>', 'Zulu</a> · <a href="/ingles/verbos-irregulares/sr/">Српски</a></p>')
        open(p, 'w', encoding='utf-8').write(s); count += 1
    elif '<strong>Zulu</strong></p>' in s:
        s = s.replace('<strong>Zulu</strong></p>', '<strong>Zulu</strong> · <a href="/ingles/verbos-irregulares/sr/">Српски</a></p>')
        open(p, 'w', encoding='utf-8').write(s); count += 1
p = BASE + '/index.html'
s = open(p, encoding='utf-8').read()
if '/zu/' not in s and 'Zulu</a></p>' in s:
    s = s.replace('Zulu</a></p>', 'Zulu</a> · <a href="/ingles/verbos-irregulares/sr/">Српски</a></p>')
    open(p, 'w', encoding='utf-8').write(s); count += 1
print('footer-updated pages:', count)

# 4. Counters 53 -> 54
for f in ['404.html', 'ingles/index.html', 'index.html']:
    p = ROOT + '/' + f
    s = open(p, encoding='utf-8').read()
    s = s.replace('54 IDIOMAS', '55 IDIOMAS').replace('54 idiomas', '55 idiomas')
    open(p, 'w', encoding='utf-8').write(s)
print('done')

# 5. Rebuild inline VERBS_ALL (class list, 37) from the NEW catalog:
# template substitution does not touch VERBS_ALL, so without this step
# class mode keeps the previous language's glosses.
import json as _json
def _rebuild_verbs_all(lang):
    p = BASE + '/' + lang + '/index.html'
    s = open(p, encoding='utf-8').read()
    cat = open(BASE + '/' + lang + '/catalog.js', encoding='utf-8').read()
    i = cat.find('var VERBS_CATALOG=') + len('var VERBS_CATALOG=')
    entries, _ = _json.JSONDecoder().raw_decode(cat[i:])
    by_inf = {e['inf']: e for e in entries}
    m = re.search(r'(VERBS_ALL=\[)(.*?)(\];)', s, re.S)
    infs = re.findall(r'"inf":"([^"]+)"', m.group(2))
    assert len(infs) == 37
    def ser(e):
        acc = e['acc']
        def a(k): return k + ':[' + ','.join(_json.dumps(x, ensure_ascii=False) for x in acc[k]) + ']'
        return ('{"es":' + _json.dumps(e['es'], ensure_ascii=False)
                + ',"inf":' + _json.dumps(e['inf'])
                + ',"past":' + _json.dumps(e['past'])
                + ',"pp":' + _json.dumps(e['pp'])
                + ',"acc":{' + a('inf') + ',' + a('past') + ',' + a('pp') + '}}')
    newarr = ',\n'.join(ser(by_inf[x]) for x in infs)
    s = s[:m.start()] + m.group(1) + '\n' + newarr + '\n' + m.group(3) + s[m.end():]
    open(p, 'w', encoding='utf-8').write(s)
_rebuild_verbs_all('sr')
print('VERBS_ALL rebuilt')
