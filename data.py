import pandas as pd
import numpy as np
from faker import Faker

fake = Faker('pt_BR')
Faker.seed(42)
np.random.seed(42)

# ---------------------------------
# Gerador de nomes de produtos
# ---------------------------------
MARCAS = [
    "Bom Preço", "Saboroso", "Doce Vida", "Casa & Campo", "Naturalle",
    "Pratiko", "Master", "Top", "Delícia", "Boa Mesa", "Alfa", "Premium"
]
PRODUTOS_BASE = [
    "Arroz", "Feijão", "Açúcar", "Sal", "Macarrão", "Café", "Leite", "Óleo de Soja",
    "Farinha de Trigo", "Farinha de Milho", "Molho de Tomate", "Biscoito", "Achocolatado",
    "Manteiga", "Margarina", "Queijo", "Presunto", "Iogurte", "Refrigerante", "Suco",
    "Água Mineral", "Cerveja", "Detergente", "Sabão em Pó", "Amaciante", "Desinfetante",
    "Água Sanitária", "Shampoo", "Sabonete", "Papel Higiênico", "Guardanapo", "Papel Toalha",
    "Esponja", "Saco de Lixo", "Alho", "Cebola", "Tomate", "Batata", "Banana", "Maçã",
    "Pão de Forma", "Linguiça", "Carne Bovina", "Frango", "Peixe", "Ovos", "Atum",
    "Sardinha", "Milho em Conserva", "Ervilha em Conserva"
]
VARIANTES = [
    "Integral", "Parboilizado", "Carioca", "Preto", "Refinado", "Cristal", "Sem Sal",
    "Tradicional", "Extra Forte", "Skim", "UHT", "Zero", "Light", "Clássico", "Sabor Chocolate",
    "Defumada", "Temperado", "Congelado", "Fresquinho", "De Corte"
]
TAMANHOS = [
    "1kg", "2kg", "5kg", "500g", "250g", "200g", "400g", "1L", "2L", "500ml", "200ml",
    "6un", "12un", "30un"
]

def gerar_nome_produto(idx: int) -> str:
    rng = np.random.default_rng(42 + idx)
    base = rng.choice(PRODUTOS_BASE)
    marca = rng.choice(MARCAS)
    tamanho = rng.choice(TAMANHOS)
    if rng.random() < 0.5:
        variante = rng.choice(VARIANTES)
        nome = f"{base} {variante} {marca} {tamanho}"
    else:
        nome = f"{base} {marca} {tamanho}"
    return f"{nome} • SKU{idx:04d}"

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

# Substitui nomes por itens de mercado realistas
produtos['nome'] = [gerar_nome_produto(i) for i in range(1, 1001)]

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

# Valor total calculado (robusto por id)
precos_por_id = produtos.set_index('id')['preco']
vendas['valor_total'] = vendas['quantidade'] * vendas['produto_id'].map(precos_por_id)

# ---------------------------
# Caixa (entrada/saída)
# ---------------------------
caixa = pd.DataFrame({
    'data': pd.date_range('2025-11-01', periods=30),
    'entrada': np.random.randint(500, 2000, 30),
    'saida': np.random.randint(200, 1000, 30)
})
