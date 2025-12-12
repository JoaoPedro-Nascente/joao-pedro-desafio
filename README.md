-----

# 💰 API REST - Controle Financeiro Pessoal

Este projeto contém o backend da aplicação de Controle Financeiro Pessoal, desenvolvido utilizando **Django** e **Django REST Framework (DRF)**.

A API é responsável por gerenciar dados de transações (receitas e despesas), calcular o saldo em tempo real e fornecer segurança através de autenticação JWT.

-----

## 🛠️ Tecnologias e Dependências

| Categoria | Tecnologia | Uso Principal |
| :--- | :--- | :--- |
| **Framework** | Django 5.x | Core da Aplicação Web. |
| **API** | Django REST Framework | Criação das Views e Serializers. |
| **Segurança** | Simple JWT | Autenticação stateless via token. |
| **CORS** | `django-cors-headers` | Permite conexões do frontend (Live Server). |
| **Banco de Dados** | SQLite | Padrão de desenvolvimento. |
| **Qualidade** | `coverage.py` | Medição da cobertura de testes. |

-----

## ⚙️ Configuração e Instalação

Siga os passos abaixo para configurar o projeto localmente:

### 1\. Preparação do Ambiente

```bash
# Clone o projeto (se ainda não o fez)
git clone https://github.com/JoaoPedro-Nascente/joao-pedro-desafio
cd joao-pedro-desafio

# Crie e ative o ambiente virtual
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Linux/Mac
```

### 2\. Instalar Dependências

Instale os pacotes Python necessários:

```bash
pip install -r requirements.txt  # Assumindo que você tem este arquivo
# OU instale manualmente:
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers coverage
```

### 3\. Inicializar o Banco de Dados

Crie as tabelas necessárias:

```bash
python manage.py makemigrations api_rest
python manage.py migrate
```

### 4\. Criar Usuário Administrador

Crie um usuário para login e testes:

```bash
python manage.py createsuperuser
```

### 5\. Inicializar API

```bash
python manage.py runserver
```
-----

## 🔑 Autenticação (JSON Web Tokens - JWT)

A API utiliza tokens JWT. Todas as rotas de transação são protegidas e exigem o `Access Token` no cabeçalho.

### 1\. Registro de Usuário (Criação)

Crie um usuário para login (assumindo que você tem uma rota de registro customizada, ou usa o `createsuperuser`):

| Ação | Método | Endpoint (Exemplo) |
| :--- | :--- | :--- |
| **Criação de Usuário** | `POST` | `/auth/register/` |

**Corpo da Requisição (JSON):**

```json
{
    "username": "novo_usuario",
    "password": "senha_segura"
}
```

### 2\. Login e Obtenção de Token

Use o endpoint `auth/token/` para obter os tokens necessários.

| Ação | Método | Endpoint (Corrigido) |
| :--- | :--- | :--- |
| **Login** | `POST` | `/auth/token/` |

**Corpo da Requisição (JSON):**

```json
{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

**Resposta de Sucesso:**

```json
{
    "refresh": "...",
    "access": "..."
}
```

### 3\. Uso do Token (Acesso)

O `Access Token` é usado em todas as requisições protegidas (CRUD de Transações, Resumo, etc.):

**Cabeçalho Requerido:**

```http
Authorization: Bearer <SEU_ACCESS_TOKEN>
Content-Type: application/json
```

### 4\. Refresh do Token

Use o `Refresh Token` para obter um novo `Access Token` quando o atual expirar (o que ocorre após 50 minutos, por padrão).

| Ação | Método | Endpoint |
| :--- | :--- | :--- |
| **Refresh** | `POST` | `/api/token/refresh/` |

**Corpo da Requisição (JSON):**

```json
{
    "refresh": "<SEU_REFRESH_TOKEN_LONGO>"
}
```

-----

## 🗺️ Endpoints da API

O prefixo base para as rotas de Transações é `http://127.0.0.1:8000/api_rest/`.

| Funcionalidade | Método | Endpoint | Uso |
| :--- | :--- | :--- | :--- |
| **Lista / Criação** | `GET, POST` | `/transactions/` | Listar transações do usuário ou criar uma nova. |
| **Detalhe / CRUD** | `GET, PUT, PATCH, DELETE` | `/transactions/<id>/` | Gerenciar uma transação específica. |
| **Resumo** | `GET` | `/transactions/summary/`| Obter saldo líquido do usuário. |

-----

## 🧪 Testes e Cobertura de Código

### 1\. Rodar Testes

```bash
python manage.py test api_rest
```

### 2\. Medir Cobertura (`coverage.py`)

Para medir a porcentagem de código executada pelos testes:

```bash
python -m coverage run --source='api_rest' manage.py test
python -m coverage html
```