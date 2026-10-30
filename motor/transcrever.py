#!/usr/bin/env python3
"""Transcreve takes com marcacao de inicio e fim de cada palavra (faster-whisper).

Uso:
  python3 motor/transcrever.py saida/words.json M=takes/fala-principal.MOV C=takes/cta.MOV [--modelo medium] [--contexto "Condominio Malibu, area construida"]

Gera {"M": [[palavra, inicio, fim], ...], "C": [...]} com tempos do take original.
Observacoes:
  - Passa o audio como array numpy (passar o caminho quebra com algumas versoes do pacote av).
  - Confira numeros e nomes proprios: o modelo pode errar (ex.: "830 de area construida").
"""
import argparse, json, subprocess
import numpy as np


def carregar(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vn', '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('saida'); ap.add_argument('fontes', nargs='+', help='NOME=arquivo')
    ap.add_argument('--modelo', default='medium'); ap.add_argument('--contexto', default='')
    a = ap.parse_args()
    from faster_whisper import WhisperModel
    m = WhisperModel(a.modelo, compute_type='int8')
    out = {}
    for item in a.fontes:
        nome, path = item.split('=', 1)
        segs, _ = m.transcribe(carregar(path), language='pt', word_timestamps=True, initial_prompt=a.contexto or None)
        out[nome] = [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for s in segs for w in s.words]
        print(nome, ' '.join(f'{w}[{i}-{f}]' for w, i, f in out[nome]))
    json.dump(out, open(a.saida, 'w'), ensure_ascii=False)
    print('->', a.saida)


if __name__ == '__main__':
    main()
