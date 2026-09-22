# -*- coding: utf-8 -*-
# Generic i18n builder: python3 build_next.py PREV NEW PREVNAME NEWNAME NUM
# e.g.: python3 build_next.py sr bg "Српски" "Български" 56
import sys, re, os, json, importlib
sys.path.insert(0,'/home/sandbox/i18n')
prev, new, prevname, newname, num = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
PREV = vars(importlib.import_module(f'strings_{prev}'))[prev.upper()]
NEW  = vars(importlib.import_module(f'strings_{new}'))[new.upper()]
GLOSSES = importlib.import_module(f'glosses_{new}').GLOSSES
assert len(GLOSSES) == 145

ROOT = '/home/sandbox/portal'
BASE = ROOT + '/ingles/verbos-irregulares'
PATH = '/ingles/verbos-irregulares/'

# 1. index.html from previous language template
html = open(f'{BASE}/{prev}/index.html', encoding='utf-8').read()
# protect the footer's own-language <strong>NAME</strong> from string pairs that
# may collide with the language name (e.g. JV T_LANGS "Basa" inside "Basa Jawa")
html = html.replace(f'<strong>{prevname}</strong>', '\x01')
# protect the whole langnav block: display names can contain UI strings
# (e.g. jv T_LANGS 'Basa' inside 'Basa Jawa'), so pairs must not touch it
_m = re.search(r'<p class="langnav">.*?</p>', html, re.S)
assert _m, 'langnav not found'
langnav = _m.group(0)
html = html.replace(langnav, '\x02')
pairs = [(PREV[k], NEW[k]) for k in PREV if k in NEW and k != 'LANG' and PREV[k] and PREV[k] != NEW[k]]
pairs.sort(key=lambda p: -len(p[0]))
for idx, (a, b) in enumerate(pairs):
    if a not in html: print('WARN missing in template:', a[:60])
    html = html.replace(a, '\x00%d\x00' % idx)
for idx, (a, b) in enumerate(pairs):
    html = html.replace('\x00%d\x00' % idx, b)
html = html.replace(PATH + prev + '/', PATH + new + '/')
html = html.replace(f'html lang="{prev}"', f'html lang="{new}"')
# direction handling: strip inherited RTL, re-apply for RTL languages
RTL_LANGS = {'ar','fa','ur','ps','sd','tk','ug','he','ks'}
RTL_CSS = "html[dir=rtl] *{letter-spacing:normal}\nhtml[dir=rtl] th{text-align:right}\nhtml[dir=rtl] details .body ul{padding-left:0;padding-right:20px}\nhtml[dir=rtl] .setbar a{margin-left:0;margin-right:8px}\n"
html = html.replace(f'<html lang="{new}" dir="rtl">', f'<html lang="{new}">')
html = html.replace(RTL_CSS, '')
if new in RTL_LANGS:
    html = html.replace(f'<html lang="{new}">', f'<html lang="{new}" dir="rtl">')
    anchor = '/* pronunciacion */'
    if anchor in html and 'html[dir=rtl]' not in html:
        html = html.replace(anchor, RTL_CSS + '\n' + anchor, 1)
# restore langnav, translating only its label
langnav = langnav.replace(f'<p class="langnav">{PREV["T_LANGS"]}:', f'<p class="langnav">{NEW["T_LANGS"]}:')
assert NEW['T_LANGS'] in langnav, 'langnav label not swapped'
html = html.replace('\x02', langnav)
html = html.replace('\x01', f'<strong>{prevname}</strong>')
if f'<strong>{prevname}</strong> · <a href="{PATH}{new}/">{newname}</a></p>' in html:
    html = html.replace(f'<strong>{prevname}</strong> · <a href="{PATH}{new}/">{newname}</a></p>',
        f'<a href="{PATH}{prev}/">{prevname}</a> · <strong>{newname}</strong></p>')
else:
    html = html.replace(f'<strong>{prevname}</strong></p>',
        f'<a href="{PATH}{prev}/">{prevname}</a> · <strong>{newname}</strong></p>')
assert f'<strong>{prevname}</strong>' not in html, 'strong not swapped'
assert f'<strong>{newname}</strong>' in html and html.count(PATH + prev + '/') == 1, 'footer swap wrong'
assert f'lang="{new}"' in html
os.makedirs(f'{BASE}/{new}', exist_ok=True)
open(f'{BASE}/{new}/index.html', 'w', encoding='utf-8').write(html)

# 2. catalog.js from previous catalog (replace "es" in order)
cat = open(f'{BASE}/{prev}/catalog.js', encoding='utf-8').read()
i = 0
def repl(m):
    global i
    g = GLOSSES[i]; i += 1
    return '{"es":' + json.dumps(g, ensure_ascii=False) + ','
cat = re.sub(r'\{"es":"(?:[^"\\]|\\.)*",', repl, cat)
assert i == 145, f'only {i} glosses swapped'
open(f'{BASE}/{new}/catalog.js', 'w', encoding='utf-8').write(cat)

# 3. Footer link on every other page
count = 0
for d in os.listdir(BASE):
    p = os.path.join(BASE, d, 'index.html')
    if d == new or not os.path.isfile(p): continue
    s = open(p, encoding='utf-8').read()
    if PATH + new + '/' in s: continue
    if prevname + '</a></p>' in s:
        s = s.replace(prevname + '</a></p>', prevname + f'</a> · <a href="{PATH}{new}/">{newname}</a></p>')
        open(p, 'w', encoding='utf-8').write(s); count += 1
    elif f'<strong>{prevname}</strong></p>' in s:
        s = s.replace(f'<strong>{prevname}</strong></p>', f'<strong>{prevname}</strong> · <a href="{PATH}{new}/">{newname}</a></p>')
        open(p, 'w', encoding='utf-8').write(s); count += 1
p = BASE + '/index.html'
s = open(p, encoding='utf-8').read()
if PATH + new + '/' not in s and prevname + '</a></p>' in s:
    s = s.replace(prevname + '</a></p>', prevname + f'</a> · <a href="{PATH}{new}/">{newname}</a></p>')
    open(p, 'w', encoding='utf-8').write(s); count += 1
print('footer-updated pages:', count)

# 4. Counters N-1 -> N
for f in ['404.html', 'ingles/index.html', 'index.html']:
    p = ROOT + '/' + f
    s = open(p, encoding='utf-8').read()
    s = s.replace(f'{num-1} IDIOMAS', f'{num} IDIOMAS').replace(f'{num-1} idiomas', f'{num} idiomas')
    open(p, 'w', encoding='utf-8').write(s)

# 5. Rebuild inline VERBS_ALL (class list, 37) from the NEW catalog
p = f'{BASE}/{new}/index.html'
s = open(p, encoding='utf-8').read()
cat = open(f'{BASE}/{new}/catalog.js', encoding='utf-8').read()
j = cat.find('var VERBS_CATALOG=') + len('var VERBS_CATALOG=')
entries, _ = json.JSONDecoder().raw_decode(cat[j:])
by_inf = {e['inf']: e for e in entries}
m = re.search(r'(VERBS_ALL=\[)(.*?)(\];)', s, re.S)
infs = re.findall(r'"inf":"([^"]+)"', m.group(2))
assert len(infs) == 37
def ser(e):
    acc = e['acc']
    def a(k): return k + ':[' + ','.join(json.dumps(x, ensure_ascii=False) for x in acc[k]) + ']'
    return ('{"es":' + json.dumps(e['es'], ensure_ascii=False)
            + ',"inf":' + json.dumps(e['inf'])
            + ',"past":' + json.dumps(e['past'])
            + ',"pp":' + json.dumps(e['pp'])
            + ',"acc":{' + a('inf') + ',' + a('past') + ',' + a('pp') + '}}')
newarr = ',\n'.join(ser(by_inf[x]) for x in infs)
s = s[:m.start()] + m.group(1) + '\n' + newarr + '\n' + m.group(3) + s[m.end():]
open(p, 'w', encoding='utf-8').write(s)
print('done; VERBS_ALL rebuilt')
