import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import altair as alt
from datetime import datetime
import locale
import roman
import uuid
from fpdf import FPDF
from st_aggrid import AgGrid
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode
from st_aggrid.shared import GridUpdateMode


# Configurando a localização para o Brasil

from babel.numbers import format_currency

# Tenta configurar o locale para diferentes opções




# Configura a página para o modo wide
# st.set_page_config(layout="wide")
st.set_page_config(
    layout="wide",
    page_title="PCCR IDARON",
    page_icon="💰",
)


def format_currency_babel(value):
    return format_currency(value, 'BRL', locale='pt_BR')

# Adiciona estilo CSS para centralizar o título no topo
st.markdown(
    """
    <style>
    .title {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 10vh;
        font-size: 3rem;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título da página
st.markdown('<div class="title">Dados portal da Transparência IDARON RO</div>', unsafe_allow_html=True)

# Corpo da página
st.write("Dados baixados do último post do portal da transparência para a IDARON.")

# Criar um menu de opções
with st.sidebar:
    selected = option_menu(
        menu_title="PCCR IDARON",  # required
        options=["Métricas atuais", "Simular PCCR por Serv.", "Simular PCCR-FOLHA", "Mostrar Dados do Quadro", "Mostrar Dados", "Avaliar Dados", "Tabelas"],  # required
        icons=["bar-chart", "calculator", "file-earmark-text", "clipboard-data", "table", "clipboard-check", "grid"],  # updated with icon for "Avaliar Dados"
        menu_icon="cast",  # optional: icon for the menu
        default_index=0,  # optional: default index
    )
#Dataframes niveis    
data_nivel_superior = {
    "NIVEL": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"],
    "FORMAÇÃO REQUISITO PARA INGRESSO": [1111.64, 1144.98, 1179.34, 1214.71, 1251.15, 1288.69, 1327.35, 1367.17, 1408.19, 1450.43, 1493.94, 1538.77, 1584.93, 1632.47, 1681.45, 1731.90, 1783.85, 1837.36, 1892.48, 1949.26],
    "CAPACITAÇÃO": [1139.43, 1173.61, 1208.81, 1245.08, 1282.44, 1320.91, 1360.54, 1401.35, 1443.39, 1486.69, 1531.29, 1577.23, 1624.55, 1673.29, 1723.48, 1775.19, 1828.45, 1883.30, 1939.79, 1997.99],
    "ESPECIALIZAÇÃO": [1195.01, 1230.86, 1267.78, 1305.82, 1344.99, 1385.34, 1426.91, 1469.71, 1513.80, 1559.21, 1605.99, 1654.17, 1703.80, 1754.91, 1807.56, 1861.79, 1917.63, 1975.16, 2034.42, 2095.45],
    "GRADUAÇÃO POSTERIOR RELACIONADA ÁS ATRIBUIÇÕES DO CARGO": [1278.38, 1316.74, 1356.24, 1396.92, 1438.83, 1481.99, 1526.45, 1572.24, 1619.41, 1667.99, 1718.04, 1769.57, 1822.67, 1877.34, 1933.66, 1991.68, 2051.42, 2112.96, 2176.36, 2241.65],
    "MESTRADO": [1361.75, 1402.61, 1444.68, 1488.02, 1532.67, 1578.65, 1626.00, 1674.79, 1725.02, 1776.77, 1830.08, 1884.98, 1941.53, 1999.78, 2059.77, 2121.57, 2185.21, 2250.78, 2318.29, 2387.84],
    "DOUTORADO": [1445.13, 1488.48, 1533.14, 1579.13, 1626.50, 1675.30, 1725.55, 1777.32, 1830.64, 1885.57, 1942.13, 2000.39, 2060.40, 2122.22, 2185.88, 2251.46, 2319.00, 2388.58, 2460.23, 2534.04]
}

data_nivel_medio = {
    "NIVEL": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"],
    "FORMAÇÃO REQUISITO PARA INGRESSO": [719.92, 741.51, 763.76, 786.67, 810.28, 834.58, 859.62, 885.40, 911.96, 939.33, 967.50, 996.53, 1026.43, 1057.22, 1088.94, 1121.61, 1155.25, 1189.92, 1225.60, 1262.37],
    "CAPACITAÇÃO": [737.91, 760.05, 782.86, 806.34, 830.53, 855.44, 881.10, 907.54, 934.77, 962.81, 991.69, 1021.44, 1052.09, 1083.65, 1116.17, 1149.64, 1184.13, 1219.65, 1256.25, 1293.93],
    "GRADUAÇÃO": [773.91, 797.13, 821.04, 845.67, 871.05, 897.17, 924.09, 951.81, 980.37, 1009.78, 1040.07, 1071.27, 1103.41, 1136.51, 1170.60, 1205.72, 1241.90, 1279.15, 1317.53, 1357.05],
    "ESPECIALIZAÇÃO": [827.90, 852.74, 878.32, 904.67, 931.81, 959.76, 988.56, 1018.22, 1048.76, 1080.22, 1112.63, 1146.01, 1180.40, 1215.80, 1252.28, 1289.85, 1328.54, 1368.40, 1409.45, 1451.73],
    "MESTRADO": [881.90, 908.35, 935.60, 963.67, 992.58, 1022.37, 1053.04, 1084.62, 1117.16, 1150.68, 1185.19, 1220.76, 1257.38, 1295.10, 1333.95, 1373.97, 1415.19, 1457.64, 1501.37, 1546.41],
    "DOUTORADO": [935.89, 963.97, 992.89, 1022.67, 1053.35, 1084.96, 1117.50, 1151.03, 1185.55, 1221.13, 1257.76, 1295.49, 1334.35, 1374.38, 1415.62, 1458.08, 1501.83, 1546.89, 1593.29, 1641.09]
}

data_nivel_fundamental = {
    "NIVEL": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"],
    "FORMAÇÃO REQUISITO PARA INGRESSO": [661.69, 681.54, 701.98, 723.04, 744.73, 767.08, 790.09, 813.79, 838.20, 863.35, 889.26, 915.93, 943.41, 971.71, 1000.86, 1030.89, 1061.81, 1093.67, 1126.48, 1160.27],
    "CAPACITAÇÃO": [678.23, 698.57, 719.53, 741.12, 763.35, 786.25, 809.84, 834.14, 859.16, 884.94, 911.49, 938.82, 967.00, 996.00, 1025.88, 1056.66, 1088.36, 1121.02, 1154.64, 1189.28],
    "GRADUAÇÃO": [711.32, 732.65, 754.63, 777.28, 800.59, 824.61, 849.34, 874.82, 901.07, 928.10, 955.94, 984.62, 1014.16, 1044.59, 1075.93, 1108.20, 1141.45, 1175.70, 1210.96, 1247.30],
    "ESPECIALIZAÇÃO": [760.94, 783.77, 807.28, 831.50, 856.45, 882.14, 908.61, 935.86, 963.94, 992.86, 1022.64, 1053.32, 1084.92, 1117.47, 1150.99, 1185.52, 1221.08, 1257.71, 1295.45, 1334.31],
    "MESTRADO": [810.57, 834.88, 859.93, 885.73, 912.30, 939.67, 967.86, 996.89, 1026.80, 1057.61, 1089.34, 1122.01, 1155.68, 1190.35, 1226.06, 1262.84, 1300.72, 1339.74, 1379.94, 1421.34],
    "DOUTORADO": [860.19, 886.00, 912.58, 939.96, 968.16, 997.20, 1027.12, 1057.93, 1089.67, 1122.36, 1156.03, 1190.71, 1226.43, 1263.22, 1301.12, 1340.16, 1380.35, 1421.77, 1464.43, 1508.35]
}

# Define the DataFrame for "Valor do Ponto do Adic de Desempenho"
data_adic_desempenho = {
    "GRAU": ["A", "B", "C", "D", "E", "F"],
    "VALOR DO PONTO DO ADIC DE DESEMPENHO": [0.029, 0.031, 0.033, 0.038, 0.046, 0.059]
}


# Define the DataFrame for "Qualificação Horas Cursos"
data_horas_cursos = {
    "QUALIFICAÇÃO HORAS CURSOS": ["100 HORAS", "200 HORAS", "300 HORAS", "400 HORAS", "500 HORAS"],
    "PERCENTUAL": ["6,00%", "12,00%", "18,00%", "24,00%", "30,00%"]
}

# Define the DataFrame for "Qualificação Títulos"
data_titulos = {
    "QUALIFICAÇÃO TITULOS": ["FORM. REQ. INGRESSO", "GRADUAÇÃO", "ESPECIALIZAÇÃO", "MESTRADO", "DOUTORADO"],
    "PERCENTUAL": ["0%", "40%", "50%", "60%", "70%"]
}

# Define the DataFrame for "Índice de Adicional de Desempenho"
data_indice_desempenho = {
    "NIVEL": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"],
    "ÍNDICE DE ADICIONAL DE DESEMPENHO": [1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6, 1.65, 1.7, 1.75, 1.8, 1.85, 1.9, 2]
}

# Convertendo os dicionários para DataFrames do pandas
df_adic_desempenho = pd.DataFrame(data_adic_desempenho)
df_indice_desempenho = pd.DataFrame(data_indice_desempenho)


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Simulação de PCCR-FOLHA', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 6, body)  # Adjust the line height to 6
        self.ln(3)  # Reduce space after each block

def extrair_ano(data):
    try:
        return pd.to_datetime(data).year
    except:
        return None

def salario_base(ano, nivel_educacao):
    ano_atual = datetime.now().year
    anos_diferenca = ano_atual - ano
    
    if anos_diferenca % 2 != 0:
        anos_diferenca += 1
        
    nivel = anos_diferenca // 2
    nivel_romano = roman.toRoman(nivel)
    return nivel_romano, nivel

def calcular_produtividade(nivel_romano, grau, upf, pontos):
    df_adic_desempenho = pd.DataFrame(data_adic_desempenho)
    df_indice_desempenho = pd.DataFrame(data_indice_desempenho)
    
    valor_ponto = df_adic_desempenho[df_adic_desempenho["GRAU"] == grau]["VALOR DO PONTO DO ADIC DE DESEMPENHO"].values[0]
    indice_desempenho = df_indice_desempenho[df_indice_desempenho["NIVEL"] == nivel_romano]["ÍNDICE DE ADICIONAL DE DESEMPENHO"].values[0]
    
    adicional_produtividade = indice_desempenho * valor_ponto * upf * pontos
    return adicional_produtividade, indice_desempenho, valor_ponto

# Função para carregar e exibir dados filtrados por página
def carregar_e_exibir_dados():
    # Carregar a planilha de dados
    df = pd.read_excel('dados_completos.xlsx')
    
    # Convertendo valores monetários para float
    df['Total (Salário bruto)'] = df['Total (Salário bruto)'].replace({'R\$': '', '\.': '', ',': '.'}, regex=True).astype(float, errors='ignore')
    
    # Formatar valores monetários
    df['Total (Salário bruto)'] = df['Total (Salário bruto)'].apply(lambda x: f'R$ {x:,.2f}' if isinstance(x, (int, float)) else x)
    
    # Mostrar todos os dados em um expander
    with st.expander("Mostrar todos os dados", expanded=True):
        df.index = df.index + 1
        st.dataframe(df, use_container_width=True)

    # Obter os números de página únicos
    paginas = df['Número da Página'].unique()

    # Exibir os dados filtrados por página
    for pagina in paginas:
        with st.expander(f'Dados da Página {pagina}', expanded=False):
            df_pagina = df[df['Número da Página'] == pagina].reset_index(drop=True)
            df_pagina.index += 1  # Ajustar o índice para começar com 1
            df_pagina['Total (Salário bruto)'] = df_pagina['Total (Salário bruto)'].apply(lambda x: f'R$ {x:,.2f}' if isinstance(x, (int, float)) else x)
            st.dataframe(df_pagina, use_container_width=True)

def converter_para_numero(valor):
        if isinstance(valor, str):
            valor = valor.replace('R$', '').replace('.', '').replace(',', '.').strip()
            try:
                return float(valor)
            except ValueError:
                return 0.0
        return valor


# Função para exibir métricas atuais
def mostrar_metricas_atuais():
    # Carregar a planilha de dados
    df = pd.read_excel('dados_completos.xlsx')

    # Remover o símbolo de moeda e converter para float
    df['Total (Salário bruto)'] = df['Total (Salário bruto)'].replace({'R\$': '', '\.': '', ',': '.'}, regex=True).astype(float, errors='ignore')

    # Calcular o total do salário bruto
    total_salario_bruto = df['Total (Salário bruto)'].sum()
    # Calcular o valor anual
    total_salario_bruto_anual = total_salario_bruto * 12
    # Exibir a métrica total da folha
    st.metric(label="Total da folha", value=f"R$ {total_salario_bruto:,.2f}", delta=f"Anual (x 12): R$ {total_salario_bruto_anual:,.2f}", delta_color="off")

    # Filtrar os dados para 'Ativo - Efetivo'
    df_ativo_efetivo = df[df['Situação funcional'] == 'Ativo - Efetivo']
    df_outros = df[df['Situação funcional'] != 'Ativo - Efetivo']

    # Lista dos cargos para "Efetivo do quadro"
    cargos_efetivo_quadro = [
        'Idaron - Aux.de Serv. de Def. Agrosilv.',
        'Idaron - Agente de Dilig. e Transporte',
        'Idaron - Agente de Transporte Fluvial',
        'Idaron - Assist. de Gest. da Def. Agrop.',
        'Idaron - Assist. Estad. de Fisc. Agrop.',
        'Idaron - Fiscal Estadual Agropecuario',
        'Idaron - Analista de Tecnologia da Inf.',
        'Idaron - Contador',
        'Idaron - Economista',
        'Idaron - Pedagogo',
        'Idaron - Administrador',
        'Idaron - Procurador Estadual Autarquico',
        'Piloto de Aeronave'
    ]

    # Filtrar os dados para o grupo "Efetivo do quadro"
    df_efetivo_quadro = df_ativo_efetivo[df_ativo_efetivo['Cargo/Função/Emprego'].isin(cargos_efetivo_quadro)]
    # df_ativo_efetivo_restante = df_ativo_efetivo[~df_ativo_efetivo['Cargo/Função/Emprego'].isin(cargos_efetivo_quadro)]

    # Função para exibir métricas em colunas
    def exibir_metricas(df, total_salario_bruto):
        agrupado_por_cargo = df.groupby('Cargo/Função/Emprego').agg(
            total_salario_bruto=('Total (Salário bruto)', 'sum'),
            num_servidores=('Total (Salário bruto)', 'count')
        ).reset_index()
        agrupado_por_cargo['Porcentagem'] = (agrupado_por_cargo['total_salario_bruto'] / total_salario_bruto) * 100
        agrupado_por_cargo['total_salario_bruto'] = agrupado_por_cargo['total_salario_bruto'].apply(lambda x: f'R$ {x:,.2f}')

        # Criar colunas para exibir as métricas
        cols = st.columns(5)
        col_index = 0

        # Exibir as métricas para cada cargo
        for index, row in agrupado_por_cargo.iterrows():
            with cols[col_index]:
                st.metric(
                    label=f"{row['Cargo/Função/Emprego']}",
                    value=row['total_salario_bruto'],
                    delta=f"{row['Porcentagem']:.2f}% - {row['num_servidores']} servidores"
                )
            col_index = (col_index + 1) % 5

    # Exibir métricas para "Efetivo do quadro"
    st.subheader("Efetivo do quadro")
    exibir_metricas(df_efetivo_quadro, total_salario_bruto)

    # Separador
    st.markdown("---")

    # Exibir métricas para "Outros servidores"
    st.subheader("Outros servidores")
    exibir_metricas(df_outros, total_salario_bruto)

    # Separador
    st.markdown("---")

    # Gráfico de barras centralizado
    st.subheader("Participação de cada cargo na folha")

    # Preparar os dados para o gráfico
    agrupado_por_cargo = df.groupby('Cargo/Função/Emprego')['Total (Salário bruto)'].sum().reset_index()
    agrupado_por_cargo = agrupado_por_cargo.sort_values(by='Total (Salário bruto)', ascending=False)

    # Exibir dados para depuração
    col1, col2 = st.columns(2)

    with col1:
        st.write("Dados agrupados por cargo:", agrupado_por_cargo)
    with col2:
    # Criar o gráfico de barras com Altair
        chart_barras = alt.Chart(agrupado_por_cargo).mark_bar(color='red').encode(
            x=alt.X('Total (Salário bruto):Q', title='Total (Salário bruto)'),
            y=alt.Y('Cargo/Função/Emprego:N', sort='-x', title='Cargo/Função/Emprego'),
            tooltip=['Cargo/Função/Emprego', 'Total (Salário bruto)']
        ).properties(
            title='Custo Total por Cargo',
            width=550,
            height=500
        ).configure_axis(
            labelFontSize=10,
            titleFontSize=10
        ).configure_title(
            fontSize=14
        )
        # Exibir o gráfico de barras
        st.altair_chart(chart_barras, use_container_width=True)
        
    # Separador
    st.markdown("---")

    agrupado_por_cargo = df.groupby('Cargo/Função/Emprego').agg(
    total_salario_bruto=('Total (Salário bruto)', 'sum'),
    num_servidores=('Total (Salário bruto)', 'count')
    ).reset_index()

    agrupado_por_cargo['Custo por Servidor'] = agrupado_por_cargo['total_salario_bruto'] / agrupado_por_cargo['num_servidores']
    agrupado_por_cargo['Custo por Servidor Formatado'] = agrupado_por_cargo['Custo por Servidor'].apply(lambda x: f"R${x:.2f}")

    treemap_chart = alt.Chart(agrupado_por_cargo).mark_arc().encode(
        theta=alt.Theta(field="Custo por Servidor", type="quantitative"),
        color=alt.Color(field="Cargo/Função/Emprego", type="nominal"),
        tooltip=['Cargo/Função/Emprego', 'Custo por Servidor Formatado']
    ).properties(
        width=800,
        height=600,
        title='Participação Proporcional ao Nível de Servidor'
    )

    # Exibir o gráfico de treemap
    st.altair_chart(treemap_chart)
    st.markdown("---")

# Chamar a função apropriada com base na seleção do menu
if selected == "Mostrar Dados":
  
      
    carregar_e_exibir_dados()



elif selected == "Mostrar Dados do Quadro":

    # Função para exibir os dados filtrados no AgGrid
    def display_filtered_data(group_df, search_term):
        if search_term:
            filtered_group_df = group_df[group_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        else:
            filtered_group_df = group_df
        
        gb = GridOptionsBuilder.from_dataframe(filtered_group_df)
        gb.configure_selection('single', use_checkbox=True, groupSelectsChildren=True)
        gb.configure_default_column(editable=True, resizable=True)
        
        for col in filtered_group_df.columns:
            gb.configure_column(col, minWidth=250)
        
        grid_options = gb.build()
        
        grid_response = AgGrid(
            filtered_group_df,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.MODEL_CHANGED,
            fit_columns_on_grid_load=True
        )

        return grid_response

    # Título principal
    st.title("Mostrar Dados do Quadro")

    # Botão de atualização
    if st.button('Atualizar Dados'):
        st.experimental_rerun()

    # Carregar o dataframe (substitua pelo seu caminho correto)
    df = pd.read_excel('dados_completos.xlsx')  

    # Filtrar os dados conforme especificado
    filtered_df = df[(df['Nível'].notna()) & (df['Nível'] != 'None') & (df['Nível'] != 0)]

    # Obter lista única de cargos/funções/empregos
    cargos = filtered_df['Cargo/Função/Emprego'].unique()

    # Radio buttons para seleção de cargo
    selected_cargo = st.radio("Selecionar Cargo/Função/Emprego:", cargos)

    # Campo de pesquisa
    search_term = st.text_input(f"Pesquisar em {selected_cargo}", key=f"{selected_cargo}_search")

    # Filtrar dados pelo cargo selecionado
    filtered_group_df = filtered_df[filtered_df['Cargo/Função/Emprego'] == selected_cargo]

    # Exibir dados filtrados no AgGrid
    grid_response = display_filtered_data(filtered_group_df, search_term)

    # Capturar as linhas selecionadas
    selected_rows = grid_response.get('selected_rows', [])

    # Exibir dados selecionados automaticamente
    if selected_rows is not None and len(selected_rows) > 0:
        selected_df = pd.DataFrame(selected_rows)
        
        # Filtrar para remover colunas com valores 0 ou nulos na linha selecionada
        selected_df = selected_df.loc[:, (selected_df != 0).any(axis=0)]
        selected_df = selected_df.dropna(axis=1, how='all')

        # Mostrar cabeçalho e linha selecionada em duas colunas formatadas como uma tabela
        if not selected_df.empty:
            selected_header = list(selected_df.columns)
            selected_data = selected_df.iloc[0].tolist()  # Exibindo apenas a primeira linha selecionada

            table_data = list(zip(selected_header, selected_data))
            table_df = pd.DataFrame(table_data, columns=["Descrição", "Dados"])
            
            st.write("**Dados Selecionados:**")
            st.write(table_df.to_html(index=False), unsafe_allow_html=True)
    else:
        st.write("Nenhum dado selecionado.")

elif selected == "Simular PCCR-FOLHA":
    st.title("Simular PCCR-FOLHA")
    # Funções auxiliares
    def converter_para_numero(valor):
        if isinstance(valor, str):
            valor = valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
        try:
            return float(valor)
        except ValueError:
            return 0.0

    def format_currency_babel(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def processar_dataframe(df):
        df['VENCIMENTO'] = df['VENCIMENTO'].apply(converter_para_numero)
        df['Idaron - Adicional de Desempenho'] = df['Idaron - Adicional de Desempenho'].apply(converter_para_numero)

        df_agrupado = df.groupby(['Ano', 'Nível']).agg(
            Quantidade_Servidores=('Ano', 'size'),
            Total_Vencimento=('VENCIMENTO', 'sum'),
            Total_Adicional_Desempenho=('Idaron - Adicional de Desempenho', 'sum'),
        ).reset_index()

        df_agrupado['Total_Vencimento'] = df_agrupado['Total_Vencimento'].astype(float)
        df_agrupado['Total_Adicional_Desempenho'] = df_agrupado['Total_Adicional_Desempenho'].astype(float)

        df_agrupado['Total_Vencimento'] = df_agrupado['Total_Vencimento'].apply(format_currency_babel)
        df_agrupado['Total_Adicional_Desempenho'] = df_agrupado['Total_Adicional_Desempenho'].apply(format_currency_babel)
        return df_agrupado

    # Inicialização do estado da sessão se necessário
    if 'simulacoes' not in st.session_state:
        st.session_state.simulacoes = []

    if 'simulacoes_para_remover' not in st.session_state:
        st.session_state.simulacoes_para_remover = []

    if 'usar_pontuacao' not in st.session_state:
        st.session_state.usar_pontuacao = False

    if 'novo_pontos_medio' not in st.session_state:
        st.session_state.novo_pontos_medio = 0

    if 'novo_pontos_gestao' not in st.session_state:
        st.session_state.novo_pontos_gestao = 0

    if 'novo_pontos_fiscal' not in st.session_state:
        st.session_state.novo_pontos_fiscal = 0

    if 'novo_pontos_superior' not in st.session_state:
        st.session_state.novo_pontos_superior = 0

    def calcular_grau(ano_final, checkbox_state, dataframe_original, nivel_atual_str, radio_mestrado, radio_doutorado):
        grau_original = nivel_atual_str[-1]  # Assume que o grau é a última letra do valor da coluna 'Nível'
        ano_atual = datetime.now().year

        # Se a checkbox estiver desmarcada, retorne o grau original
        if not checkbox_state:
            return grau_original

        # Evolução automática do grau
        graus_por_nivel = ['D', 'E', 'F']
        
        # Se a checkbox do mestrado estiver marcada e o grau original for D, evolui para E
        if radio_mestrado and grau_original == 'D':
            return 'E'
        
        # Se a checkbox do doutorado estiver marcada e o grau original for E
        # E se passaram 3 anos ou mais, evolui para F
        if radio_doutorado and grau_original == 'E' and (ano_final - ano_atual) >= 3:
            return 'F'
        
        # Se a checkbox do doutorado estiver marcada e o grau original for D
        # E se passaram 3 anos ou mais, evolui para F
        if radio_doutorado and grau_original == 'D' and (ano_final - ano_atual) >= 3:
            return 'F'

        # Se a checkbox do doutorado estiver marcada e o grau original for D, evolui para E
        if radio_doutorado and grau_original == 'D':
            return 'E'

        return grau_original

    def determinar_nivel(ano_final, nivel_atual, ano_atual, checkbox_state, dataframe_original, nivel_atual_str, radio_mestrado, radio_doutorado, nivel_adicional):
        novo_grau = calcular_grau(ano_final, checkbox_state, dataframe_original, nivel_atual_str, radio_mestrado, radio_doutorado)
        
        if ano_final == ano_atual:
            return nivel_atual + nivel_adicional, novo_grau

        diferenca_anos = ano_final - ano_atual
        if diferenca_anos % 2 != 0:
            diferenca_anos += 1
        niveis_adicionais = diferenca_anos // 2
        novo_nivel = nivel_atual + niveis_adicionais + nivel_adicional

        return novo_nivel, novo_grau

    def obter_vencimento(dataframe_vencimentos, nivel, grau, nivel_educacao):
        cursos = {
            "A": "FORMAÇÃO REQUISITO PARA INGRESSO",
            "B": "CAPACITAÇÃO",
            "C": "GRADUAÇÃO" if nivel_educacao != "Nivel superior" else "ESPECIALIZAÇÃO",
            "D": "ESPECIALIZAÇÃO" if nivel_educacao != "Nivel superior" else "GRADUAÇÃO POSTERIOR RELACIONADA ÁS ATRIBUIÇÕES DO CARGO",
            "E": "MESTRADO",
            "F": "DOUTORADO"
        }
        
        curso = cursos.get(grau)
        if curso not in dataframe_vencimentos.columns:
            return 0.0
        
        vencimento = dataframe_vencimentos.loc[dataframe_vencimentos['NIVEL'] == roman.toRoman(nivel), curso].values
        if len(vencimento) > 0:
            return vencimento[0]
        return 0.0

    def desempenho(grau, nivel_roman, upf_value, pontos):
        valor_adic_desempenho = df_adic_desempenho.loc[df_adic_desempenho['GRAU'] == grau, 'VALOR DO PONTO DO ADIC DE DESEMPENHO'].values[0]
        indice_desempenho = df_indice_desempenho.loc[df_indice_desempenho['NIVEL'] == nivel_roman, 'ÍNDICE DE ADICIONAL DE DESEMPENHO'].values[0]
        valor_desempenho = upf_value * valor_adic_desempenho * indice_desempenho * pontos
        return valor_desempenho

    def exibir_totais(simulacao):
        totais_atuais = gerar_totais(simulacao['dataframes_processados'], simulacao['dataframes_processados'], "atuais", simulacao['pontos_medio'], simulacao['pontos_gestao'], simulacao['pontos_fiscal'], simulacao['pontos_superior'], simulacao['ano_final'])
        totais_simulados = gerar_totais(simulacao['dataframes_simulados'], simulacao['dataframes_processados'], "simulados", simulacao['pontos_medio'], simulacao['pontos_gestao'], simulacao['pontos_fiscal'], simulacao['pontos_superior'], simulacao['ano_final'])

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Valores Atuais")
            st.markdown(totais_atuais, unsafe_allow_html=True)
        with col2:
            st.markdown("### Totais Simulados")
            st.markdown(totais_simulados, unsafe_allow_html=True)

        st.markdown("---")

    def gerar_totais(dataframes_processados, dataframes_referencias, simulacao_tipo, pontos_medio, pontos_gestao, pontos_fiscal, pontos_superior, ano_final):
        totais = []
        total_vencimento_geral = 0.0
        total_desempenho_geral = 0.0
        total_diferenca_vencimento = 0.0
        total_diferenca_desempenho = 0.0

        for nome, df in dataframes_processados.items():
            df_referencia = dataframes_referencias.get(nome, pd.DataFrame())

            total_servidores = df['Qtd'].sum()
            total_vencimento = df['Total_Vencimento'].apply(converter_para_numero).sum()
            total_desempenho = df['Total_Adicional_Desempenho'].apply(converter_para_numero).sum()
            total_vencimento_geral += total_vencimento
            total_desempenho_geral += total_desempenho

            pontos = 0
            if nome == 'Nível Fundamental':
                pontos = pontos_medio
            elif nome == 'Assistentes de Gestão':
                pontos = pontos_gestao
            elif nome == 'Assistentes Fiscais':
                pontos = pontos_fiscal
            elif nome == 'Cargos de Nível Superior':
                pontos = pontos_superior

            totais.append(f"<div><b>{nome}:</b></div>")
            if simulacao_tipo == "atuais":
                totais.append(f"<div>. Total de Servidores: {total_servidores}</div>")
                totais.append(f"<div>. Total Salário Base: {format_currency_babel(total_vencimento)}</div>")
                totais.append(f"<div>. Total Adicional de Desempenho: {format_currency_babel(total_desempenho)}</div><br>")
            else:
                total_vencimento_referencia = df_referencia['Total_Vencimento'].apply(converter_para_numero).sum() if not df_referencia.empty else 0.0
                total_desempenho_referencia = df_referencia['Total_Adicional_Desempenho'].apply(converter_para_numero).sum() if not df_referencia.empty else 0.0

                if total_vencimento > 0:
                    diferenca_vencimento = total_vencimento - total_vencimento_referencia
                    total_diferenca_vencimento += diferenca_vencimento
                    totais.append(f"<div>. Pontos: {pontos} | Ano: {ano_final}</div>")
                    totais.append(f"<div>. Total Salário Base: {format_currency_babel(total_vencimento)} | Diferença: {format_currency_babel(diferenca_vencimento) if diferenca_vencimento != 0 else '-'}</div>")
                else:
                    totais.append(f"<div>. Pontos: {pontos} | Ano: {ano_final}</div>")
                    totais.append(f"<div>. Total Salário Base: {format_currency_babel(total_vencimento)}</div>")

                if total_desempenho > 0:
                    diferenca_desempenho = total_desempenho - total_desempenho_referencia
                    total_diferenca_desempenho += diferenca_desempenho
                    totais.append(f"<div>. Total Adicional de Desempenho: {format_currency_babel(total_desempenho)} | Diferença: {format_currency_babel(diferenca_desempenho) if diferenca_desempenho != 0 else '-'}</div>")
                else:
                    totais.append(f"<div>. Total Adicional de Desempenho: {format_currency_babel(total_desempenho)}</div>")

                totais.append("<br>")

        totais.append(f"<div><b>Total Geral:</b></div>")
        totais.append(f"<div>. Total Salário Base: {format_currency_babel(total_vencimento_geral)}</div>")
        totais.append(f"<div>. Total Adicional de Desempenho: {format_currency_babel(total_desempenho_geral)}</div><br>")

        if simulacao_tipo == "simulados":
            totais.append(f"<div><b>Diferença Somada:</b></div>")
            totais.append(f"<div>. Total Diferença Salário Base: {format_currency_babel(total_diferenca_vencimento)}</div>")
            totais.append(f"<div>. Total Diferença Adicional de Desempenho: {format_currency_babel(total_diferenca_desempenho)}</div>")
            totais.append(f"<div>. Total Diferença: {format_currency_babel(total_diferenca_vencimento + total_diferenca_desempenho)}</div>")
            totais.append(f"<div>. Total Diferença Anual (x12): {format_currency_babel((total_diferenca_vencimento + total_diferenca_desempenho) * 12)}</div><br>")

        return "".join(totais)
    

    def gerar_pdf(simulacao, totais_simulados):
        pdf = PDF()
        pdf.add_page()
        
        titulo_simulacao = simulacao['titulo_simulacao']
        pdf.chapter_title(titulo_simulacao)

        # Adicionando totais simulados no corpo do PDF
        pdf.chapter_body(totais_simulados)

        # Salvando PDF no buffer
        pdf_output = f"{titulo_simulacao.replace(' ', '_')}.pdf"
        pdf.output(pdf_output)
        
        return pdf_output
        # Simulação do PCCR-FOLHA
    def gerar_totais_pdf(simulacao):
        totais = []

        def format_currency(value):
            return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ",")

        for nome, df in simulacao['dataframes_processados'].items():
            if nome == 'Nível Fundamental':
                pontos_value = simulacao['pontos_medio']
            elif nome == 'Assistentes de Gestão':
                pontos_value = simulacao['pontos_gestao']
            elif nome == 'Assistentes Fiscais':
                pontos_value = simulacao['pontos_fiscal']
            elif nome == 'Cargos de Nível Superior':
                pontos_value = simulacao['pontos_superior']
            else:
                pontos_value = 0

            totais.append(f"{nome}:")
            totais.append(f"  Pontos: {pontos_value} | Ano: {simulacao['ano_final']}")

            total_salario_base = df['Total_Vencimento'].apply(converter_para_numero).sum()
            total_adicional_desempenho = df['Total_Adicional_Desempenho'].apply(converter_para_numero).sum()

            df_simulado = simulacao['dataframes_simulados'][nome]
            total_salario_base_simulado = df_simulado['Total_Vencimento'].apply(converter_para_numero).sum()
            total_adicional_desempenho_simulado = df_simulado['Total_Adicional_Desempenho'].apply(converter_para_numero).sum()

            diferenca_salario_base = total_salario_base_simulado - total_salario_base
            diferenca_adicional_desempenho = total_adicional_desempenho_simulado - total_adicional_desempenho

            totais.append(f"  Total Salário Base: {format_currency(total_salario_base_simulado)} | Diferença: {format_currency(diferenca_salario_base)}")
            totais.append(f"  Total Adicional de Desempenho: {format_currency(total_adicional_desempenho_simulado)} | Diferença: {format_currency(diferenca_adicional_desempenho)}")
            totais.append("")

        total_salario_base_geral = sum(df['Total_Vencimento'].apply(converter_para_numero).sum() for df in simulacao['dataframes_simulados'].values())
        total_adicional_desempenho_geral = sum(df['Total_Adicional_Desempenho'].apply(converter_para_numero).sum() for df in simulacao['dataframes_simulados'].values())
        total_diferenca_salario_base = total_salario_base_geral - sum(df['Total_Vencimento'].apply(converter_para_numero).sum() for df in simulacao['dataframes_processados'].values())
        total_diferenca_adicional_desempenho = total_adicional_desempenho_geral - sum(df['Total_Adicional_Desempenho'].apply(converter_para_numero).sum() for df in simulacao['dataframes_processados'].values())

        totais.append("Total Geral:")
        totais.append(f"  Total Salário Base: {format_currency(total_salario_base_geral)}")
        totais.append(f"  Total Adicional de Desempenho: {format_currency(total_adicional_desempenho_geral)}")
        totais.append("")

        totais.append("Diferença Somada:")
        totais.append(f"  Total Diferença Salário Base: {format_currency(total_diferenca_salario_base)}")
        totais.append(f"  Total Diferença Adicional de Desempenho: {format_currency(total_diferenca_adicional_desempenho)}")
        totais.append(f"  Total Diferença: {format_currency(total_diferenca_salario_base + total_diferenca_adicional_desempenho)}")
        totais.append(f"  Total Diferença Anual (x12): {format_currency((total_diferenca_salario_base + total_diferenca_adicional_desempenho) * 12)}")

        return "\n".join(totais)


    try:
        df_servidores = pd.read_excel('dados_completos.xlsx')
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
    else:
        df_filtrado = df_servidores[df_servidores['Nível'].notna() & (df_servidores['Nível'] != 0)]
        df_filtrado['Ano'] = df_filtrado['Data de admissão'].apply(lambda x: pd.to_datetime(x).year)
        df_filtrado['Ano'] = df_filtrado['Ano'].astype(str)

        cargos_fundamental = ['Idaron - Agente de Transporte Fluvial', 'Idaron - Agente de Dilig. e Transporte', 'Idaron - Aux.de Serv. de Def. Agrosilv.']
        cargo_gestao = 'Idaron - Assist. de Gest. da Def. Agrop.'
        cargo_fiscal = 'Idaron - Assist. Estad. de Fisc. Agrop.'

        df_nivel_fundamental = df_filtrado[df_filtrado['Cargo/Função/Emprego'].isin(cargos_fundamental)]
        df_assistentes_gestao = df_filtrado[df_filtrado['Cargo/Função/Emprego'] == cargo_gestao]
        df_assistentes_fiscais = df_filtrado[df_filtrado['Cargo/Função/Emprego'] == cargo_fiscal]
        df_nivel_superior = df_filtrado[~df_filtrado['Cargo/Função/Emprego'].isin(cargos_fundamental + [cargo_gestao, cargo_fiscal])]

        with st.expander("Servidores de Nível Fundamental"):
            df_fundamental = processar_dataframe(df_nivel_fundamental)
            st.dataframe(df_fundamental)
            total_servidores_fundamental = df_fundamental['Quantidade_Servidores'].sum()
            st.write(f"Total de Servidores: {total_servidores_fundamental}")

        with st.expander("Assistentes de Gestão"):
            df_gestao = processar_dataframe(df_assistentes_gestao)
            st.dataframe(df_gestao)
            total_servidores_gestao = df_gestao['Quantidade_Servidores'].sum()
            st.write(f"Total de Servidores: {total_servidores_gestao}")

        with st.expander("Assistentes Fiscais"):
            df_fiscal = processar_dataframe(df_assistentes_fiscais)
            st.dataframe(df_fiscal)
            total_servidores_fiscal = df_fiscal['Quantidade_Servidores'].sum()
            st.write(f"Total de Servidores: {total_servidores_fiscal}")

        with st.expander("Cargos de Nível Superior"):
            df_superior = processar_dataframe(df_nivel_superior)
            st.dataframe(df_superior)
            total_servidores_superior = df_superior['Quantidade_Servidores'].sum()
            st.write(f"Total de Servidores: {total_servidores_superior}")

        # Inicialize as variáveis fora do escopo dos checkboxes
        pontos_medio_input = 300
        pontos_gestao_input = 500
        pontos_fiscal_input = 1700
        pontos_superior_input = 3900
        st.markdown("---")
        # Define as colunas para os inputs
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            pontos_medio = st.number_input("Pontos", min_value=0, step=1, value=pontos_medio_input, key="pontos_medio", format="%d")
            simular_fundamental = st.checkbox("Simular Nível Fundamental")
            if simular_fundamental:
                tipo_salario_medio = st.radio(
                    "Tipo de Graduação",
                    ["MESTRADO", "DOUTORADO"],
                    key="tipo_salario_medio"
                )
                grau_fundamental = 'E' if tipo_salario_medio == 'MESTRADO' else 'F'
            else:
                grau_fundamental = ''

        with col2:
            pontos_gestao = st.number_input("Pontos", min_value=0, step=1, value=pontos_gestao_input, key="pontos_gestao", format="%d")
            simular_gestao = st.checkbox("Simular Assistentes de Gestão")
            if simular_gestao:
                tipo_salario_gestao = st.radio(
                    "Tipo de Graduação",
                    ["MESTRADO", "DOUTORADO"],
                    key="tipo_salario_gestao"
                )
                grau_gestao = 'E' if tipo_salario_gestao == 'MESTRADO' else 'F'
            else:
                grau_gestao = ''

        with col3:
            pontos_fiscal = st.number_input("Pontos", min_value=0, step=1, value=pontos_fiscal_input, key="pontos_fiscal", format="%d")
            simular_fiscal = st.checkbox("Simular Assistentes Fiscais")
            if simular_fiscal:
                tipo_salario_fiscal = st.radio(
                    "Tipo de Graduação",
                    ["MESTRADO", "DOUTORADO"],
                    key="tipo_salario_fiscal"
                )
                grau_fiscal = 'E' if tipo_salario_fiscal == 'MESTRADO' else 'F'
            else:
                grau_fiscal = ''

        with col4:
            pontos_superior = st.number_input("Pontos", min_value=0, step=1, value=pontos_superior_input, key="pontos_superior", format="%d")
            simular_superior = st.checkbox("Simular Cargos de Nível Superior")
            if simular_superior:
                tipo_salario_superior = st.radio(
                    "Tipo de Salário",
                    ["MESTRADO", "DOUTORADO"],
                    key="tipo_salario_superior"
                )
                grau_superior = 'E' if tipo_salario_superior == 'MESTRADO' else 'F'
            else:
                grau_superior = ''
        st.markdown("---")
        # Define as colunas para os inputs do UPF e Ano Final
        col1, col2, col3 = st.columns(3)
        with col1:
            upf_value = st.number_input("Valor do UPF", min_value=0.0, value=113.61)
        with col2:
            ano_final = st.number_input("Ano Final", min_value=2000, value=datetime.now().year)
        with col3:
            nivel_adicional = st.number_input("Adicionar Nível", min_value=0, value=0)   

        descricao_opcional = st.text_input("Descrição opcional")

        # Define as colunas para o botão "Simular" e o expander "Alterar Pontuação"
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Simular", key="simular_button_folha"):
                st.session_state.simulacoes_para_remover.clear()

                # Determinar quais pontuações usar
                if st.session_state.get("usar_pontuacao", False):
                    pontos_medio = st.session_state.get("novo_pontos_medio", pontos_medio)
                    pontos_gestao = st.session_state.get("novo_pontos_gestao", pontos_gestao)
                    pontos_fiscal = st.session_state.get("novo_pontos_fiscal", pontos_fiscal)
                    pontos_superior = st.session_state.get("novo_pontos_superior", pontos_superior)

                # Depuração
                st.write("Usando pontuações:")
                st.write(f"Pontos Médio: {pontos_medio}")
                st.write(f"Pontos Gestão: {pontos_gestao}")
                st.write(f"Pontos Fiscal: {pontos_fiscal}")
                st.write(f"Pontos Superior: {pontos_superior}")

                dataframes_processados = {
                    'Nível Fundamental': processar_dataframe(df_nivel_fundamental),
                    'Assistentes de Gestão': processar_dataframe(df_assistentes_gestao),
                    'Assistentes Fiscais': processar_dataframe(df_assistentes_fiscais),
                    'Cargos de Nível Superior': processar_dataframe(df_nivel_superior)
                }

                for key, df in dataframes_processados.items():
                    df.rename(columns={
                        'Ano': 'Ano',
                        'Nível': 'Nível',
                        'Quantidade_Servidores': 'Qtd',
                        'Total_Vencimento': 'Total_Vencimento',
                        'Total_Adicional_Desempenho': 'Total_Adicional_Desempenho'
                    }, inplace=True)

                # Criar dataframes simulados
                dataframes_simulados = {}
                for nome, df in dataframes_processados.items():
                    df_simulado = df.copy()
                    # Chamada da função determinar_nivel
                    for idx, row in df.iterrows():
                        nivel_atual_str = row['Nível']
                        try:
                            nivel_atual = int(''.join(filter(str.isdigit, nivel_atual_str)))
                        except ValueError:
                            nivel_atual = 0

                        if nome == 'Nível Fundamental':
                            novo_nivel, novo_grau = determinar_nivel(ano_final, nivel_atual, datetime.now().year, simular_fundamental, df_nivel_fundamental, nivel_atual_str, grau_fundamental == 'E', grau_fundamental == 'F', nivel_adicional)
                            vencimento = obter_vencimento(pd.DataFrame(data_nivel_fundamental), novo_nivel, novo_grau, "Nivel fundamental")
                            pontos = pontos_medio
                        elif nome == 'Assistentes de Gestão':
                            novo_nivel, novo_grau = determinar_nivel(ano_final, nivel_atual, datetime.now().year, simular_gestao, df_assistentes_gestao, nivel_atual_str, grau_gestao == 'E', grau_gestao == 'F', nivel_adicional)
                            vencimento = obter_vencimento(pd.DataFrame(data_nivel_medio), novo_nivel, novo_grau, "Nivel medio")
                            pontos = pontos_gestao
                        elif nome == 'Assistentes Fiscais':
                            novo_nivel, novo_grau = determinar_nivel(ano_final, nivel_atual, datetime.now().year, simular_fiscal, df_assistentes_fiscais, nivel_atual_str, grau_fiscal == 'E', grau_fiscal == 'F', nivel_adicional)
                            vencimento = obter_vencimento(pd.DataFrame(data_nivel_medio), novo_nivel, novo_grau, "Nivel medio")
                            pontos = pontos_fiscal
                        else:
                            novo_nivel, novo_grau = determinar_nivel(ano_final, nivel_atual, datetime.now().year, simular_superior, df_nivel_superior, nivel_atual_str, grau_superior == 'E', grau_superior == 'F', nivel_adicional)
                            vencimento = obter_vencimento(pd.DataFrame(data_nivel_superior), novo_nivel, novo_grau, "Nivel superior")
                            pontos = pontos_superior

                        df_simulado.at[idx, 'Nível'] = novo_nivel
                        df_simulado.at[idx, 'Grau'] = novo_grau
                        df_simulado.at[idx, 'Total_Vencimento'] = vencimento * row['Qtd']
                        df_simulado.at[idx, 'Total_Adicional_Desempenho'] = desempenho(novo_grau, roman.toRoman(novo_nivel), upf_value, pontos) * row['Qtd']

                    dataframes_simulados[nome] = df_simulado

                numero_simulacao = len(st.session_state.simulacoes) + 1
                titulo_simulacao = f"Simulação {numero_simulacao}: {descricao_opcional}" if descricao_opcional else f"Simulação {numero_simulacao}"
                simulacao_id = str(uuid.uuid4())

                st.session_state.simulacoes.append({
                    'titulo_simulacao': titulo_simulacao,
                    'descricao_opcional': descricao_opcional,
                    'dataframes_processados': dataframes_processados,
                    'dataframes_simulados': dataframes_simulados,
                    'simulacao_id': simulacao_id,
                    'checkbox_states': {
                        'simular_fundamental': simular_fundamental,
                        'simular_gestao': simular_gestao,
                        'simular_fiscal': simular_fiscal,
                        'simular_superior': simular_superior,
                    },
                    'upf_value': upf_value,
                    'ano_final': ano_final,
                    'pontos_medio': pontos_medio,
                    'pontos_gestao': pontos_gestao,
                    'pontos_fiscal': pontos_fiscal,
                    'pontos_superior': pontos_superior,
                    'grau_fundamental': grau_fundamental,
                    'grau_gestao': grau_gestao,
                    'grau_fiscal': grau_fiscal,
                    'grau_superior': grau_superior
                })

                if 'resultado_simulacao' not in st.session_state:
                    st.session_state.resultado_simulacao = ""
                
                totais_simulados = gerar_totais(dataframes_simulados, dataframes_processados, "simulados", pontos_medio, pontos_gestao, pontos_fiscal, pontos_superior, ano_final)
                
                # Extraindo apenas o bloco "Diferença Somada"
                diferenca_somada_index = totais_simulados.find('<div><b>Diferença Somada:</b></div>')
                st.session_state.resultado_simulacao = totais_simulados[diferenca_somada_index:]

                # Exibir o resumo da simulação
                st.markdown(f"### Diferença Somada")
                st.markdown(st.session_state.resultado_simulacao, unsafe_allow_html=True)

        with col2:
            with st.expander("Alterar Pontuação"):
                with st.form(key="form_cargos"):
                    porcentagem = st.number_input("Porcentagem", min_value=0, max_value=100, step=10, value=50, key="porcentagem")
                    direcao = st.radio("Direção", ["Para Mais", "Para Menos"], key="direcao")
                    col1, col2 = st.columns(2)

                    with col1:
                        cargo_fundamental = st.checkbox("Nível Fundamental", value=True)
                        cargo_gestao = st.checkbox("Assistentes de Gestão", value=True)
                        cargo_fiscal = st.checkbox("Assistentes Fiscais", value=True)
                        cargo_superior = st.checkbox("Nível Superior", value=True)
                        submitted = st.form_submit_button("Confirmar")

                        if submitted:
                            ajuste = (porcentagem / 100)
                            ajuste = ajuste if direcao == "Para Mais" else -ajuste

                            if cargo_fundamental:
                                st.session_state.novo_pontos_medio_temp = int(pontos_medio * (1 + ajuste))
                            else:
                                st.session_state.novo_pontos_medio_temp = pontos_medio

                            if cargo_gestao:
                                st.session_state.novo_pontos_gestao_temp = int(pontos_gestao * (1 + ajuste))
                            else:
                                st.session_state.novo_pontos_gestao_temp = pontos_gestao

                            if cargo_fiscal:
                                st.session_state.novo_pontos_fiscal_temp = int(pontos_fiscal * (1 + ajuste))
                            else:
                                st.session_state.novo_pontos_fiscal_temp = pontos_fiscal

                            if cargo_superior:
                                st.session_state.novo_pontos_superior_temp = int(pontos_superior * (1 + ajuste))
                            else:
                                st.session_state.novo_pontos_superior_temp = pontos_superior

                    with col2:
                        if 'novo_pontos_medio_temp' in st.session_state:
                            st.write(f"Novo Pontos Nível Fundamental: {st.session_state.novo_pontos_medio_temp}")
                        if 'novo_pontos_gestao_temp' in st.session_state:
                            st.write(f"Novo Pontos Assistentes de Gestão: {st.session_state.novo_pontos_gestao_temp}")
                        if 'novo_pontos_fiscal_temp' in st.session_state:
                            st.write(f"Novo Pontos Assistentes Fiscais: {st.session_state.novo_pontos_fiscal_temp}")
                        if 'novo_pontos_superior_temp' in st.session_state:
                            st.write(f"Novo Pontos Nível Superior: {st.session_state.novo_pontos_superior_temp}")

            st.session_state.usar_pontuacao = st.checkbox("Usar essa pontuação", value=st.session_state.usar_pontuacao)

    # Atualizar os pontos armazenados com base na checkbox
    if st.session_state.usar_pontuacao:
        st.session_state.novo_pontos_medio = st.session_state.get("novo_pontos_medio_temp", 0)
        st.session_state.novo_pontos_gestao = st.session_state.get("novo_pontos_gestao_temp", 0)
        st.session_state.novo_pontos_fiscal = st.session_state.get("novo_pontos_fiscal_temp", 0)
        st.session_state.novo_pontos_superior = st.session_state.get("novo_pontos_superior_temp", 0)
    else:
        st.session_state.novo_pontos_medio = 0
        st.session_state.novo_pontos_gestao = 0
        st.session_state.novo_pontos_fiscal = 0
        st.session_state.novo_pontos_superior = 0

    # Atualizar a seção onde as simulações são exibidas
    simulacoes_para_remover = []
    for simulacao_idx, simulacao in enumerate(st.session_state.simulacoes):
        st.markdown(f"### {simulacao['titulo_simulacao']}")
        st.write("#### FOLHA DE PONTO ATUAL")
        for nome, df in simulacao['dataframes_processados'].items():
            checkbox_states = simulacao['checkbox_states']
            ano_atual = datetime.now().year
            ano_final = simulacao['ano_final']
            grau_fundamental = simulacao['grau_fundamental']
            grau_gestao = simulacao['grau_gestao']
            grau_fiscal = simulacao['grau_fiscal']
            grau_superior = simulacao['grau_superior']
            pontos_medio = simulacao['pontos_medio']
            pontos_gestao = simulacao['pontos_gestao']
            pontos_fiscal = simulacao['pontos_fiscal']
            pontos_superior = simulacao['pontos_superior']

            df_zerado = pd.DataFrame({
                'Nível': [''] * len(df),
                'Grau': [''] * len(df),
                'Venc-Unitário': [''] * len(df),
                'Venc-Total': [''] * len(df),
                'Pontos': [''] * len(df),  # Adiciona a coluna Pontos
                'Desemp': [''] * len(df),
                'Desemp-Total': [''] * len(df)
            })

            for idx, row in df.iterrows():
                nivel_atual_str = row['Nível']
                try:
                    nivel_atual = int(''.join(filter(str.isdigit, nivel_atual_str)))
                except ValueError:
                    nivel_atual = 0

                if nome == 'Nível Fundamental':
                    novo_nivel, novo_grau = determinar_nivel(ano_final, nivel_atual, ano_atual, checkbox_states['simular_fundamental'], df_nivel_fundamental, nivel_atual_str, grau_fundamental == 'E', grau_fundamental == 'F', nivel_adicional)
                    vencimento = obter_vencimento(pd.DataFrame(data_nivel_fundamental), novo_nivel, novo_grau, "Nivel fundamental")
                    pontos = pontos_medio
                elif nome == 'Assistentes de Gestão':
                    novo_nivel, novo_grau = determinar_nivel(ano_final, nivel_atual, ano_atual, checkbox_states['simular_gestao'], df_assistentes_gestao, nivel_atual_str, grau_gestao == 'E', grau_gestao == 'F', nivel_adicional)
                    vencimento = obter_vencimento(pd.DataFrame(data_nivel_medio), novo_nivel, novo_grau, "Nivel medio")
                    pontos = pontos_gestao
                elif nome == 'Assistentes Fiscais':
                    novo_nivel, novo_grau = determinar_nivel(ano_final, nivel_atual, ano_atual, checkbox_states['simular_fiscal'], df_assistentes_fiscais, nivel_atual_str, grau_fiscal == 'E', grau_fiscal == 'F', nivel_adicional)
                    vencimento = obter_vencimento(pd.DataFrame(data_nivel_medio), novo_nivel, novo_grau, "Nivel medio")
                    pontos = pontos_fiscal
                else:
                    novo_nivel, novo_grau = determinar_nivel(ano_final, nivel_atual, ano_atual, checkbox_states['simular_superior'], df_nivel_superior, nivel_atual_str, grau_superior == 'E', grau_superior == 'F', nivel_adicional)
                    vencimento = obter_vencimento(pd.DataFrame(data_nivel_superior), novo_nivel, novo_grau, "Nivel superior")
                    pontos = pontos_superior

                df_zerado.at[idx, 'Nível'] = novo_nivel
                df_zerado.at[idx, 'Grau'] = novo_grau
                df_zerado.at[idx, 'Venc-Unitário'] = format_currency_babel(vencimento) if vencimento != 0 else "R$ 0,00"

                qtd = row['Qtd']
                venc_total = vencimento * qtd
                df_zerado.at[idx, 'Venc-Total'] = format_currency_babel(venc_total) if venc_total != 0 else "R$ 0,00"

                # Preencher a coluna Pontos
                df_zerado.at[idx, 'Pontos'] = pontos

                nivel_roman = roman.toRoman(novo_nivel)
                valor_desempenho = desempenho(novo_grau, nivel_roman, simulacao['upf_value'], pontos)
                df_zerado.at[idx, 'Desemp'] = format_currency_babel(valor_desempenho) if valor_desempenho != 0 else "R$ 0,00"

                desemp_total = valor_desempenho * qtd
                df_zerado.at[idx, 'Desemp-Total'] = format_currency_babel(desemp_total) if desemp_total != 0 else "R$ 0,00"

            with st.expander(f"{nome}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(df)
                with col2:
                    st.dataframe(df_zerado)

        # Exibir os totais
        exibir_totais(simulacao)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"Relat. gerado para a : {simulacao['titulo_simulacao']}")

        with col2:
            if st.button(f"Excluir Simulação {simulacao['titulo_simulacao']}", key=f"excluir_{simulacao_idx}"):
                st.session_state.simulacoes_para_remover.append(simulacao['simulacao_id'])

        with col3:
            if st.button(f"Gerar PDF {simulacao['titulo_simulacao']}", key=f"gerar_pdf_{simulacao_idx}"):
                totais_simulados = gerar_totais_pdf(simulacao)
                pdf_output = gerar_pdf(simulacao, totais_simulados)
                with open(pdf_output, "rb") as pdf_file:
                    st.download_button(label="Download PDF", data=pdf_file, file_name=pdf_output, mime="application/pdf")

    if st.session_state.simulacoes_para_remover:
        st.session_state.simulacoes = [sim for sim in st.session_state.simulacoes if sim['simulacao_id'] not in st.session_state.simulacoes_para_remover]
        st.session_state.simulacoes_para_remover.clear()
        st.experimental_rerun()

    st.markdown("---")



elif selected == "Simular PCCR por Serv.":
    st.title("Simular PCCR por Servidor.")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ano = st.number_input("Ano", min_value=2002, step=1)
    
    with col2:
        nivel_educacao = st.selectbox(
            "Nível de Educação",
            ["Nivel fundamental", "Nivel medio", "Nivel superior"]
        )
    
    with col3:
        upf = st.number_input("UPF", value=113.61)
    
    with col4:
        pontos = st.selectbox(
            "Pontos",
            [300, 500, 1700, 3900, "Outro"]
        )
        if pontos == "Outro":
            pontos = st.number_input("Digite um novo número de pontos", format="%d", step=1)
    
    graus_nivel_superior = {
        "FORMAÇÃO REQUISITO PARA INGRESSO": "A",
        "CAPACITAÇÃO": "B",
        "ESPECIALIZAÇÃO": "C",
        "GRADUAÇÃO POSTERIOR RELACIONADA ÁS ATRIBUIÇÕES DO CARGO": "D",
        "MESTRADO": "E",
        "DOUTORADO": "F"
    }
    
    graus_nivel_medio_fundamental = {
        "FORMAÇÃO REQUISITO PARA INGRESSO": "A",
        "CAPACITAÇÃO": "B",
        "GRADUAÇÃO": "C",
        "ESPECIALIZAÇÃO": "D",
        "MESTRADO": "E",
        "DOUTORADO": "F"
    }
    
    if nivel_educacao == "Nivel superior":
        selected_data = st.radio(
            "Tipo de Salário",
            list(graus_nivel_superior.keys()),
            key="tipo_salario_superior"
        )
        grau = graus_nivel_superior[selected_data]
    else:
        selected_data = st.radio(
            "Tipo de Salário",
            list(graus_nivel_medio_fundamental.keys()),
            key="tipo_salario_medio_fundamental"
        )
        grau = graus_nivel_medio_fundamental[selected_data]
    
    descricao = st.text_input("Descrição opcional da simulação", key="descricao_servidor")
    
    if 'global_simulation_id_servidor' not in st.session_state:
        st.session_state.global_simulation_id_servidor = 0
    
    if st.button("Simular", key="simular_button_servidor"):
        st.session_state.global_simulation_id_servidor += 1
        
        nivel_romano, nivel = salario_base(ano, nivel_educacao)
        
        if nivel_educacao == "Nivel superior":
            df = pd.DataFrame(data_nivel_superior)
            coluna_salario = 'FORMAÇÃO REQUISITO PARA INGRESSO'
        elif nivel_educacao == "Nivel medio":
            df = pd.DataFrame(data_nivel_medio)
            coluna_salario = 'FORMAÇÃO REQUISITO PARA INGRESSO'
        else:
            df = pd.DataFrame(data_nivel_fundamental)
            coluna_salario = 'FORMAÇÃO REQUISITO PARA INGRESSO'
        
        if coluna_salario not in df.columns:
            st.error(f"Coluna '{coluna_salario}' não encontrada no DataFrame.")
        else:
            salario_base_val = df[df["NIVEL"] == nivel_romano][coluna_salario].values[0]
            adicional_produtividade, indice_desempenho, valor_ponto = calcular_produtividade(nivel_romano, grau, upf, pontos)
            salario_final = salario_base_val + adicional_produtividade
            
            if 'simulacoes_servidor' not in st.session_state:
                st.session_state.simulacoes_servidor = []
            st.session_state.simulacoes_servidor.append({
                'simulacao_num': st.session_state.global_simulation_id_servidor,
                'descricao': descricao,
                'ano': ano,
                'nivel_educacao': nivel_educacao,
                'upf': upf,
                'pontos': pontos,
                'tipo_salario': selected_data,
                'salario_base': salario_base_val,
                'produtividade': adicional_produtividade,
                'salario_final': salario_final,
                'nivel_romano': nivel_romano,
                'grau': grau
            })
    
    st.markdown("---")
    
    def excluir_simulacao_servidor(simulacao_num):
        st.session_state.simulacoes_servidor = [sim for sim in st.session_state.simulacoes_servidor if sim['simulacao_num'] != simulacao_num]
    
    if 'simulacoes_servidor' in st.session_state:
        for simulacao in st.session_state.simulacoes_servidor:
            st.markdown(f"""
            ### Simulação {simulacao['simulacao_num']}
            - **Descrição**: {simulacao['descricao']}
            - **Ano**: {simulacao['ano']}
            - **Nível de Educação**: {simulacao['nivel_educacao']}
            - **UPF**: R$ {simulacao['upf']:.2f}
            - **Pontos**: {simulacao['pontos']}
            - **Tipo de Salário**: {simulacao['tipo_salario']}
            - **Salário Base**: R$ {simulacao['salario_base']:.2f}
            - **Produtividade**: Nível {simulacao['nivel_romano']} Grau {simulacao['grau']} - R$ {simulacao['produtividade']:.2f}
            - **Salário Final**: R$ {simulacao['salario_final']:.2f}
            """)
            if st.button(f"Excluir Simulação {simulacao['simulacao_num']}", key=f"excluir_{simulacao['simulacao_num']}_servidor_{st.session_state.global_simulation_id_servidor}_{simulacao['simulacao_num']}"):
                excluir_simulacao_servidor(simulacao['simulacao_num'])
                st.experimental_rerun()
            st.markdown("---")

elif selected == "Métricas atuais":
    mostrar_metricas_atuais()


elif selected == "Avaliar Dados":
    st.title("Avaliar Dados Baixados")
    def encontrar_divergencias(df_original, df_calculado):
        divergencias = df_original.copy()
        divergencias['Niv'] = df_calculado['Niv']
        divergencias['Grau'] = df_calculado['Grau']
        divergencias['Vencimento Calculado'] = df_calculado['Vencimento']
        divergencias['Desempenho Calculado'] = df_calculado['Desempenho']
        divergencias = divergencias[
            (divergencias['VENCIMENTO'] != divergencias['Vencimento Calculado']) | 
            (divergencias['Idaron - Adicional de Desempenho'] != divergencias['Desempenho Calculado'])
        ]
        return divergencias

    def obter_vencimento(dataframe_vencimentos, nivel, grau, nivel_educacao):
        cursos = {
            "A": "FORMAÇÃO REQUISITO PARA INGRESSO",
            "B": "CAPACITAÇÃO",
            "C": "GRADUAÇÃO" if nivel_educacao != "Nivel superior" else "ESPECIALIZAÇÃO",
            "D": "ESPECIALIZAÇÃO" if nivel_educacao != "Nivel superior" else "GRADUAÇÃO POSTERIOR RELACIONADA ÁS ATRIBUIÇÕES DO CARGO",
            "E": "MESTRADO",
            "F": "DOUTORADO"
        }
        
        curso = cursos.get(grau)
        if curso not in dataframe_vencimentos.columns:
            return 0.0
        
        vencimento = dataframe_vencimentos.loc[dataframe_vencimentos['NIVEL'] == roman.toRoman(nivel), curso].values
        if len(vencimento) > 0:
            return vencimento[0]
        return 0.0

    def format_currency_babel(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def desempenho(grau, nivel_roman, upf_value, pontos):
        valor_adic_desempenho = df_adic_desempenho.loc[df_adic_desempenho['GRAU'] == grau, 'VALOR DO PONTO DO ADIC DE DESEMPENHO'].values[0]
        indice_desempenho = df_indice_desempenho.loc[df_indice_desempenho['NIVEL'] == nivel_roman, 'ÍNDICE DE ADICIONAL DE DESEMPENHO'].values[0]
        valor_desempenho = upf_value * valor_adic_desempenho * indice_desempenho * pontos
        return valor_desempenho
    

    def render_table_if_not_empty(df, colunas_desejadas, title):
        if not df.empty:
            st.write(title)
            html = df[colunas_desejadas].to_html(index=False, classes='table table-striped')
            st.write(html, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True) 
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    try:
        df_servidores = pd.read_excel('dados_completos.xlsx')
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
    else:

        df_filtrado = df_servidores[df_servidores['Nível'].notna() & (df_servidores['Nível'] != 0)]
        df_filtrado['Ano'] = df_filtrado['Data de admissão'].apply(lambda x: pd.to_datetime(x).year)
        df_filtrado['Ano'] = df_filtrado['Ano'].astype(str)

        cargos_fundamental = ['Idaron - Agente de Transporte Fluvial', 'Idaron - Agente de Dilig. e Transporte', 'Idaron - Aux.de Serv. de Def. Agrosilv.']
        cargo_gestao = 'Idaron - Assist. de Gest. da Def. Agrop.'
        cargo_fiscal = 'Idaron - Assist. Estad. de Fisc. Agrop.'

        df_nivel_fundamental = df_filtrado[df_filtrado['Cargo/Função/Emprego'].isin(cargos_fundamental)]
        df_assistentes_gestao = df_filtrado[df_filtrado['Cargo/Função/Emprego'] == cargo_gestao]
        df_assistentes_fiscais = df_filtrado[df_filtrado['Cargo/Função/Emprego'] == cargo_fiscal]
        df_nivel_superior = df_filtrado[~df_filtrado['Cargo/Função/Emprego'].isin(cargos_fundamental + [cargo_gestao, cargo_fiscal])]

        colunas_desejadas = [
            'Nome do Servidor', 'VENCIMENTO', 'Idaron - Adicional de Desempenho', 'Nível'
        ]

        pontos_medio_input = 300
        pontos_gestao_input = 500
        pontos_fiscal_input = 1700
        pontos_superior_input = 3900
        # Criar quatro colunas com os inputs de pontos e UPF
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            pontos_medio = st.number_input("Pontos Nível Fundamental", min_value=0, step=1, value=pontos_medio_input, key="pontos_medio", format="%d")

        with col2:
            pontos_gestao = st.number_input("Pontos Assistentes de Gestão", min_value=0, step=1, value=pontos_gestao_input, key="pontos_gestao", format="%d")

        with col3:
            pontos_fiscal = st.number_input("Pontos Assistentes Fiscais", min_value=0, step=1, value=pontos_fiscal_input, key="pontos_fiscal", format="%d")

        with col4:
            pontos_superior = st.number_input("Pontos Cargos de Nível Superior", min_value=0, step=1, value=pontos_superior_input, key="pontos_superior", format="%d")

        with col5:
            upf = st.number_input("UPF", value=113.61)

        # Função para calcular vencimento e desempenho e processar o dataframe
        def calcular_vencimento_desempenho(dataframe, tabela_vencimentos, nivel_educacao, pontos, upf):
            dataframe['Niv'] = dataframe['Nível'].str.extract('(\d+)').astype(int)
            dataframe['Grau'] = dataframe['Nível'].str.extract('([A-Za-z]+)')
            dataframe['Vencimento'] = dataframe.apply(lambda row: obter_vencimento(tabela_vencimentos, row['Niv'], row['Grau'], nivel_educacao), axis=1)
            dataframe['Desempenho'] = dataframe.apply(lambda row: desempenho(row['Grau'], roman.toRoman(row['Niv']), upf, pontos), axis=1)
            dataframe['Vencimento'] = dataframe['Vencimento'].apply(format_currency_babel)
            dataframe['Desempenho'] = dataframe['Desempenho'].apply(format_currency_babel)
            return dataframe[['Niv', 'Grau', 'Vencimento', 'Desempenho']]

        # Tabelas de vencimentos
        tabela_vencimentos_superior = pd.DataFrame(data_nivel_superior)
        tabela_vencimentos_medio = pd.DataFrame(data_nivel_medio)
        tabela_vencimentos_fundamental = pd.DataFrame(data_nivel_fundamental)

        # Exibir os dados filtrados nos expansores
        with st.expander("Servidores de Nível Fundamental"):
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(df_nivel_fundamental[colunas_desejadas])
            with col2:
                df_fundamental_vencimento = calcular_vencimento_desempenho(df_nivel_fundamental.copy(), tabela_vencimentos_fundamental, "Nivel medio", pontos_medio, upf)
                st.dataframe(df_fundamental_vencimento)

        with st.expander("Assistentes de Gestão"):
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(df_assistentes_gestao[colunas_desejadas])
            with col2:
                df_gestao_vencimento = calcular_vencimento_desempenho(df_assistentes_gestao.copy(), tabela_vencimentos_medio, "Nivel medio", pontos_gestao, upf)
                st.dataframe(df_gestao_vencimento)

        with st.expander("Assistentes Fiscais"):
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(df_assistentes_fiscais[colunas_desejadas])
            with col2:
                df_fiscais_vencimento = calcular_vencimento_desempenho(df_assistentes_fiscais.copy(), tabela_vencimentos_medio, "Nivel medio", pontos_fiscal, upf)
                st.dataframe(df_fiscais_vencimento)

        with st.expander("Cargos de Nível Superior"):
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(df_nivel_superior[colunas_desejadas])
            with col2:
                df_superior_vencimento = calcular_vencimento_desempenho(df_nivel_superior.copy(), tabela_vencimentos_superior, "Nivel superior", pontos_superior, upf)
                st.dataframe(df_superior_vencimento)

        st.markdown("---")
        st.write("Divergências")

        # Encontrar e exibir divergências
        colunas_desejadas_divergencias = [
            'Nome do Servidor', 'Nível', 'Niv', 'Grau', 'VENCIMENTO', 'Idaron - Adicional de Desempenho', 'Vencimento Calculado', 'Desempenho Calculado'
        ]

        # Divergências Nível Fundamental
        divergencias_fundamental = encontrar_divergencias(df_nivel_fundamental, df_fundamental_vencimento)
        render_table_if_not_empty(divergencias_fundamental, colunas_desejadas_divergencias, "Divergências Nível Fundamental")

        # Divergências Assistentes de Gestão
        divergencias_gestao = encontrar_divergencias(df_assistentes_gestao, df_gestao_vencimento)
        render_table_if_not_empty(divergencias_gestao, colunas_desejadas_divergencias, "Divergências Assistentes de Gestão")

        # Divergências Assistentes Fiscais
        divergencias_fiscais = encontrar_divergencias(df_assistentes_fiscais, df_fiscais_vencimento)
        render_table_if_not_empty(divergencias_fiscais, colunas_desejadas_divergencias, "Divergências Assistentes Fiscais")

        # Divergências Cargos de Nível Superior
        divergencias_superior = encontrar_divergencias(df_nivel_superior, df_superior_vencimento)
        render_table_if_not_empty(divergencias_superior, colunas_desejadas_divergencias, "Divergências Cargos de Nível Superior")









 
elif selected == "Tabelas":
    df_nivel_superior = pd.DataFrame(data_nivel_superior)
    html_table = df_nivel_superior.to_html(index=False)
    st.markdown(f"### Tabela I - Cargos das Carreiras de Nível Superior")
    st.markdown(html_table, unsafe_allow_html=True)

    st.markdown("---")
    df_nivel_medio = pd.DataFrame(data_nivel_medio)
    html_table = df_nivel_medio.to_html(index=False)
    st.markdown(f"### Tabela II - Cargos das Carreiras de Nível Médio")
    st.markdown(html_table, unsafe_allow_html=True)

    st.markdown("---")
    df_fundamental = pd.DataFrame(data_nivel_fundamental)
    html_table = df_fundamental.to_html(index=False)
    st.markdown(f"### Tabela III - Cargos das Carreiras de Nível Fundamental")
    st.markdown(html_table, unsafe_allow_html=True)

    st.markdown("---")
    df_adic_desempenho = pd.DataFrame(data_adic_desempenho)
    html_table_adic_desempenho = df_adic_desempenho.to_html(index=False)
    st.markdown(f"### Tabela - Valor do Ponto do Adicional de Desempenho")
    st.markdown(html_table_adic_desempenho, unsafe_allow_html=True)

    st.markdown("---")
    df_horas_cursos = pd.DataFrame(data_horas_cursos)
    html_table_horas_cursos = df_horas_cursos.to_html(index=False)
    st.markdown(f"### Tabela - Qualificação Horas Cursos")
    st.markdown(html_table_horas_cursos, unsafe_allow_html=True)

    st.markdown("---")
    df_titulos = pd.DataFrame(data_titulos)
    html_table_titulos = df_titulos.to_html(index=False)
    st.markdown(f"### Tabela - Qualificação Títulos")
    st.markdown(html_table_titulos, unsafe_allow_html=True)

    st.markdown("---")
    df_indice_desempenho = pd.DataFrame(data_indice_desempenho)
    html_table_indice_desempenho = df_indice_desempenho.to_html(index=False)
    st.markdown(f"### Tabela - Índice de Adicional de Desempenho")
    st.markdown(html_table_indice_desempenho, unsafe_allow_html=True)