#!/usr/bin/env python3
"""Sugere pontos de corte no silencio mais proximo (minimo de energia) dentro de uma janela.

Uso:
  python3 motor/cortes.py takes/fala-principal.MOV 3.78-3.98 12.2-12.6 14.0-14.33

Para cada janela inicio-fim (segundos do take), mostra o instante de menor energia e o nivel em dB.
Nivel abaixo de ~-60 dB = silencio limpo. Acima de ~-40 dB = corte dentro de fala (usar fade ou escolher outra janela).
Dica: monte as janelas em volta dos limites das palavras do words.json (fim da ultima palavra que fica, inicio da proxima).
"""
import subprocess, sys
import numpy as np


def envelope(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vn', '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                         capture_output=True, check=True).stdout
    f = np.frombuffer(raw, np.int16).astype(np.float32)
    return np.sqrt(np.convolve(f ** 2, np.ones(480) / 480, 'same'))[::160]  # janela 30 ms, passo 10 ms


def main():
    env = envelope(sys.argv[1])
    for jan in sys.argv[2:]:
        a, b = (float(x) for x in jan.split('-'))
        i0, i1 = int(a * 100), int(b * 100)
        i = i0 + int(np.argmin(env[i0:i1]))
        db = 20 * np.log10(env[i] / 32768 + 1e-9)
        print(f'{jan:>14}  corte em {i / 100:.2f}s  ({db:.1f} dB)')


if __name__ == '__main__':
    main()
