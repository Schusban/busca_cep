import streamlit as st
import pandas as pd
import requests
import time
from io import BytesIO

def obter_endereco_por_cep(cep):
    """
    Consulta a API ViaCEP para obter informações de endereço com base no CEP.

    Parâmetros:
    cep (str): O CEP para o qual o endereço deve ser consultado.

    Retorna:
    dict: Retorna um dicionário contendo informações do endereço ou None se o CEP não for encontrado.
    """
    try:
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        endereco = response.json()
        return endereco if "erro" not in endereco else None
    except requests.RequestException:
        return None

def processar_planilha(planilha):
    """
    Processa uma planilha Excel contendo CEPs e retorna dois DataFrames:
    CEPs válidos e CEPs inválidos.

    Parâmetros:
    planilha (UploadedFile): Arquivo Excel enviado pelo usuário via Streamlit.

    Retorna:
    Tuple[pd.DataFrame, pd.DataFrame]: DataFrames com CEPs encontrados e CEPs inválidos.
    """
    planilha_cep = pd.read_excel(planilha, sheet_name='CEP')
    ceps = planilha_cep['CEP'].dropna()

    encontrados = []
    invalidos = []

    with st.spinner('Consultando CEPs, aguarde...'):
        for cep in ceps:
            cep_formatado = str(cep).replace('-', '')
            endereco = obter_endereco_por_cep(cep_formatado)

            if endereco:
                encontrados.append({
                    'CEP': cep,
                    'Logradouro': endereco.get('logradouro', ''),
                    'Bairro': endereco.get('bairro', ''),
                    'Localidade': endereco.get('localidade', ''),
                    'UF': endereco.get('uf', ''),
                })
            else:
                invalidos.append({'CEP': cep})

            time.sleep(0.3)

    df_encontrados = pd.DataFrame(encontrados)
    df_invalidos = pd.DataFrame(invalidos)
    return df_encontrados, df_invalidos

def processar_cep_unico(cep):
    """
    Processa um CEP único e retorna um DataFrame somente se válido.

    Parâmetros:
    cep (str): CEP a ser consultado.

    Retorna:
    pd.DataFrame ou None: DataFrame com dados do CEP, ou None se inválido.
    """
    cep_formatado = str(cep).replace('-', '')
    endereco = obter_endereco_por_cep(cep_formatado)

    if endereco:
        df = pd.DataFrame([{
            'CEP': cep,
            'Logradouro': endereco.get('logradouro', ''),
            'Bairro': endereco.get('bairro', ''),
            'Localidade': endereco.get('localidade', ''),
            'UF': endereco.get('uf', ''),
        }])
        return df
    else:
        return None

# -------------------- Interface Streamlit --------------------
# -------------------- Planilha modelo para o usuário --------------------
st.subheader("📄 Baixar planilha modelo")

# Cria um DataFrame com duas linhas de exemplo
df_modelo = pd.DataFrame({
    'CEP': ['01001-000', '20040-020']  # exemplos válidos de CEP com ou sem traço
})

# Cria o arquivo Excel em memória
output_modelo = BytesIO()
with pd.ExcelWriter(output_modelo, engine='openpyxl') as writer:
    df_modelo.to_excel(writer, sheet_name='CEP', index=False)
modelo_bytes = output_modelo.getvalue()

# Botão de download
st.download_button(
    label="📥 Baixar planilha modelo",
    data=modelo_bytes,
    file_name="planilha_modelo_cep.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


st.set_page_config(page_title="Consulta de Endereços por CEP", layout="wide")
st.title("📍 Busque endereços pelo número do CEP")

st.markdown("""
Bem-vindo ao sistema de consulta de endereços por CEP.

**Funcionalidades:**
1. Busque endereços individualmente pelo número do CEP.
2. Ou carregue uma planilha Excel contendo vários CEPs.

**Formato da planilha Excel:**
- Aba: `CEP`
- Coluna obrigatória: `CEP`
- Os CEPs podem conter ou não o traço (`-`)
""")

# Consulta individual de CEP
st.subheader("🔎 Consultar CEP único")
cep_input = st.text_input("Digite um CEP para consulta:")

if st.button("Consultar CEP"):
    if cep_input:
        df_cep = processar_cep_unico(cep_input)
        if df_cep is not None:
            st.success("Endereço encontrado:")
            st.dataframe(df_cep.reset_index(drop=True))
        else:
            st.warning("CEP não encontrado ou inválido.")
    else:
        st.warning("Digite um CEP válido.")

st.markdown("---")
st.subheader("📂 Consultar CEPs via planilha Excel")

uploaded_file = st.file_uploader(
    "Carregue sua planilha (.xlsx) com a aba 'CEP'", type=["xlsx"]
)

if uploaded_file:
    df_encontrados, df_invalidos = processar_planilha(uploaded_file)

    if not df_encontrados.empty or not df_invalidos.empty:
        st.success("Consulta concluída!")

        if not df_encontrados.empty:
            st.subheader("✅ CEPs encontrados")
            st.dataframe(df_encontrados.reset_index(drop=True))

        if not df_invalidos.empty:
            st.subheader("❌ CEPs inválidos")
            st.dataframe(df_invalidos.reset_index(drop=True))

        # Salvar em Excel com duas abas sem índice
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            if not df_encontrados.empty:
                df_encontrados.to_excel(writer, sheet_name='CEPs encontrados', index=False)
            if not df_invalidos.empty:
                df_invalidos.to_excel(writer, sheet_name='CEPs inválidos', index=False)
        processed_data = output.getvalue()

        st.download_button(
            label="📥 Baixar planilha com resultados",
            data=processed_data,
            file_name="enderecos_resultados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("Nenhum CEP encontrado. Verifique os dados na planilha.")
