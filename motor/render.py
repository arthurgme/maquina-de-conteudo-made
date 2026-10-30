#!/usr/bin/env python3
"""Renderiza um reel a partir de um plano.json.

Uso:
  python3 motor/render.py projetos/<slug>/plano.json --midia <pasta_com_os_takes> [--trabalho <pasta>] [--so-pecas v01,v02] [--forcar]

Etapas: pecas de video (sem audio) -> pecas de audio -> concat -> legendas/selos (ASS) -> final com tratamento de audio.
"""
import argparse, json, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(AQUI, 'fontes')


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(' '.join(cmd)); print(r.stderr[-2000:]); sys.exit(1)
    return r.stdout


def probe_dims(path):
    """Dimensoes como exibidas (considera rotacao do iPhone)."""
    out = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
               'stream=width,height:stream_side_data=rotation', '-of', 'json', path])
    s = json.loads(out)['streams'][0]
    w, h = s['width'], s['height']
    rot = 0
    for sd in s.get('side_data_list', []):
        rot = int(sd.get('rotation', 0) or 0)
    if abs(rot) == 90:
        w, h = h, w
    return w, h


def duracao(path):
    return float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]).strip())


class Fontes:
    """Resolve 'fonte' + tempo do take original para arquivo + tempo local (suporta trechos recortados)."""

    def __init__(self, cfg, midia):
        self.cfg, self.midia, self._dur = cfg, midia, {}

    def resolver(self, nome, ini, dur):
        f = self.cfg[nome]
        if 'trechos' in f:
            for t in f['trechos']:
                p = os.path.join(self.midia, t['arquivo'])
                if p not in self._dur:
                    self._dur[p] = duracao(p)
                if t['offset'] - 0.01 <= ini and ini + dur <= t['offset'] + self._dur[p] + 0.01:
                    return p, round(ini - t['offset'], 3)
            sys.exit(f'Nenhum trecho de {nome} cobre {ini}-{ini + dur}')
        return os.path.join(self.midia, f['arquivo']), ini


def peca_video(p, fontes, cor_base, pasta, forcar):
    out = os.path.join(pasta, f"{p['id']}.mp4")
    if os.path.exists(out) and not forcar:
        return out
    dur, vel = p['dur'], p.get('vel', 1)
    path, ss = fontes.resolver(p['fonte'], p['ini'], dur * vel)
    w, h = probe_dims(path)
    horiz = w > h
    z0, z1 = p.get('zoom', [1.0, 1.0])
    fx0, fx1 = p.get('fx', [.5, .5])
    fy = p.get('fy', .5)
    f = []
    if vel != 1:
        f.append(f'setpts={1 / vel}*PTS')
    if horiz:  # recorte vertical 9:16 com panoramica digital opcional
        cw = int(round(h * 9 / 16))
        f.append(f"crop={cw}:{h}:x='(iw-{cw})*({fx0}+({fx1}-{fx0})*t/{dur})':y=0")
    z = f'({z0}+({z1}-{z0})*t/{dur})'
    f.append(f"scale=w='trunc(1080*{z}/2)*2':h='trunc(1920*{z}/2)*2':eval=frame:flags=bicubic")
    f.append(f"crop=1080:1920:x='(iw-1080)*{fx0 if not horiz else .5}':y='(ih-1920)*{fy}'")
    f.append('fps=30,format=yuv420p,setsar=1')
    vf = ','.join(f) + ',' + cor_base + p.get('cor_extra', '')
    run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(dur * vel + 0.2), '-i', path, '-an',
         '-vf', vf, '-t', str(dur), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', out])
    return out


def peca_audio(i, a, fontes, pasta):
    out = os.path.join(pasta, f'a{i:02d}.wav')
    if 'silencio' in a:
        run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-t', str(a['silencio']), out])
        return out
    path, ss = fontes.resolver(a['fonte'], a['ini'], a['dur'])
    d = a['dur']
    run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(d), '-i', path, '-vn',
         '-af', f'aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.04,afade=t=out:st={d - 0.05}:d=0.05',
         '-c:a', 'pcm_s16le', out])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('plano'); ap.add_argument('--midia', required=True)
    ap.add_argument('--trabalho', default='/tmp/maquina'); ap.add_argument('--saida')
    ap.add_argument('--so-pecas'); ap.add_argument('--forcar', action='store_true')
    a = ap.parse_args()
    plano = json.load(open(a.plano))
    pasta = os.path.join(a.trabalho, 'pecas'); os.makedirs(pasta, exist_ok=True)
    fontes = Fontes(plano['fontes'], a.midia)
    cor = plano.get('cor', 'colortemperature=temperature=5200:mix=0.6,eq=contrast=1.05:saturation=1.12:gamma=1.02')

    pecas_v = plano['video']
    if a.so_pecas:
        ids = a.so_pecas.split(',')
        for p in pecas_v:
            if p['id'] in ids:
                print(peca_video(p, fontes, cor, pasta, True))
        return
    vids = []
    for p in pecas_v:
        vids.append(peca_video(p, fontes, cor, pasta, a.forcar)); print('ok', p['id'], flush=True)
    auds = [peca_audio(i, x, fontes, pasta) for i, x in enumerate(plano['audio'], 1)]

    lv, la = os.path.join(a.trabalho, 'v.txt'), os.path.join(a.trabalho, 'a.txt')
    open(lv, 'w').writelines(f"file '{v}'\n" for v in vids)
    open(la, 'w').writelines(f"file '{x}'\n" for x in auds)
    vcat, acat = os.path.join(a.trabalho, 'video_cat.mp4'), os.path.join(a.trabalho, 'audio_cat.wav')
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lv, '-c', 'copy', vcat])
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', la, '-c', 'copy', acat])

    # legendas e selos
    ass = os.path.join(a.trabalho, 'legendas.ass')
    words = os.path.join(os.path.dirname(os.path.abspath(a.plano)), 'words.json')
    run([sys.executable, os.path.join(AQUI, 'legendas.py'), a.plano, words, ass])

    total = sum(p['dur'] for p in pecas_v)
    fim = plano.get('fade_final', 0.55)
    saida = a.saida or os.path.join(a.trabalho, f"{plano['projeto']} - corte.mp4")
    af = plano.get('audio_final', 'highpass=f=80,afftdn=nf=-30,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=200,'
                                  'loudnorm=I=-14:TP=-1.5:LRA=9')
    run(['ffmpeg', '-v', 'error', '-y', '-i', vcat, '-i', acat,
         '-vf', f'ass={ass}:fontsdir={FONTES},fade=t=out:st={total - fim:.2f}:d={fim}',
         '-af', f'{af},afade=t=out:st={total - fim:.2f}:d={fim}', '-ar', '48000',
         '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
         '-movflags', '+faststart', '-t', f'{total:.3f}', saida])
    print('SAIDA', saida, duracao(saida))


if __name__ == '__main__':
    main()
