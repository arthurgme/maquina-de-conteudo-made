#!/usr/bin/env python3
"""Gera os efeitos sonoros do motor (sintetizados, sem direitos de terceiros).

Uso: python3 motor/sfx/gerar_sfx.py   -> motor/sfx/click.wav
click: clique curto de interface (~80 ms): transiente de ruido agudo + corpo tonal + segundo clique mais fraco.
"""
import os, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def env(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))


def clique(amp=1.0):
    n = int(0.05 * SR)
    ruido = rng.standard_normal(n)
    ruido = np.diff(ruido, prepend=0)          # puxa para o agudo
    ruido = ruido * env(n, 0.0015)
    t = np.arange(n) / SR
    corpo = 0.6 * np.sin(2 * np.pi * 1850 * t) * env(n, 0.006) + 0.35 * np.sin(2 * np.pi * 950 * t) * env(n, 0.012)
    return amp * (0.5 * ruido / np.abs(ruido).max() + corpo)


def click():
    out = np.zeros(int(0.09 * SR))
    a = clique(1.0); out[:len(a)] += a
    d = int(0.028 * SR); b = clique(0.45); out[d:d + len(b)] += b[:len(out) - d]
    out[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
    return out / np.abs(out).max() * 10 ** (-3 / 20)


def salvar(nome, x):
    st = np.repeat((x * 32767).astype(np.int16)[:, None], 2, axis=1)
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), nome)
    with wave.open(p, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
    print('->', p)


if __name__ == '__main__':
    salvar('click.wav', click())
