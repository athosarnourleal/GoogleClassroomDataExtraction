# Criador Automático de Planilha (Classroom para Sheets) 📊🎓

Este é um projeto em Python que automatiza a extração de notas de alunos do **Google Classroom** e exporta esses dados diretamente para uma planilha formatada no **Google Sheets**. Ele possui uma interface gráfica amigável construída com **Streamlit**, permitindo que os professores selecionem suas turmas e atividades com facilidade.

## Funcionalidades

- **Integração com Google Classroom:** Autenticação segura via OAuth2 para listar cursos, alunos e atividades.
- **Extração de Notas:** Captura automática das notas das atividades selecionadas (sejam elas atribuídas ou em rascunho).
- **Processamento de Dados:** Consolidação das notas usando a biblioteca `pandas`.
- **Exportação para Google Sheets:** Criação automática de planilhas com formatação visual (cores, alinhamento, tamanhos de células) usando a API do Google Sheets e `gspread`.
- **Fórmulas Dinâmicas:** Insere fórmulas nativas do Google Sheets automaticamente (ex: cálculo da soma das atividades e nota final).
- **Interface Web:** Interface simples e iterativa via **Streamlit** para gerenciamento de todo o fluxo.

## Tecnologias Utilizadas

- **Linguagem:** Python
- **Interface Gráfica:** Streamlit
- **Manipulação de Dados:** Pandas, Numpy
- **Google APIs:** 
  - `google-api-python-client` (Classroom)
  - `google-auth`, `google-auth-oauthlib`
  - `gspread` (Sheets)
- **Outros:** `python-dotenv`

## Estrutura do Projeto

```text
├── interface/
│   └── app.py                            # Interface principal do Streamlit
├── scripts/
│   ├── ClassroomDataExtractor.py         # Lógica de manipulação de dados com Pandas
│   ├── google_classrom_connection.py     # Gerenciamento da API do Google Classroom (OAuth)
│   └── google_sheets_connection.py       # Conexão e formatação via API do Google Sheets
├── google credentials/                   # Pasta para os arquivos de credenciais (IMPORTANTE)
│   ├── credentials_client_google_classroom.json # Credencial OAuth (Classroom)
│   └── credentials_service_googleSheets.json    # Credencial de Conta de Serviço (Sheets)
└── README.md
```

## Pré-requisitos e Configuração

### 1. Clonar o Repositório e Instalar Dependências

Crie um ambiente virtual, ative-o e instale as dependências (você precisará criar um `requirements.txt` ou instalá-las manualmente):

```bash
# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# Instale os pacotes principais
pip install streamlit pandas numpy gspread google-api-python-client google-auth-httplib2 google-auth-oauthlib python-dotenv
```

### 2. Configurar Credenciais do Google Cloud

Este projeto necessita de duas credenciais distintas criadas no **Google Cloud Console**:

1. **Google Classroom (OAuth 2.0 Client IDs):** 
   - Crie uma credencial OAuth.
   - Baixe o JSON, renomeie para `credentials_client_google_classroom.json` e coloque na pasta `google credentials/`.
   - *Nota: Na primeira execução, ele abrirá o navegador para você logar na sua conta e gerará um arquivo `token.json`.*

2. **Google Sheets (Service Account):**
   - Crie uma Conta de Serviço (Service Account).
   - Gere uma chave (JSON) para ela.
   - Baixe o JSON, renomeie para `credentials_service_googleSheets.json` e coloque na pasta `google credentials/`.
   - *Importante: Não se esqueça de compartilhar a planilha de destino (o link que estiver em uso no código) com o e-mail gerado pela sua Conta de Serviço.*

## Como Executar

Após configurar as credenciais e o ambiente, inicie a aplicação Streamlit:

```bash
# Vá para a raiz do projeto (se não estiver)
# Ative o ambiente virtual: source .venv/bin/activate
streamlit run interface/app.py
```

O seu navegador padrão abrirá automaticamente na página da aplicação (geralmente em `http://localhost:8501`).

## Como Usar o App

1. Clique em **"conectar"** para autenticar com sua conta do Google (para ter acesso ao Classroom).
2. Escolha a turma (curso) desejada na lista de cursos disponíveis e clique em **"confirmar"**.
3. Selecione as atividades (checkbox) que deseja extrair as notas.
4. Clique em **"carregar dados de notas"**. A tabela será gerada e exibida na tela.
5. Insira o título da planilha desejada e clique em **"export to google sheet"** para enviar a tabela formatada para a nuvem.
