# Registro de decisões

Mais recente no topo. Uma linha por decisão ou aprendizado; detalhes no `notas.md` do projeto.

## 30/10/2026: Casa 11 Malibu (corte 4)

- Duração deixa de ser fixa em 50 s: o vídeo tem o tamanho que o conteúdo pede (corte 4: 48,8 s).
- CTA encurtada de 7,15 s para 5,9 s: começa 0,4 s antes da fala (em vez de ~1,5 s de caminhada) e termina 0,3 s depois do "aguardando". Fade final de 0,35 s.
- Motor: corrigido o zoom animado. O recorte era calculado pelo tamanho do primeiro quadro, então o zoom crescia para a direita e para baixo (na CTA a corretora ia para a borda). Agora usa zoompan, centrado em fx/fy quadro a quadro. Zoom fixo continua pelo caminho antigo (peças v02, v03 e v06 do corte 1 seguem idênticas); peças com zoom animado do corte 1 mudaram de propósito (enquadramento corrigido).
- Motor: `fx` [início, fim] agora também anima em takes verticais (acompanhar a pessoa).

## 30/10/2026: Casa 11 Malibu (corte 3)

- Click sintetizado reprovado (soou inventado). Trocado por gravação real de clique de mouse, CC0 (`motor/sfx/mouse-click.wav`, origem em `motor/sfx/LEIAME.md`), -7 dB.
- Regra: efeitos sonoros sempre de gravação real com licença livre, nunca sintetizados.

## 30/10/2026: Casa 11 Malibu (corte 2)

- Click sonoro em cada ambiente da lista com flash (sala de jantar, salão de jogos, piscina, academia), na palavra dita, -9 dB. Som sintetizado (`motor/sfx/click.wav`), sem direitos de terceiros.
- Removida a contagem "2, 1" de quem gravava, que vazava antes da fala da CTA: áudio da CTA começa no silêncio de 2,13 s do take (vídeo inalterado).
- Lição de captação: quem grava não deve contar em voz alta; usar gesto.
- Motor: efeitos sonoros (`efeitos` no plano.json), mixados depois do tratamento de voz para o compressor não achatar o click.
- Motor: corrigida a conversão de tempo quando duas peças de áudio do mesmo take se encostam (o tempo caía na peça anterior pela folga de 0,05 s). Corte 1 continua idêntico (`plano-corte1.json`).

## 30/10/2026: teste Casa 11 Malibu (corte 1)

- Edição por código (ffmpeg + plano.json) escolhida em vez de CapCut: precisão de corte pela transcrição e reprodutibilidade. CapCut não tem projeto que o Claude consiga gerar.
- Duração alvo ~50 s, igual à referência. Bloco "salas integradas" cortado para caber.
- Sem logo por enquanto.
- Todos os takes enviados são da casa (inclusive as duas academias).
- Entrega sem trilha; música escolhida no Instagram.
- Aquecimento de cor leve (não o dourado forte da referência) por causa do mármore branco.
- Lista de ambientes com flashes de ~1 s e pausa de 0,4 s antes de "academia".
- Pendente: "clique aqui embaixo" na CTA só funciona como anúncio; definir orgânico vs anúncio no briefing.
- Estrutura de trabalho: repositório (cérebro e motor) + pasta de mídia no Mac + Projeto no Claude com chats separados (Produção por imóvel, Laboratório, Processo).
- Motor v1 validado: reproduz o corte 1 com legendas idênticas e peças com o mesmo MD5.
