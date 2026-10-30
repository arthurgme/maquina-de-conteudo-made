# Plano do processo

Versão 1, 30/10/2026, depois do teste com a Casa 11 Malibu.

## O que travou no teste

Do briefing ao corte 1: cerca de 50 min, mais várias rodadas de perguntas. A maior parte do tempo foi **receber material e tomar decisões**, não editar.

| Gargalo | O que aconteceu | Recorrente? | Resolve com |
|---|---|---|---|
| Referência | Link do Instagram não abre pelo Claude, foi preciso baixar | Sempre | Referência baixada em `referencia/` |
| Takes espalhados | Take em Downloads no meio de ~2 mil arquivos, outros pelo chat em duas levas, CTA chegou no meio | Sim | Pasta padrão do projeto |
| Briefing aos pedaços | Duração, logo, CTA, orgânico/anúncio, música: cada ponto virou pergunta | Sim | Modelo de briefing |
| Limite técnico | Take de 510 MB (limite de transferência 400 MB), Mac não renderiza pelo Claude | Com 4K longo | Recorte sem recompressão (regra no CLAUDE.md) |
| Tudo do zero | Scripts, fontes, estilo criados na hora | Só na 1ª vez | Motor + manual visual neste repositório |
| Captação | Fala de 85 s seguidos, muito de costas, lente 1x; ambientes curtos e metade horizontal | Sim, maior impacto | Checklist de captação + roteiro da fala |
| Revisão | MP4 fechado, ajuste exige render | Sim | Plano.json + render só das peças alteradas |

## Fluxo alvo

1. **Antes de gravar**: com a referência e o imóvel, o Claude gera o roteiro curto da fala e a lista de takes (`04-checklist-captacao.md`).
2. **Material**: tudo na pasta do projeto (referência, takes nomeados, briefing).
3. **Análise**: estrutura da referência (ou modelo da biblioteca) + catálogo dos takes + transcrição.
4. **Mapa de edição**: tabela com tempo final, trecho, fala e tratamento. Único ponto de aprovação.
5. **Corte 1**: `plano.json` + motor, com o manual visual.
6. **Ajustes e entrega**: MP4 em `saida/`; versões extras se pedidas (story, anúncio).

## Peças do sistema

| Peça | Onde | Status |
|---|---|---|
| Pasta padrão por imóvel | Mac: `MÁQUINA DE CONTEÚDO - MADE/projetos/` | A criar |
| Modelo de briefing | `docs/03-modelo-briefing.md` | v1 |
| Biblioteca de referências | `docs/referencias/` + vídeos em `_referencias/` no Mac | 1 modelo |
| Manual visual | `docs/02-manual-visual.md` | v1 (do corte 1) |
| Checklist de captação | `docs/04-checklist-captacao.md` | v1 |
| Motor de edição | `motor/` | v1, validado |
| Método salvo (skill) | depois de 2 ou 3 vídeos | Fase 3 |

## Fases

- **Fase 1 (agora)**: pasta padrão, briefing, manual visual, referência como primeiro modelo, motor no repositório.
- **Fase 2 (próximos 2 a 3 vídeos)**: rodar o fluxo com roteiro e checklist antes de gravar. Medir tempo do material ao corte 1 e número de rodadas de ajuste.
- **Fase 3**: congelar como skill, com variações (tour narrado, só imagens com texto, story).
- **Fase 4 (escala)**: versões automáticas a partir do mesmo material (story 15 s, anúncio com outra CTA), lote semanal.

## Métricas

- Tempo do material completo até o corte 1 (teste: ~50 min + idas e vindas)
- Rodadas de ajuste até aprovar
- Perguntas feitas fora do briefing (meta: zero)
- Takes aproveitados / takes enviados

## Decisões pendentes

1. Volume esperado de vídeos por semana
2. Quem grava e como o material chega (AirDrop para o Mac ou pasta compartilhada no Google Drive)
3. Claude finaliza 100% ou faz corte + legendas e alguém finaliza num editor
4. Formatos além do reel (story, anúncio)
