#!/usr/bin/env python3
"""Gera legendas palavra a palavra + selos (ASS 1080x1920) a partir do plano.json e do words.json.

Uso: python3 motor/legendas.py plano.json words.json saida.ass

No plano:
  "audio": pecas de audio na ordem da timeline (define o mapa tempo-do-take -> tempo-do-video)
  "legendas": {"blocos": [{"fonte","ini","frases":[...]}], "enfase": [...], "enfase_por_fonte": {"C": [...]}, "corrigir": {...}}
  "selos": lista de {"tipo": "texto"|"contador", ...}; tempos podem ser numero (tempo do video)
           ou {"fonte": "M", "t": 6.64} (tempo do take, convertido automaticamente)
"""
import json, sys

p_plano, p_words, p_out = sys.argv[1:4]
plano = json.load(open(p_plano))
W = json.load(open(p_words))

# mapa das pecas de audio na timeline final
PECAS, t = [], 0.0
for a in plano['audio']:
    if 'silencio' in a:
        t += a['silencio']; continue
    PECAS.append((a['fonte'], a['ini'], a['ini'] + a['dur'], t)); t += a['dur']
FIM = sum(v['dur'] for v in plano['video'])


def out_time(src, tt):
    for tol in (0, 0.05):  # primeiro a peca que contem o tempo; folga so se nenhuma contiver
        for s, a, b, o in PECAS:
            if s == src and a - tol <= tt < b + tol:
                return o + (tt - a)
    raise ValueError(f'{src}@{tt} fora das pecas de audio')


def T(v):
    return out_time(v['fonte'], v['t']) if isinstance(v, dict) else float(v)


def ts(x):
    x = max(0, x); return f'{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}'


L = plano.get('legendas', {})
EMPH = {w.lower() for w in L.get('enfase', [])}
EMPH_F = {k: {w.lower() for w in v} for k, v in L.get('enfase_por_fonte', {}).items()}
FIX = L.get('corrigir', {})
Y_CAP = L.get('y', 1290)
events = []

# ---------- legendas ----------
for bloco in L.get('blocos', []):
    src, a = bloco['fonte'], bloco['ini']
    peca = next(pc for pc in PECAS if pc[0] == src and abs(pc[1] - a) < 0.01)
    b, o = peca[2], peca[3]
    ws = [w for w in W[src] if w[1] >= a - 0.02 and w[1] < b - 0.05]
    phrases, i = [], 0
    for fr in bloco['frases']:
        n = len(fr.split()); phrases.append(ws[i:i + n]); i += n
    if i != len(ws):
        sys.exit(f'Frases do bloco {src}@{a} somam {i} palavras, a fala tem {len(ws)}: {[w[0] for w in ws]}')
    for pi, ph in enumerate(phrases):
        nxt = out_time(src, phrases[pi + 1][0][1]) if pi + 1 < len(phrases) else o + (b - a)
        for k, w in enumerate(ph):
            st = out_time(src, w[1])
            en = out_time(src, ph[k + 1][1]) if k + 1 < len(ph) else min(out_time(src, w[2]) + 0.35, nxt)
            parts = []
            for ww in ph[:k + 1]:
                word = FIX.get(ww[0], ww[0])
                core = word.strip(',.!?').lower()
                if core in EMPH or core in EMPH_F.get(src, set()):
                    parts.append(r'{\fnPlayfair Display\i1\fs74}' + word + r'{\r}')
                else:
                    parts.append(word)
            pop = r'{\fscx108\fscy108\t(0,90,\fscx100\fscy100)}' if k == 0 else ''
            events.append((1, st, en, 'Cap', rf'{{\an5\pos(540,{Y_CAP})}}' + pop + ' '.join(parts)))

# ---------- selos ----------
GOLD = plano.get('cor_brilho', '&H8FD3FF&')
BLACK, ITAL = 'Inter Display Black', 'Playfair Display'
SOMBRA = r'\bord10\blur22\1a&HFF&\3c&H000000&\3a&H90&'
BRILHO = rf'\bord5\blur10\1a&H00&\3c{GOLD}\3a&H60&'


def selo_texto(s):
    st, en = T(s['ini']), T(s['fim']) if s.get('fim') != 'fim' else FIM - 0.05
    fi, fo = s.get('fade', [120, 200])
    for text, y, size in s['linhas']:
        base = rf'\an5\pos(540,{y})\fn{BLACK}\fs{size}\fad({fi},{fo})'
        anim = r'\fscx118\fscy118\t(0,220,\fscx100\fscy100)'
        events.append((0, st, en, 'Selo', '{' + base + anim + SOMBRA + '}' + text))
        events.append((1, st, en, 'Selo', '{' + base + anim + BRILHO + '}' + text))
        events.append((2, st, en, 'Selo', '{' + base + anim + r'\bord0\shad0' + '}' + text))


def selo_contador(s):
    st, en = T(s['ini']), T(s['fim'])
    alvo, y, sufixo, y2 = s['valor'], s['y'], s.get('apoio', ''), s.get('y_apoio', s['y'] + 110)
    n, dur, un = 15, 0.55, s.get('unidade', ' m²')
    for i in range(n + 1):
        a = st + dur * i / n
        b = st + dur * (i + 1) / n if i < n else en
        txt = f'{round(alvo * (i / n) ** 0.6):,}'.replace(',', '.') + un
        f = (100 if i == 0 else 0, 200 if i == n else 0)
        for layer, extra in [(0, SOMBRA), (1, rf'\bord5\blur10\3c{GOLD}\3a&H60&'), (2, r'\bord0\shad0')]:
            events.append((layer, a, b, 'Selo', rf'{{\an5\pos(540,{y})\fn{BLACK}\fs150\fad({f[0]},{f[1]}){extra}}}' + txt))
    if sufixo:
        for layer, extra in [(0, r'\bord8\blur18\1a&HFF&\3c&H000000&\3a&H90&'), (2, r'\bord0\shad0')]:
            events.append((layer, st + 0.15, en, 'Selo', rf'{{\an5\pos(540,{y2})\fn{ITAL}\i1\fs76\fad(200,200){extra}}}' + sufixo))


for s in plano.get('selos', []):
    (selo_contador if s['tipo'] == 'contador' else selo_texto)(s)

HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter SemiBold,66,&H00FFFFFF,&H00FFFFFF,&H70000000,&H00000000,0,0,0,0,100,100,0,0,1,3,0,5,60,60,0,1
Style: Selo,Inter Display Black,120,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,-1,0,1,0,0,5,20,20,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open(p_out, 'w') as fh:
    fh.write(HEAD)
    for layer, st, en, style, txt in sorted(events, key=lambda e: (e[1], e[0])):
        if en - st < 0.01:
            continue
        if style == 'Cap':
            txt = r'{\blur3}' + txt
        fh.write(f'Dialogue: {layer},{ts(st)},{ts(en)},{style},,0,0,0,,{txt}\n')
print(len(events), 'eventos ->', p_out)
