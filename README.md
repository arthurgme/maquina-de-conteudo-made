# MÁQUINA DE CONTEÚDO - MADE

Sistema de produção de reels de imóveis da **@madeimoveis**: referência + takes + briefing entram, reel vertical pronto sai.

Este repositório guarda o **cérebro** (processo, padrão visual, modelos e o motor de edição). Os **vídeos** (takes, referências em vídeo, cortes) ficam na pasta de mídia no Mac, com a mesma estrutura de projetos.

## Estrutura

```
docs/
  01-plano-do-processo.md      gargalos, fluxo ideal, fases, decisões pendentes
  02-manual-visual.md          legenda, selos, cor, ritmo, estrutura padrão (~50 s)
  03-modelo-briefing.md        o que preencher antes de cada vídeo
  04-checklist-captacao.md     como gravar para a edição render bem
  05-registro-de-decisoes.md   o que foi testado, aprovado ou descartado
  06-instrucoes-projeto-claude.md   texto para colar nas instruções do Projeto no Claude
  referencias/                 análises de reels de referência (modelos de estrutura)
motor/                         ferramenta de edição (ffmpeg + Python)
  render.py                    monta o reel a partir de um plano.json
  legendas.py                  legenda palavra a palavra + selos (ASS)
  transcrever.py               transcrição com tempo de cada palavra
  cortes.py                    acha o silêncio mais próximo para cortar
  folha_contato.py             folhas de contato de referências, takes e cortes
  fontes/                      Inter e Playfair Display (OFL)
projetos/<AAAA-MM-DD-imovel>/  briefing.md, plano.json, words.json, notas.md (sem vídeos)
```

## Pasta de mídia no Mac

```
MÁQUINA DE CONTEÚDO - MADE/
  _marca/                      logo, músicas aprovadas
  _referencias/                reels de referência baixados (ref-01-....mp4)
  projetos/<AAAA-MM-DD-imovel>/
    referencia/                o reel que vai guiar este vídeo
    takes/                     nomeados pelo conteúdo: fala-principal.MOV, cta.MOV, piscina.MOV...
    saida/                     cortes entregues
    _trabalho/                 temporários (trechos recortados, áudio extraído)
```

O nome da pasta do projeto é o mesmo aqui e no Mac.

## Fluxo em uma linha

Briefing + pasta do projeto → análise da referência → catálogo dos takes + transcrição → **mapa de edição (aprovação)** → corte 1 → ajustes → entrega.

Detalhes em `docs/01-plano-do-processo.md`. Como rodar o motor em `motor/README.md`.
