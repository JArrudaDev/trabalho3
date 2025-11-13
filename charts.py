import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import pandas as pd

def grafico_vela(caixa):
    fig = px.line(caixa, x='data', y=['entrada', 'saida'], title='Fluxo de Caixa')
    return fig

def grafico_coluna(vendas, produtos, top_n=10):
    df = vendas.groupby('produto_id')['quantidade'].sum().reset_index()
    df = df.merge(produtos[['id', 'nome']], left_on='produto_id', right_on='id')
    df_top = df.sort_values('quantidade', ascending=False).head(top_n)
    fig = px.bar(df_top, x='nome', y='quantidade', title=f'Top {top_n} Produtos Mais Vendidos')
    return fig

def grafico_pizza(vendas, produtos, top_n=10):
    df = vendas.groupby('produto_id')['quantidade'].sum().reset_index()
    df = df.merge(produtos[['id', 'nome']], left_on='produto_id', right_on='id')
    df_top = df.sort_values('quantidade', ascending=False).head(top_n)
    fig = px.pie(df_top, names='nome', values='quantidade', title=f'Distribuição Top {top_n} Produtos')
    return fig

def grafico_wordcloud(vendas, produtos, top_n=10):
    df = vendas.groupby('produto_id')['quantidade'].sum().reset_index()
    df = df.merge(produtos[['id', 'nome']], left_on='produto_id', right_on='id')
    df_top = df.sort_values('quantidade', ascending=False).head(top_n)
    texto = ' '.join(df_top['nome'].tolist())
    wc = WordCloud(width=800, height=400, background_color='white').generate(texto)
    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
