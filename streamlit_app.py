# Importando as bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px

# Carregando os dados
dados = pd.read_excel('Vendas_Base_de_Dados.xlsx')

# Calcula o faturamento em cada linha
dados['Faturamento'] = dados['Quantidade'] * dados['Valor Unitário']

# Gera dataframe de faturamento por loja
df_lojas_full = (
    dados.groupby('Loja')['Faturamento']
    .sum()
    .reset_index()
    .sort_values(by='Faturamento', ascending=False)
)

# Lista de lojas (agora pode fazer sem erro)
lojas = df_lojas_full['Loja'].tolist()



# ========================
# 0) FATURAMENTO TOTAL
# ========================
# Faturamento total de todas as lojas
faturamento_total_geral = dados['Faturamento'].sum()
st.markdown(f"""
<div style="text-align: center;">
    <h2>Faturamento Total:</h2>
    <h1 style="font-size: 50px; margin-bottom:50px;">R$ {faturamento_total_geral:,.2f}</h1>
</div>
""", unsafe_allow_html=True)


# ========================
# 1) Detalhamento por Loja e Produto
# ========================
st.subheader("Detalhamento de Vendas por Loja e Produto")

# Seleção da loja
loja_escolhida = st.selectbox(
    'Escolha uma loja para ver detalhes:',
    lojas
)

# Lista de produtos disponíveis na loja selecionada
produtos_na_loja = sorted(dados[dados['Loja'] == loja_escolhida]['Produto'].unique())

produto_escolhido = st.selectbox(
    'Escolha um produto:',
    produtos_na_loja
)

# Filtra os dados com base na seleção
dados_filtrados = dados[
    (dados['Loja'] == loja_escolhida) &
    (dados['Produto'] == produto_escolhido)
]

# Faturamento total da loja + produto selecionado
faturamento_total = dados_filtrados['Faturamento'].sum()

# Resumo textual
st.subheader(
    f"**Na loja `{loja_escolhida}`, o produto `{produto_escolhido}` teve um faturamento total de: `R$ {faturamento_total:,.2f}`.**"
)

# Exibir tabela de dados detalhados
st.dataframe(dados_filtrados.reset_index(drop=True))


# ========================
# 2) Gráfico de Pizza dos Produtos na Loja
# ========================

# Agrupa faturamento por produto na loja escolhida
df_produtos_loja = (
    dados[dados['Loja'] == loja_escolhida]
    .groupby('Produto')['Faturamento']
    .sum()
    .reset_index()
    .sort_values(by='Faturamento', ascending=False)
)

# Cria gráfico de pizza dos produtos na loja
grafico_pizza_produtos = px.pie(
    df_produtos_loja,
    names='Produto',
    values='Faturamento',
    title=f'Participação dos Produtos no Faturamento da Loja {loja_escolhida}'
)
st.plotly_chart(grafico_pizza_produtos)


# ========================
# 3) Gráfico de Barras por Loja
# ========================
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
# 4) Gráfico de Pizza por Loja
# ========================
st.subheader("Distribuição de Faturamento por Loja")

lojas_selecionadas = st.multiselect(
    'Escolha as lojas para o gráfico:',
    lojas,
    default=lojas
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


