#!/usr/bin/env python3
"""Folhas de contato com timecode, para analisar referencias, catalogar takes e revisar cortes.

Uso:
  python3 motor/folha_contato.py video.mp4 saida.jpg [--fps 1] [--colunas 10] [--largura 180] [--cortes]
  python3 motor/folha_contato.py --takes pasta_takes/ saida.jpg      (uma linha por take, 6 quadros cada)

--cortes  lista tambem os instantes de troca de cena (util para mapear o ritmo de uma referencia).
Takes 4K HEVC grandes: use --rapido (so quadros-chave, ~1 por segundo, bem mais rapido).
"""
import argparse, glob, os, subprocess, tempfile


def sheet(video, out, fps, cols, width, rapido=False):
    """Gera paginas saida_01.jpg, saida_02.jpg... com 5 linhas de quadros cada."""
    pre = ['-skip_frame', 'nokey'] if rapido else []
    vf = ('' if rapido else f'fps={fps},') + (f"scale={width}:-2,drawtext=text='%{{pts\\:hms}}':x=3:y=3:fontsize=14:"
                                               f"fontcolor=red:box=1,tile={cols}x5:padding=3")
    base, ext = os.path.splitext(out)
    cmd = ['ffmpeg', '-v', 'error', '-y'] + pre + ['-i', video, '-vf', vf] + (['-vsync', 'vfr'] if rapido else [])
    subprocess.run(cmd + [f'{base}_%02d{ext}'], check=True)


def cortes(video, limiar=0.12):
    r = subprocess.run(['ffmpeg', '-i', video, '-vf', f"select='gt(scene,{limiar})',showinfo", '-an', '-f', 'null', '-'],
                       capture_output=True, text=True)
    return [float(l.split('pts_time:')[1].split()[0]) for l in r.stderr.splitlines() if 'pts_time:' in l]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('entrada'); ap.add_argument('saida')
    ap.add_argument('--fps', type=float, default=1); ap.add_argument('--colunas', type=int, default=10)
    ap.add_argument('--largura', type=int, default=180); ap.add_argument('--cortes', action='store_true')
    ap.add_argument('--takes', action='store_true'); ap.add_argument('--rapido', action='store_true')
    a = ap.parse_args()
    if a.takes:
        tmp = tempfile.mkdtemp(); linhas = []
        for f in sorted(glob.glob(os.path.join(a.entrada, '*'))):
            if not f.lower().endswith(('.mov', '.mp4', '.m4v')):
                continue
            nome = os.path.splitext(os.path.basename(f))[0]
            dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f],
                                       capture_output=True, text=True).stdout)
            o = os.path.join(tmp, nome + '.jpg')
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-vf',
                            f"fps={6 / max(dur, 1):.4f},scale=-2:300,drawtext=text='{nome} %{{pts\\:hms}}':x=3:y=3:"
                            f"fontsize=13:fontcolor=red:box=1,tile=6x1:padding=3", '-frames:v', '1', o], check=True)
            linhas.append(o); print(f'{nome}: {dur:.1f}s')
        ins = sum([['-i', l] for l in linhas], [])
        subprocess.run(['ffmpeg', '-v', 'error', '-y'] + ins + ['-filter_complex',
                        ''.join(f'[{i}]scale=1800:-2[s{i}];' for i in range(len(linhas))) +
                        ''.join(f'[s{i}]' for i in range(len(linhas))) + f'vstack={len(linhas)}', a.saida], check=True)
    else:
        sheet(a.entrada, a.saida, a.fps, a.colunas, a.largura, a.rapido)
    if a.cortes:
        print('trocas de cena (s):', ' '.join(f'{c:.2f}' for c in cortes(a.entrada)))
    print('->', a.saida)


if __name__ == '__main__':
    main()
