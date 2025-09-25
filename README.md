# Projeto FIAP Fase 1

## Descrição do Projeto

- Este projeto realiza scraping do site https://books.toscrape.com/, normalize os dados coletados e disponibiliza rotas REST para consultar e filtrar os livros. Foi desenvolvido para demonstrar conceitos de coleta de dados, tratamento, e exposição via API (FastAPI).

#### Principais Objetivos
- Extrair metadados dos livros (__título, categoria, imagem, avaliação, preço__).

- Armazenar e disponibilizar os dados via API.

- Autenticação via JWT para proteger endpoints sensíveis.

- Deploy em Render.


## Como Reproduzir o Projeto

### Pré-requisito
- Python -> 3.10+
- Git

### Configuração - Variáveis de Ambiente
- Crie um arquivo .env com as seguintes variaveis:

```
SECRET_KEY = "4b6f8a10e53c47a9d2f3b13f93d25a9e4c71f0d9e1a6f62c12d9f6a7b05b3c2f";
ALGORITHM = "HS256"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"
PORT = 8000
```

### Passo a Passo para Rodar Localmente
1. Clonar o repositório:
> *git clone https://github.com/vinisouz4/FIAP_projeto_fase_1.git*

2. Acessar a pasta do projeto 
> *cd {seu-caminho}*

3. Criar um ambiente virtual 
> *python -m venv venv*
- Ativar a venv (Linux/Mac): *source venv/bin/activate*
- Ativar a venv (Windows): *venv\Scripts\activate*

4. Instale as dependências
> *pip install -r requirements.txt*

5. Rodar o projeto localmente
> *uvicorn run:app --reload*

6. Acessar o swagger
- http://localhost:8000/docs


## API
> URL API: *https://fiap-projeto-fase-1.onrender.com/docs* 

#### Autenticação
- Usuário padrão (para testes): __admin/admin__ - apenas para teste e validação do projeto;
- O endpoint /auth/login, retorna um JWT com período de experiação determinado dentro do código;
- No Swagger UI, clique em Authorize e cole o Bearer {token}

#### Endpoints
- 


