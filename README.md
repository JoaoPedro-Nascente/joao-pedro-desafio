````markdown
# 💰 API REST - Controle Financeiro Pessoal

Este repositório contém o backend da aplicação de Controle Financeiro Pessoal, desenvolvido utilizando **Django** e **Django REST Framework (DRF)**.

A API é responsável por gerenciar dados de transações (receitas e despesas), calcular o saldo em tempo real e fornecer segurança através de autenticação JWT.

## 🛠️ Tecnologias e Dependências

* **Linguagem:** Python 3.12+
* **Framework Web:** Django 5.x
* **API Framework:** Django REST Framework
* **Autenticação:** Simple JWT
* **Banco de Dados:** SQLite (padrão de desenvolvimento)
* **Testes e Cobertura:** `unittest` (integrado ao Django) e `coverage.py`
* **Segurança:** `django-cors-headers`

## ⚙️ Configuração e Instalação

Siga os passos abaixo para configurar o projeto localmente.

### 1. Clonar o Repositório e Configurar o Ambiente

```bash
# Clone o projeto (se ainda não o fez)
git clone https://github.com/JoaoPedro-Nascente/joao-pedro-desafio
cd joao-pedro-desafio

# Crie e ative o ambiente virtual
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Linux/Mac
````

### 2\. Instalar Dependências

Instale os pacotes Python necessários (Django, DRF, JWT, CORS, etc.):

```bash
pip install -r requirements.txt
# OU instale manualmente:
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers coverage
```

### 3\. Configurar o Banco de Dados

Crie as tabelas iniciais e as tabelas de aplicação (`api_rest_transaction`):

```bash
# Cria os arquivos de migração (se houver mudanças no models.py)
python manage.py makemigrations api_rest

# Aplica todas as migrações ao banco de dados (cria o db.sqlite3)
python manage.py migrate
```

### 4\. Criar Usuário Administrador

Crie um usuário para login e testes:

```bash
python manage.py createsuperuser
```

### 5\. Executar o Servidor

Inicie o servidor de desenvolvimento. A API estará disponível em `http://127.0.0.1:8000/`.

```bash
python manage.py runserver
```

## 🔑 Autenticação (JSON Web Tokens - JWT)

Todas as rotas de transação são protegidas e exigem um token JWT válido no cabeçalho `Authorization`.

### 1\. Obter Token (Login)

Para iniciar uma sessão, envie as credenciais do usuário.

| Método | Endpoint |
| :--- | :--- |
| `POST` | `/api/token/` |

**Corpo da Requisição (JSON):**

```json
{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

**Resposta de Sucesso:** Retorna o `access` token (usado nas requisições) e o `refresh` token.

### 2\. Formato do Cabeçalho de Requisição

Use o token de acesso em todas as rotas protegidas:

```http
Authorization: Bearer <SEU_ACCESS_TOKEN>
Content-Type: application/json
```

## 🗺️ Endpoints da API

O prefixo base para as rotas de Transações é `http://127.0.0.1:8000/api_rest/`.

| Funcionalidade | Método | Endpoint | Descrição |
| :--- | :--- | :--- | :--- |
| **Listar Transações** | `GET` | `/transactions/` | Lista transações do usuário logado. Suporta Paginação e Filtros. |
| **Criar Transação** | `POST` | `/transactions/` | Cria uma nova Receita/Despesa. O campo `user` é preenchido automaticamente pelo token. |
| **Detalhe/CRUD** | `GET` | `/transactions/<id>/` | Retorna detalhes de uma transação específica (requer permissão do dono). |
| **Atualizar (Total)** | `PUT` | `/transactions/<id>/` | Atualiza **todos** os campos de uma transação. |
| **Atualizar (Parcial)** | `PATCH` | `/transactions/<id>/` | Atualiza **apenas** os campos fornecidos. |
| **Excluir Transação** | `DELETE`| `/transactions/<id>/` | Remove a transação do banco de dados (retorna 204 No Content). |
| **Resumo Financeiro**| `GET` | `/transactions/summary/`| Calcula e retorna o saldo líquido, total de receita e total de despesa do usuário logado. |

## 🧪 Testes e Cobertura de Código

Os testes unitários e de integração estão localizados em `api_rest/transactions/tests.py`.

### 1\. Rodar Testes

```bash
# Roda todos os testes da aplicação 'api_rest'
python manage.py test api_rest
```

### 2\. Verificar Cobertura

Para medir a porcentagem de código que seus testes estão executando:

```bash
# 1. Executa os testes e coleta dados (rastreia apenas a pasta api_rest)
python -m coverage run --source='api_rest' manage.py test

# 2. Gera o relatório visual (em uma pasta htmlcov/)
python -m coverage html

# 3. Abre o relatório no navegador para ver as linhas não cobertas.
# Abra o arquivo htmlcov/index.html
```