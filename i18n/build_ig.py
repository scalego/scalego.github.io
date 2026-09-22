# -*- coding: utf-8 -*-
import sys, re, os
sys.path.insert(0,'/home/sandbox/i18n')
from strings_ig import IG
from glosses_ig import GLOSSES

YO = {
"T_DESC":"Kọ́ àwọn ọ̀rọ̀-iṣe aìdéédéé èdè Gẹ̀ẹ́sì: ìbéèrè àríyànjiyàn, àyẹ̀wò lẹ́sẹ̀kẹsẹ̀, àti tábìlì ọ̀rọ̀-iṣe kíkún.",
"T_OGDESC":"Kọ́ àwọn ọ̀rọ̀-iṣe aìdéédéé èdè Gẹ̀ẹ́sì pẹ̀lú ìbéèrè àríyànjiyàn, àyẹ̀wò lẹ́sẹ̀kẹsẹ̀, àti tábìlì kíkún.",
"T_TITLE":"Kọ́ Gẹ̀ẹ́sì · Àwọn Ọ̀rọ̀-Iṣe Aìdéédéé",
"T_BRAND":"Kọ́ Gẹ̀ẹ́sì",
"T_SUB":"Àwọn Ọ̀rọ̀-Iṣe Aìdéédéé",
"T_INTRO":"Ṣe àdáṣe pẹ̀lú àwọn ìbéèrè àríyànjiyàn: kọ fọ́ọ̀mù tó pé kí o sì rí lẹ́sẹ̀kẹsẹ̀ bóyá ìdáhùn rẹ̀ dára. Ọ̀rọ̀-iṣe tí o ṣe àṣìṣe lórí á padà dé nígbà mìíràn.",
"T_SECTIONS":"Àwọn apá",
"T_TAB_PRACTICE":"Ìdánwò",
"T_TAB_REVIEW":"Ṣàyẹ̀wò Àkójọ",
"T_TAB_CREATE":"Ṣẹ̀dá Àkójọ",
"T_IPA_SUMMARY":"Kí ni ìtumọ̀ àwọn àmì /.../ (ìpè)",
"T_IPA_P1A":"Àwọn àmì tó wà láàrín àwọn síláàṣì, bí àpẹẹrẹ /ɡəʊ/, ",
"T_IPA_P1B":"kíkọ ìpè sáyẹ́nsì (IPA)",
"T_IPA_P1C":" ni: wọ́n fi hàn bí a ṣe ń pe ọ̀rọ̀ náà ní ",
"T_IPA_P1D":"Gẹ̀ẹ́sì Brítíìṣì",
"T_IPA_P1E":", ohùn kọ̀ọ̀kan.",
"T_IPA_L1":"ˈ fi hàn sílíbù tí a ń tẹ̀ lé lọ́kàn: /bɪˈɡɪn/ a ń pe é bi-GIN.",
"T_IPA_L2":"ː mú fáàsìlẹ̀ gùn: /iː/ jẹ́ \"i\" gígùn.",
"T_IPA_L3":"/ə/ jẹ́ fáàsìlẹ̀ láàárín tó gbajúmọ̀ jùlọ ní Gẹ̀ẹ́sì, bí \"a\" nínú ọ̀rọ̀ \"about\".",
"T_IPA_L4":"Bí àwọn àmì wọ̀nyí bá ṣòro fún ọ, ò títí: tẹ bọ́tìnnì 🔊 kí o sì gbọ́ ọ̀rọ̀ náà.",
"T_STATS_Q":"Ìbéèrè: ",
"T_STATS_OK":" · Tó pé: ",
"T_STATS_BAD":" · Àṣìṣe: ",
"T_RESTART":"Tún bẹ̀rẹ̀",
"T_ANSWER_PH":"Ìdáhùn rẹ ní Gẹ̀ẹ́sì",
"T_CHECK":"Ṣàyẹ̀wò",
"T_NEXT":"Ìbéèrè tókàn",
"T_PROGRESS":"Ìlòsíwájú rẹ̀ wà nínú ìjàwáde yìí nìkan: bí o bá pa á tàbí tún ṣí i, gbogbo rẹ̀ á padà.",
"T_CORR_SUMMARY":"Àtúnṣe ìdánwò",
"T_SEARCH_LABEL":"Wá ọ̀rọ̀-iṣe",
"T_SEARCH_PH":"Wá ní Gẹ̀ẹ́sì (àp. make, go, went)",
"T_TH_GLOSS":"Ìtumọ̀",
"T_TH_INF":"Ìbẹ̀rẹ̀",
"T_EMPTY":"Kò sí ọ̀rọ̀-iṣe tó bá wíwa mu.",
"T_CL_INTRO":"Yan àwọn ọ̀rọ̀-iṣe kí o sì dàwọ́ ọ́nà náà ṣẹ́: ẹnikẹ́ni tó bá ṣí i á ṣiṣẹ́ pẹ̀lú àwọn ìyàn rẹ nìkan, pẹ̀lú ohùn àti kíkọ ìpè.",
"T_CL_FILTER_PH":"Ṣẹ́ àwọn ọ̀rọ̀-iṣe (àp. eat, go, write)",
"T_CL_ALL":"Yan gbogbo wọn",
"T_CL_NONE":"Yọ ìyàn",
"T_CL_COPY":"Dàwọ́ ọ́nà àkójọ",
"T_FOOTER":"Raúl ló ṣe é · ",
"T_LANGS":"Àwọn èdè",
"J_PRON_PAST":"past:'Fọ́ọ̀mù àtijọ́'",
"J_OF":" ọ̀rọ̀-iṣe:",
"J_OF2":" ti ọ̀rọ̀-iṣe ",
"J_IS":" ni ",
"J_CLASS_CHIP":"'Àkójọ kíláàsì · '+VERBS.length+' ọ̀rọ̀-iṣe'",
"J_GOTO_CAT":"' · <a href=\"#l=todos\">Kátálógì kíkún ('+VERBS_CATALOG.length+')</a>'",
"J_CAT_CHIP":"'Kátálógì kíkún · '+VERBS.length+' ọ̀rọ̀-iṣe · <a href=\"/ingles/verbos-irregulares/yo/\">Padà sí àkójọ kíláàsì</a>'",
"J_CUSTOM_CHIP":"'Àkójọ ìyàn rẹ · '+VERBS.length+' ọ̀rọ̀-iṣe · <a href=\"/ingles/verbos-irregulares/yo/\">Padà sí àkójọ kíláàsì</a>'",
"J_MARK_ONE":"\"Yan ó kéré jù ọ̀rọ̀-iṣe kan.\"",
"J_COPIED":"\"A ti dàwọ́ ọ́nà: \"+sel.length+\" ọ̀rọ̀-iṣe.\"",
"J_CORRECT":"Tó pé.",
"J_WRONG":"Kò pé.",
"J_YOUWROTE":"'O kọ \"'+input.value.trim()+'\". '",
"J_WILLRETURN":". Á tún padà dé.",
"J_FB_BODY":"return FORM_LABELS[f]+' ti ọ̀rọ̀-iṣe '+gloss+' ni <b>'+form+'</b>';",
"J_LISTEN":'aria-label="Gbọ́: ',
}

ROOT = '/home/sandbox/portal'
BASE = ROOT + '/ingles/verbos-irregulares'

# 1. Build ig/index.html from yo template
html = open(BASE + '/yo/index.html', encoding='utf-8').read()
pairs = [(YO[k], IG[k]) for k in YO if k in IG and YO[k] and YO[k] != IG[k]]
pairs.sort(key=lambda p: -len(p[0]))
for a, b in pairs:
    if a not in html:
        print('WARN missing in template:', a[:60])
    html = html.replace(a, b)
html = html.replace('/ingles/verbos-irregulares/yo/', '/ingles/verbos-irregulares/ig/')
html = html.replace('html lang="yo"', 'html lang="ig"')
html = html.replace('<strong>Yorùbá</strong></p>',
    '<a href="/ingles/verbos-irregulares/yo/">Yorùbá</a> · <strong>Igbo</strong></p>')
assert '<strong>Yorùbá</strong>' not in html, 'strong not swapped'
assert '<strong>Igbo</strong>' in html and html.count('/yo/') == 1, 'footer swap wrong'
assert 'lang="ig"' in html
os.makedirs(BASE + '/ig', exist_ok=True)
open(BASE + '/ig/index.html', 'w', encoding='utf-8').write(html)

# 2. Build ig/catalog.js from yo catalog (replace "es" in order)
cat = open(BASE + '/yo/catalog.js', encoding='utf-8').read()
i = 0
def repl(m):
    global i
    g = GLOSSES[i]; i += 1
    return '{"es":' + __import__('json').dumps(g, ensure_ascii=False) + ','
cat = re.sub(r'\{"es":"(?:[^"\\]|\\.)*",', repl, cat)
assert i == 145, f'only {i} glosses swapped'
open(BASE + '/ig/catalog.js', 'w', encoding='utf-8').write(cat)

# 3. Footer link on every other page
count = 0
for d in os.listdir(BASE):
    p = os.path.join(BASE, d, 'index.html')
    if d == 'ig' or not os.path.isfile(p): continue
    s = open(p, encoding='utf-8').read()
    if '/ig/' in s: continue
    if 'Yorùbá</a></p>' in s:
        s = s.replace('Yorùbá</a></p>', 'Yorùbá</a> · <a href="/ingles/verbos-irregulares/ig/">Igbo</a></p>')
        open(p, 'w', encoding='utf-8').write(s); count += 1
p = BASE + '/index.html'
s = open(p, encoding='utf-8').read()
if '/ig/' not in s and 'Yorùbá</a></p>' in s:
    s = s.replace('Yorùbá</a></p>', 'Yorùbá</a> · <a href="/ingles/verbos-irregulares/ig/">Igbo</a></p>')
    open(p, 'w', encoding='utf-8').write(s); count += 1
print('footer-updated pages:', count)

# 4. Counters 52 -> 53
for f in ['404.html', 'ingles/index.html', 'index.html']:
    p = ROOT + '/' + f
    s = open(p, encoding='utf-8').read()
    s = s.replace('52 IDIOMAS', '53 IDIOMAS').replace('52 idiomas', '53 idiomas')
    open(p, 'w', encoding='utf-8').write(s)
print('done')
