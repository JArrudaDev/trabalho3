import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)

# ---------------------------
# Produtos (1000 produtos)
# ---------------------------
produtos = pd.DataFrame({
    'id': range(1, 1001),
    'nome': [f"{fake.word().capitalize()}_{i}" for i in range(1, 1001)],  # garante nomes únicos
    'preco': np.random.randint(5, 100, 1000),
    'estoque': np.random.randint(0, 50, 1000),
    'validade': pd.date_range('2025-11-01', periods=1000, freq='D')
})

# ---------------------------
# Clientes (1000 clientes, limitaremos Top 10 para gráficos)
# ---------------------------
clientes = pd.DataFrame({
    'id': range(1, 1001),
    'nome': [f"{fake.first_name()}_{i}" for i in range(1, 1001)],
    'fiado': np.random.randint(0, 500, 1000)
})

# ---------------------------
# Vendas (1000 vendas)
# ---------------------------
vendas = pd.DataFrame({
    'id_venda': range(1, 1001),
    'produto_id': np.random.randint(1, 1001, 1000),
    'cliente_id': np.random.randint(1, 1001, 1000),
    'quantidade': np.random.randint(1, 10, 1000),
    'data': pd.date_range('2025-11-01', periods=1000, freq='H')
})

# Valor total calculado
vendas['valor_total'] = vendas.apply(
    lambda x: x['quantidade'] * produtos.loc[x['produto_id']-1, 'preco'], axis=1
)

# ---------------------------
# Caixa (entrada/saída)
# ---------------------------
caixa = pd.DataFrame({
    'data': pd.date_range('2025-11-01', periods=30),
    'entrada': np.random.randint(500, 2000, 30),
    'saida': np.random.randint(200, 1000, 30)
})
