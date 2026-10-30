# Efeitos sonoros

| Arquivo | O que é | Origem e licença |
|---|---|---|
| `mouse-click.wav` | Clique real de mouse (apertar e soltar, 94 ms entre os dois), recortado no primeiro estalo, 48 kHz | "Mouse Click Sound" de Pixeliota, freesound.org/s/678248, **CC0** (obtido via remotion.media/mouse-click.wav) |
| `click-sintetico.wav` | Clique sintetizado (descartado no corte 3: soou artificial) | Gerado por `gerar_sfx.py`, sem direitos de terceiros |

Uso no plano.json: `{"som": "mouse-click", "t": ..., "ganho_db": -7}`. O som começa no instante `t` (o primeiro estalo está a 4 ms do início do arquivo).
Novos efeitos: preferir gravações reais com licença CC0 e registrar a origem aqui.
