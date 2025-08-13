# 📍 Busca CEP

Um sistema simples para consultar endereços a partir de CEPs no Brasil utilizando a API [ViaCEP](https://viacep.com.br/).  

O projeto permite consultar **CEP único** ou **vários CEPs via planilha Excel**.

---

## Funcionalidades

- 🔎 Consulta de CEP individual.
- 📂 Consulta de múltiplos CEPs através de planilha `.xlsx`.
- ✅ Geração de planilha de resultados com duas abas:
  - `CEPs encontrados`
  - `CEPs inválidos`
- Formato de saída: Excel sem índices adicionais.
- Interface web interativa via **Streamlit**.

---

## 📦 Pré-requisitos

- Python 3.8 ou superior
- Bibliotecas:
  ```bash
  pip install streamlit pandas requests openpyxl
  ```

## 🚀 Como executar
### 1️⃣ Clonar o repositório:

 ``` bash
git clone https://github.com/Schusban/busca_cep.git
cd busca_cep
 ```

### 2️⃣ Instalar dependências
Certifique-se de ter o **Python 3.10+** instalado e, em seguida, instale as bibliotecas necessárias:

```bash
pip install streamlit pandas requests openpyxl
```

## 3️⃣Execute o app Streamlit:
 ``` bash
streamlit run consulta_cep.py
 ```
Acesse a interface no navegador (geralmente em http://localhost:8501).

## 📄 Formato da planilha Excel

- **Aba obrigatória:** `CEP`  
- **Coluna obrigatória:** `CEP`


Exemplo de planilha modelo:

| CEP        |
|------------|
| 01001-000  |
| 20040-020  |


O app fornece um botão para baixar a planilha modelo já no formato correto.
