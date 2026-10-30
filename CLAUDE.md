# Instruções para o Claude neste repositório

Este repositório é a MÁQUINA DE CONTEÚDO - MADE: produção de reels de imóveis da @madeimoveis (imobiliária de alto padrão, RJ). Leia `README.md` para a estrutura.

## Modos de trabalho (cada um em um chat separado)

- **Produção** (um chat por imóvel): seguir o fluxo de `docs/01-plano-do-processo.md` usando o motor como está. Não alterar `motor/` num chat de produção; se algo do motor precisar mudar, anotar em `projetos/<slug>/notas.md` para o Laboratório.
- **Laboratório**: evoluir o motor e o manual visual. Toda mudança no motor precisa reproduzir o corte de referência (`projetos/2026-10-30-casa-11-malibu`) ou registrar em `docs/05-registro-de-decisoes.md` por que mudou.
- **Processo**: ajustar plano, modelos e checklist. Registrar decisões em `docs/05-registro-de-decisoes.md`.

## Regras de produção

1. Antes de editar, ter: briefing preenchido, referência em arquivo (Instagram não abre por fetch, pedir o vídeo baixado), takes na pasta `takes/` do projeto.
2. Pasta de mídia no Mac: pedir acesso uma vez à pasta `MÁQUINA DE CONTEÚDO - MADE`. Arquivos até 400 MB: trazer direto. Acima disso: recortar no Mac sem recompressão só os trechos úteis (`ffmpeg -ss X -i take.MOV -t D -map 0:v:0 -map 0:a:0 -c copy _trabalho/<nome>_a.mov`) e registrar os `trechos` com `offset` no plano.json. O áudio do trecho começa exatamente em X.
3. Nunca renderizar no Mac (o shell de lá tem limite de 180 s e processos em segundo plano morrem). Renderizar no ambiente de trabalho do Claude.
4. Transcrever com `motor/transcrever.py` (modelo medium) e conferir números e nomes próprios.
5. Montar o mapa de edição (tabela: tempo final, trecho do take, fala, tratamento) e **esperar aprovação**, salvo se o briefing disser "pode ir direto".
6. Escrever `projetos/<slug>/plano.json` e renderizar com `motor/render.py`. Revisar com `motor/folha_contato.py` (enquadramento de cada plano e leitura dos selos) e conferir nível de voz por bloco.
7. Entregar o MP4 e copiar para `saida/` no Mac. Commitar plano.json, words.json e notas.md (nunca vídeos).

## Padrão de marca

Curadoria, tom institucional, sem urgência forçada. Seguir `docs/02-manual-visual.md`. Não usar travessão em textos de tela ou relatórios. Sem logo enquanto não houver arquivo em `_marca/`.
