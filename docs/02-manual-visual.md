# Manual visual

Versão 1, extraída do corte 1 da Casa 11 Malibu (aprovado como base). Tudo isto já está implementado no motor.

## Formato

- Vertical 1080x1920, 30 fps, H.264, áudio AAC 192 kbps, voz em -14 LUFS
- Duração alvo: cerca de 50 s

## Estrutura padrão: tour narrado (~50 s)

| Tempo | Bloco | Como |
|---|---|---|
| 0–6 s | Gancho | Corretor(a) já em movimento na direção da câmera, sem "oi". Selo com o nome do condomínio |
| 6–11 s | Contexto | Atributos do condomínio ou bairro em selos |
| 11–16 s | Lista com flashes | Cada ambiente dito vira um corte de ~1 s para o take do ambiente, com selo. Se precisar, 0,4 s de pausa para o flash respirar |
| 16–29 s | Diferencial | Números (terreno, área, suítes) em contador animado |
| 29–35 s | Convite | "Vem comigo" + gesto (abrir porta, apontar) que leva à vitrine |
| 35–43 s | Vitrine | 4 ambientes, 2 s cada, câmera lenta 50%, sem fala (só trilha) |
| 43–50 s | CTA | Corretor(a) de frente, zoom progressivo até plano médio. Selo "AGENDE SUA VISITA" |

## Cortes

- Cortar repetições e frases genéricas. Fala total de ~33 s.
- Corte sempre no silêncio mais próximo (`motor/cortes.py`), com fade de 40 ms.
- Corte dentro do mesmo take (jump cut): esconder com zoom (1,0 ↔ 1,45) ou cobrir com take de ambiente.
- Corretor(a) falando de costas por mais de 3 s: cobrir com ambiente.

## Câmera e cor

- Zoom lento de 1,0 a 1,12 nos planos falados longos (dá movimento).
- Takes horizontais: recorte vertical 9:16; usar panorâmica digital (`fx` de 0 a 0,35) quando o ambiente for largo.
- Cor base: `colortemperature=5200 (mix 0,6)`, contraste 1,05, saturação 1,12. Aquecimento leve: a casa clássica com mármore branco fica "suja" com dourado forte.
- Ambiente escuro (adega): `eq=brightness=0.05:gamma=1.35`.

## Legenda

- Palavra a palavra, frases de 2 a 4 palavras escritas à mão (não terminar em preposição).
- Inter SemiBold 66, branca, contorno preto 70% com desfoque leve, centro, y = 1290.
- Palavras-chave em Playfair Display Italic 74 (ex.: mansão, Malibu, família, festa, visita).
- Pequeno "pop" na primeira palavra de cada frase.
- Não legendar trechos em que o selo já diz a mesma coisa.

## Selos

- Inter Display Black, caixa alta, 92 a 150.
- Três camadas: sombra preta desfocada (leitura em fundo claro), brilho dourado (`&H8FD3FF&`), texto nítido.
- Entrada com escala 118% → 100% em 220 ms, fade 120/200 ms.
- Posição: alto (y 330 a 500) nos planos falados; centro (y 900) nos flashes.
- Contador: número sobe em 0,55 s, sufixo " m²", linha de apoio em Playfair itálico ("de terreno", "construídos").

## Áudio

- Clique real de mouse (`som: mouse-click`, -7 dB) em cada item da lista com flash, no início da palavra. Sons sintetizados soaram artificiais: usar gravações reais (CC0). Não usar em todo selo: só onde há corte rápido para um ambiente.

- Voz: passa-alta 80 Hz, redução de ruído leve, compressor suave, loudnorm -14 LUFS.
- Entregar sem trilha, salvo pedido. Vitrine fica em silêncio para receber o áudio escolhido no Instagram.
- Fade de saída de 0,55 s em vídeo e áudio.

## Pendências do manual

- Logo e assinatura final (sem arquivo ainda)
- Texto que acompanha o movimento da câmera (não implementado)
- Variações: só imagens com texto, story 15 s
