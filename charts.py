from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64

def grafico_vela(caixa):
    # Converte entradas/saídas em saldo cumulativo e gera OHLC sintético
    df = caixa.copy().sort_values('data').reset_index(drop=True)
    df['net'] = df['entrada'] - df['saida']
    df['close'] = df['net'].cumsum()
    df['open'] = df['close'] - df['net']
    df['high'] = df[['open', 'close']].max(axis=1)
    df['low'] = df[['open', 'close']].min(axis=1)

    fig = go.Figure(data=[go.Candlestick(
        x=df['data'], open=df['open'], high=df['high'], low=df['low'], close=df['close']
    )])
    fig.update_layout(title='Fluxo de Caixa (Candlestick)', xaxis_title='Data', yaxis_title='Saldo')
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

def grafico_wordcloud_base64(vendas, produtos, top_n=10):
    # Agrupa vendas e pega top produtos
    df = vendas.groupby('produto_id')['quantidade'].sum().reset_index()
    df = df.merge(produtos[['id', 'nome']], left_on='produto_id', right_on='id')
    df_top = df.sort_values('quantidade', ascending=False).head(top_n)
    texto = ' '.join(df_top['nome'].tolist())

    # Gera WordCloud
    wc = WordCloud(width=800, height=400, background_color='white').generate(texto)
    
    # Converte para imagem base64
    img = BytesIO()
    wc.to_image().save(img, format='PNG')
    img.seek(0)
    wc_base64 = base64.b64encode(img.getvalue()).decode()
    
    return wc_base64
