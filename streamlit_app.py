# Importando as bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px

# Carregando os dados
dados = pd.read_excel('Vendas_Base_de_Dados.xlsx')

# Calcula o faturamento em cada linha
dados['Faturamento'] = dados['Quantidade'] * dados['Valor Unitário']

# ========================
# 1) Gráfico de Barras
# ========================
# Agrupa e ordena o faturamento por loja usando TODOS os dados
df_lojas_full = (
    dados.groupby('Loja')['Faturamento']
    .sum()
    .reset_index()
    .sort_values(by='Faturamento', ascending=False)
)

st.title("Dashboard de Vendas")
st.subheader("Faturamento por Loja")
grafico_barras = px.bar(
    df_lojas_full,
    x='Loja',
    y='Faturamento',
    title='Faturamento Total por Loja'
)
st.plotly_chart(grafico_barras)

# ========================
# 2) Gráfico de Pizza
# ========================
st.subheader("Distribuição de Faturamento por Loja")

# Lista de todas as lojas
lojas = df_lojas_full['Loja'].tolist()

# Permite ao usuário escolher quais lojas exibir no gráfico de pizza
lojas_selecionadas = st.multiselect(
    'Escolha as lojas para o gráfico:',
    lojas,
    default=lojas  # por padrão, exibe todas as lojas
)

df_pie = df_lojas_full[df_lojas_full['Loja'].isin(lojas_selecionadas)]
if not df_pie.empty:
    grafico_pizza = px.pie(
        df_pie,
        names='Loja',
        values='Faturamento',
        title='Participação de Faturamento por Loja'
    )
    st.plotly_chart(grafico_pizza)
else:
    st.write("Selecione ao menos uma loja para ver o gráfico.")

# ========================
# 3) Detalhamento por Loja e Produto
# ========================
st.subheader("Detalhamento de Vendas por Loja e Produto")

# Seleção de loja
loja_escolhida = st.selectbox(
    'Escolha uma loja para ver detalhes:',
    lojas
)

# Lista de produtos disponíveis dentro da loja selecionada
produtos_na_loja = sorted(dados[dados['Loja'] == loja_escolhida]['Produto'].unique())
produto_escolhido = st.selectbox(
    'Escolha um produto:',
    produtos_na_loja
)

# Filtra dados pelo produto e pela loja selecionados
dados_detalhe = dados[
    (dados['Loja'] == loja_escolhida) &
    (dados['Produto'] == produto_escolhido)
]

st.write(f"**Dados de Vendas** — Loja: {loja_escolhida} | Produto: {produto_escolhido}")
st.dataframe(dados_detalhe.reset_index(drop=True))
