import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
from data import produtos, vendas, caixa, clientes
from charts import grafico_vela, grafico_coluna, grafico_pizza, grafico_wordcloud_base64

app = dash.Dash(__name__)
app.title = "Dashboard Mercadinho"

# Gráficos
fig_fluxo = grafico_vela(caixa)
fig_coluna = grafico_coluna(vendas, produtos, top_n=10)
fig_pizza = grafico_pizza(vendas, produtos, top_n=10)
wc_base64 = grafico_wordcloud_base64(vendas, produtos, top_n=10)

# Top clientes fiado (ordenado, controle via botão)
top_clientes_sorted = clientes.sort_values('fiado', ascending=False)
TOTAL_CLIENTES = len(top_clientes_sorted)

def format_currency(valor):
    try:
        s = f"R$ {valor:,.2f}"
        return s.replace(",", "_").replace(".", ",").replace("_", ".")
    except Exception:
        return str(valor)

# Layout do dashboard
app.layout = html.Div(className="container", children=[
    dcc.Store(id='clientes-limit', data=10),
    html.H1("Dashboard Mercadinho"),
    
    html.H2("Estoque de Produtos"),
    dcc.Graph(
        figure=px.bar(produtos.head(10), x='nome', y='estoque', title='Estoque Atual Top 10')
    ),
    
    html.H2("Fluxo de Caixa"),
    dcc.Graph(figure=fig_fluxo),
    
    html.H2("Produtos Mais Vendidos"),
    dcc.Graph(figure=fig_coluna),
    
    html.H2("Distribuição de Vendas"),
    dcc.Graph(figure=fig_pizza),
    
    html.H2("WordCloud - Top 10 Produtos"),
    html.Img(src=f'data:image/png;base64,{wc_base64}', style={'width':'80%'}),
    
    html.H2("Top Clientes (Fiado)"),
    html.Div(id='clientes-info', className='muted', children="Mostrando 10"),
    html.Div(className='table-wrap', children=[
        html.Table(id='top-clientes-table', className='table', children=[
            html.Thead(html.Tr([html.Th("Cliente"), html.Th("Fiado", className='num')]))
        ] + [
            html.Tr([html.Td(row['nome']), html.Td(format_currency(row['fiado']), className='num')])
            for _, row in top_clientes_sorted.head(10).iterrows()
        ])
    ]),
    html.Div(className='actions', children=[
        html.Button("Mostrar mais", id='btn-more', className='btn'),
        html.Button("Mostrar menos", id='btn-less', className='btn btn-secondary'),
    ])
])

@app.callback(
    [Output('top-clientes-table', 'children'), Output('clientes-info', 'children'), Output('clientes-limit', 'data')],
    [Input('btn-more', 'n_clicks'), Input('btn-less', 'n_clicks')],
    [State('clientes-limit', 'data')]
)
def atualizar_top_clientes(n_more, n_less, limit):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    limit = limit or 10
    if trigger == 'btn-more':
        limit = min(limit + 10, TOTAL_CLIENTES)
    elif trigger == 'btn-less':
        limit = max(10, limit - 10)

    header = html.Thead(html.Tr([html.Th("Cliente"), html.Th("Fiado", className='num')]))
    rows = [
        html.Tr([html.Td(row['nome']), html.Td(format_currency(row['fiado']), className='num')])
        for _, row in top_clientes_sorted.head(limit).iterrows()
    ]
    info = f"Mostrando {limit} de {TOTAL_CLIENTES}"
    return [header] + rows, info, limit

if __name__ == '__main__':
    app.run(debug=True)
