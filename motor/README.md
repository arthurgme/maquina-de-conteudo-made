# Motor de edição

Edição por código: cada vídeo é descrito num `plano.json` e o motor renderiza. Assim o corte é reproduzível, e um ajuste é só editar o plano e renderizar de novo.

## Requisitos

- ffmpeg 6+ com libass e libx264
- Python 3.10+, `pip install -r motor/requirements.txt` (no ambiente do Claude: `--break-system-packages`)
- Fontes já incluídas em `motor/fontes/`

## Passo a passo de um vídeo

```bash
P=projetos/2026-10-30-casa-11-malibu
MIDIA=<pasta do projeto na mídia>            # contém takes/ e _trabalho/

# 1. folhas de contato (referência e takes)
python3 motor/folha_contato.py $MIDIA/referencia/ref.mp4 /tmp/ref.jpg --cortes
python3 motor/folha_contato.py --takes $MIDIA/takes /tmp/takes.jpg

# 2. transcrição com tempo por palavra
python3 motor/transcrever.py $P/words.json M=$MIDIA/takes/fala-principal.MOV C=$MIDIA/takes/cta.MOV \
  --contexto "nomes do condomínio, números do imóvel"

# 3. pontos de corte no silêncio
python3 motor/cortes.py $MIDIA/takes/fala-principal.MOV 3.78-3.98 12.2-12.6

# 4. escrever $P/plano.json e renderizar
python3 motor/render.py $P/plano.json --midia $MIDIA --trabalho /tmp/trab --saida "/tmp/Imovel - reel corte 1.mp4"

# re-renderizar só algumas peças depois de ajustar o plano
python3 motor/render.py $P/plano.json --midia $MIDIA --trabalho /tmp/trab --so-pecas v06,v14
```

Peças já renderizadas são reaproveitadas. Use `--forcar` para refazer todas.

## plano.json

Use `projetos/2026-10-30-casa-11-malibu/plano.json` como modelo. Todos os tempos `ini` são do **take original**.

| Campo | O que é |
|---|---|
| `fontes` | nome curto → arquivo. Take grande pode ter `trechos` (arquivo + `offset` no take original) |
| `video` | peças na ordem: `fonte`, `ini`, `dur` (duração na saída), `vel` (0.5 = câmera lenta), `zoom` [início, fim], `fx` [início, fim] (posição horizontal do recorte; em take horizontal vira panorâmica), `fy`, `cor_extra` |
| `audio` | peças na ordem: `fonte`, `ini`, `dur` ou `silencio` (segundos). A soma deve bater com o vídeo |
| `legendas` | `blocos` (um por peça de áudio legendada, com as frases escritas à mão), `enfase` (palavras em itálico serifado), `corrigir` |
| `selos` | `texto` (linhas: texto, y, tamanho) ou `contador` (número animado + linha de apoio). Tempos: número (segundos do vídeo) ou `{"fonte": "M", "t": 6.64}` (tempo do take, convertido) |
| `efeitos` | sons pontuais: `som` (arquivo em `motor/sfx/`, ex. `click`), `t` (número ou `{"fonte", "t"}`), `ganho_db` (padrão -8). Mixados depois do tratamento de voz |
| `cor` | filtro de cor base (padrão: aquecimento leve) |

## Desempenho

No ambiente do Claude (2 CPUs), decodificar 4K HEVC é o gargalo: cerca de 3,5 min para as peças de um reel de 50 s, mais 2 min para o final.

## Validação

Mudou o motor? Rode `projetos/2026-10-30-casa-11-malibu/plano-corte1.json` e compare: as legendas devem sair idênticas e as peças com o mesmo MD5 (`ffmpeg -i peca.mp4 -map 0:v -f md5 -`), ou registre a mudança em `docs/05-registro-de-decisoes.md`.
