import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
from data import produtos, vendas, caixa, clientes
from charts import grafico_vela, grafico_coluna, grafico_pizza, grafico_wordcloud

app = dash.Dash(__name__)
app.title = "Dashboard Mercadinho"

# Gráficos
fig_fluxo = grafico_vela(caixa)
fig_coluna = grafico_coluna(vendas, produtos, top_n=10)
fig_pizza = grafico_pizza(vendas, produtos, top_n=10)

# Top 10 clientes fiado
top_clientes = clientes.sort_values('fiado', ascending=False).head(10)

# Layout do dashboard
app.layout = html.Div(children=[
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
    
    html.H2("Top 10 Clientes Fiado"),
    html.Table([
        html.Tr([html.Th("Cliente"), html.Th("Fiado")])] +
        [html.Tr([html.Td(row['nome']), html.Td(row['fiado'])]) for idx,row in top_clientes.iterrows()]
    )
])

if __name__ == '__main__':
    app.run(debug=True)
