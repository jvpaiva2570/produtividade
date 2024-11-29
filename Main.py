import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np



# Configuração dos valores fixos (em amarelo)
dias_programados = 365
horas_programadas_por_dia = 24
horas_programadas_ano = dias_programados * horas_programadas_por_dia
tempo_preventiva_250h = 8
tempo_preventiva_500h = 12
tempo_preventiva_1000h = 16
tempo_preventiva_16000h = 168

# Título e layout
st.set_page_config(page_title="Dimensionamento de uma mina")

st.title("Manutenção e Disponibilidade de Caminhões")

# Configuração da tabela de entrada
caminhoes = ["CM-001", "CM-002", "CM-003", "CM-004", "CM-005", "CM-006", "CM-007", "CM-008"]
disponibilidades = []

# Criação das colunas para exibir os dados de cada caminhão
for caminhao in caminhoes:
    with st.expander(f"Configurações para {caminhao}"):
        st.subheader(f"{caminhao}")

        # Campos de entrada para os valores editáveis (quantidades para manutenções preventivas)
        qtd_250h = st.number_input(f"Qtd Preventiva 250h ({caminhao})", min_value=0, value=35)
        qtd_500h = st.number_input(f"Qtd Preventiva 500h ({caminhao})", min_value=0, value=18)
        qtd_1000h = st.number_input(f"Qtd Preventiva 1000h ({caminhao})", min_value=0, value=9)
        qtd_16000h = st.number_input(f"Qtd Preventiva 16000h ({caminhao})", min_value=0, value=0)

        # Campo para taxa de manutenção corretiva
        taxa_corretiva = st.number_input(f"Taxa Corretiva (%) ({caminhao})", min_value=0, max_value=100, value=25) / 100

        # Cálculos do tempo total parado (baseado nas quantidades e tempos preventivos)
        tempo_parado_250h = qtd_250h * tempo_preventiva_250h
        tempo_parado_500h = qtd_500h * tempo_preventiva_500h
        tempo_parado_1000h = qtd_1000h * tempo_preventiva_1000h
        tempo_parado_16000h = qtd_16000h * tempo_preventiva_16000h

        # Tempo corretivo (usando a taxa de corretiva e horas programadas)
        

        # Tempo total parado
        tempo_total_parado = tempo_parado_250h + tempo_parado_500h + tempo_parado_1000h + tempo_parado_16000h 
        tempo_corretivo = taxa_corretiva * tempo_total_parado
        tempo_total_parado+=tempo_corretivo
        # Cálculo da disponibilidade física (DF)
        df = ((horas_programadas_ano - tempo_total_parado) / horas_programadas_ano) * 100
        disponibilidades.append(df)  

        # Exibição dos resultados calculados
        st.write(f"Tempo Total Parado ({caminhao}): {tempo_total_parado:.2f} horas")
        st.write(f"Disponibilidade Física (DF) ({caminhao}): {df:.2f}%")

# Calculo da DF total da frota
if disponibilidades:
    df_total = sum(disponibilidades) / len(disponibilidades)
    st.subheader("Totais da Frota")
    st.write(f"Disponibilidade Física Média da Frota (DF): {df_total:.2f}%")

# CRIAÇÃO DO GRÁFICO DE DISPONIBILIDADE

# Definição da média fixa
metaFixa = 90

# Criação do DataFrame com os nomes dos caminhões e suas disponibilidades
df_plot = pd.DataFrame({
    'Caminhão': caminhoes,
    'Disponibilidade Física (%)': disponibilidades
})

df_plot["Acima_da_Meta"] = df_plot["Disponibilidade Física (%)"] >= metaFixa

# Adiciona a coluna indicando se atingiu a meta
df_plot["Legenda"] = df_plot["Disponibilidade Física (%)"].apply(
    lambda x: "Atingiu a Meta" if x >= metaFixa else "Não Atingiu a Meta"
)

# Define as cores com base na linha da meta
cores = ["green" if acima else "red" for acima in df_plot["Acima_da_Meta"]]

fig = px.bar(
    df_plot,
    x="Caminhão",
    y="Disponibilidade Física (%)",
    title="Disponibilidade Física por Caminhão",
    color="Legenda", 
    color_discrete_map={
        "Atingiu a Meta": "green", 
        "Não Atingiu a Meta": "red"
    }  # Define as cores com base na legenda
)

# Adiciona uma linha de referência da meta
fig.add_hline(y=df_total, line_dash="dash", line_color="blue", 
              annotation_text="Meta 90%", annotation_position="top left")

# Exibição do gráfico no Streamlit
st.plotly_chart(fig)

#CRIAÇÃO DO GRÁFICO DE PRODUTIVIDADE
# Perfil da mina
# Título do Dashboard
st.title("Perfil da Mina - Configuração de Distâncias")

# Subtítulo
st.markdown("### Insira as distâncias (Km) para cada perfil:")

# Divisão em colunas para criar um layout mais visual
col1, col2, col3 = st.columns(3)

# Campo de entrada para "Horizontal" na primeira coluna
with col1:
    st.subheader("Horizontal")
    dist_horizontal = st.number_input("Distância (Km):", min_value=0.0, value=1.0, step=0.1, key="horizontal")

# Campo de entrada para "Subindo" na segunda coluna
with col2:
    st.subheader("Subindo")
    dist_subida = st.number_input("Distância (Km):", min_value=0.0, value=3.0, step=0.1, key="subida")

# Campo de entrada para "Descendo" na terceira coluna
with col3:
    st.subheader("Descendo")
    dist_descida = st.number_input("Distância (Km):", min_value=0.0, value=0.8, step=0.1, key="descendo")

#tabela de velocidades
# Velocidades estáticas para cada perfil
velocidades = {
    "Horizontal": {"Carregado": 25, "Vazio": 30},
    "Subindo": {"Carregado": 20, "Vazio": 25},
    "Descendo": {"Carregado": 15, "Vazio": 30},
}

# Velocidade recomendada para os caminhoes
# Exibição das informações em colunas
col1, col2, col3 = st.columns(3)

# Perfil Horizontal
with col1:
    st.write(f"**Carregado:** {velocidades['Horizontal']['Carregado']} km/h")
    st.write(f"**Vazio:** {velocidades['Horizontal']['Vazio']} km/h")

# Perfil Subindo
with col2:
    st.write(f"**Carregado:** {velocidades['Subindo']['Carregado']} km/h")
    st.write(f"**Vazio:** {velocidades['Subindo']['Vazio']} km/h")

# Perfil Descendo
with col3:
    st.write(f"**Carregado:** {velocidades['Descendo']['Carregado']} km/h")
    st.write(f"**Vazio:** {velocidades['Descendo']['Vazio']} km/h")

###
# Função para calcular o tempo de ciclo total
def calcular_tempo_ciclo(dist_horizontal, dist_subida, dist_descida):
    # Velocidades médias (km/h)
    velocidades = {
        "Horizontal": {"Carregado": 25, "Vazio": 30},
        "Subindo": {"Carregado": 20, "Vazio": 25},
        "Descendo": {"Carregado": 15, "Vazio": 30},
    }
    
    # Cálculo do tempo (minutos)
    tempo_horizontal = (dist_horizontal / velocidades["Horizontal"]["Carregado"]) * 60 + \
                       (dist_horizontal / velocidades["Horizontal"]["Vazio"]) * 60
    tempo_subindo = (dist_subida / velocidades["Subindo"]["Carregado"]) * 60 + \
                    (dist_subida / velocidades["Subindo"]["Vazio"]) * 60
    tempo_descendo = (dist_descida / velocidades["Descendo"]["Carregado"]) * 60 + \
                     (dist_descida / velocidades["Descendo"]["Vazio"]) * 60

    # Soma dos tempos
    tempo_total = tempo_horizontal + tempo_subindo + tempo_descendo
    return tempo_total

# Calcular o tempo de ciclo total
tempo_total = calcular_tempo_ciclo(dist_horizontal, dist_subida, dist_descida)

# Criar gráfico de barra única
fig, ax = plt.subplots(figsize=(6, 2))
ax.barh(["Tempo de Ciclo"], [tempo_total], color="skyblue", height=0.5)
ax.set_xlim(0, 60)
ax.set_xlabel("Tempo (minutos)")
ax.set_title("Tempo de Ciclo Total")
ax.grid(axis="x", linestyle="--", alpha=0.7)

# Adicionar o valor na barra
for i, v in enumerate([tempo_total]):
    ax.text(v + 1, i, f"{v:.1f} min", va="center", ha="left", fontsize=10)

# Exibir o gráfico no Streamlit
st.pyplot(fig)

##
# Título do Dashboard
st.title("Capacidade do Caminhão e Nível de Carga")

# Campo para o usuário inserir a capacidade do caminhão
capacidade_caminhao = st.number_input("Digite a capacidade do caminhão (em toneladas):", min_value=0.0, step=0.1)

# Campo para o usuário ajustar o nível de carga (de 0% a 100%)
nivel_carga = st.slider("Selecione o nível de carga do caminhão (%):", 0, 100, step=1)


# Criar o gráfico do "termômetro"
fig, ax = plt.subplots(figsize=(2, 6))  # Ajustar proporção para parecer um termômetro
ax.barh([0], [nivel_carga], color="skyblue", height=0.6)
ax.set_xlim(0, 100)  # Limitar a escala de 0% a 100%
ax.set_xticks([0, 20, 40, 60, 80, 100])  # Marcar os principais níveis
ax.set_xticklabels(["0%", "20%", "40%", "60%", "80%", "100%"], rotation=0)
ax.set_yticks([])
ax.set_title("Nível de Carga (%)", fontsize=5)
ax.grid(axis="x", linestyle="--", alpha=0.5)

#######
import streamlit as st
import matplotlib.pyplot as plt

# Configurações iniciais
st.title("Gráfico: Nível de Carga vs Produtividade Horária")
st.write("Selecione o nível de carga do caminhão para visualizar a produtividade horária.")

# Dados fixos
capacidade_caminhao = 240  # Capacidade do caminhão (toneladas)
tempo_ciclo_total = 25.4  # Tempo de ciclo total (minutos)

# Entrada do operador: Nível de carga (%) do caminhão
nivel_carga_percentual = st.slider("Selecione o nível de carga do caminhão (%)", min_value=10, max_value=100, step=10)

# Converter o nível de carga (%) para fator de enchimento (entre 0.1 e 1.0)
nivel_carga_fator = nivel_carga_percentual / 100

# Gerar níveis de carga até o valor selecionado
niveis_de_carga = [round(x * 0.1, 1) for x in range(1, int(nivel_carga_fator * 10) + 1)]
produtividades_horarias = [
    (capacidade_caminhao * nivel) / (tempo_ciclo_total / 60)  # Convertendo tempo de ciclo para horas
    for nivel in niveis_de_carga
]

# Gerar gráfico
fig, ax = plt.subplots()
ax.plot(niveis_de_carga, produtividades_horarias, marker='o', color='red', label="Produtividade Horária")

# Adicionar o texto no ponto máximo (último ponto no gráfico)
ponto_max_x = niveis_de_carga[-1]
ponto_max_y = produtividades_horarias[-1]
ax.annotate(
    f"({ponto_max_x:.1f}, {ponto_max_y:.1f})",
    xy=(ponto_max_x, ponto_max_y),
    xytext=(ponto_max_x - 0.1, ponto_max_y + 10),  # Ajustar o texto próximo ao ponto
    fontsize=10,
    arrowprops=dict(facecolor='black', arrowstyle="->"),  # Adiciona seta ao ponto
)

# Fixar os limites do gráfico
ax.set_xlim(0, 1.1)  # Limites fixos para o eixo X
ax.set_ylim(0, max(produtividades_horarias) * 1.1)  # Limite Y ajustado com margem de 10%

# Customizações do gráfico
ax.set_title("Nível de Carga vs Produtividade Horária")
ax.set_xlabel("Nível de Carga (Fator de Enchimento)")
ax.set_ylabel("Produtividade Horária (ton/h)")
ax.legend()
ax.grid(True)

# Exibir gráfico no Streamlit
st.pyplot(fig)

