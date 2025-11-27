# Dashboard Mercadinho

Projeto de dashboard para um mercadinho usando Python, Dash e Plotly.

## Principais Funcionalidades

- Gráfico candlestick do fluxo de caixa (entrada/saída → saldo OHLC)
- Gráfico de coluna (Produtos mais vendidos)
- Gráfico de pizza (Distribuição de vendas por produto)
- WordCloud (Top produtos)
- Estoque de produtos (Top 10)
- Tabela de clientes fiadistas com “Mostrar mais/menos”
- Resumos (contagem de produtos, clientes e vendas)

- Candlestick real: o gráfico de fluxo de caixa agora usa OHLC sintetizado a partir de entrada/saída (saldo cumulativo), facilitando leitura de variações diárias.
- UI/UX: adicionado `assets/styles.css` com layout simples (cards, tabelas legíveis, grid), aparência limpa para mercadinho.
- Tabela Top Clientes: cabeçalho fixo, números alinhados, botões “Mostrar mais/menos”.
- Cálculo robusto do valor total: agora por `map` usando `produto_id`, sem depender da posição do índice.

## Estrutura do Código

- `app.py`: define o aplicativo Dash, layout das seções, gráficos no dashboard e callback para a tabela de Top Clientes (paginação por botões). Também injeta classes CSS para o estilo.
- `charts.py`: funções de geração de gráficos.
  - `grafico_vela`: cria candlestick (OHLC) do caixa a partir de entrada/saída (saldo cumulativo → open/high/low/close).
  - `grafico_coluna`: barra com Top N produtos por quantidade vendida.
  - `grafico_pizza`: pizza da distribuição de vendas por produto (Top N).
  - `grafico_wordcloud_base64`: gera imagem WordCloud em base64 dos nomes dos produtos mais vendidos.
- `data.py`: gera dados sintéticos.
  - `produtos`: 1000 itens com nomes realistas (produto base + variante opcional + marca + tamanho + SKU), preço, estoque e validade.
  - `clientes`: 1000 clientes com nomes brasileiros (Faker `pt_BR`) e valor de fiado.
  - `vendas`: 1000 vendas com `produto_id`, `cliente_id`, `quantidade` e `data`. `valor_total` calculado por `map` via id do produto.

## Como Executar

Pré-requisitos: Python 3.11

```bash
pip install -r requirements.txt
python app.py
```

Abra o endereço mostrado no terminal (geralmente `http://127.0.0.1:8050`).

## Dicas de Uso

- Se os nomes nos eixos ficarem longos, considere barras horizontais para “Produtos mais vendidos” e “Estoque”, ou reduza o Top N.
- A lista de clientes fiadistas inicia com 10 linhas; use os botões para expandir/recolher.