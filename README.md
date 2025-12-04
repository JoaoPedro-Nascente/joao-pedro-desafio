
-----

# 🌟 API RESTful para Controle de Despesas | Desafio IUPI

Este projeto implementa uma API RESTful completa para gerenciamento de transações financeiras (`Controle de Despesas`), conforme os requisitos do Desafio de Estágio Backend da IUPI. A API oferece o CRUD completo, um *endpoint* de resumo financeiro (`/summary/`) e segurança por **Autenticação JWT**.

## 🚀 Stack Tecnológica

| Componente | Tecnologia | Observações |
| :--- | :--- | :--- |
| **Backend** | Python 3.12.2, Django | Framework web principal. |
| **API** | Django REST Framework (DRF) | Usado para serialização e construção de *views* REST. |
| **Autenticação** | djangorestframework-simplejwt | Padrão JWT para acesso *stateless* e seguro. |
| **Banco de Dados**| SQLite (Padrão) | Leve e baseado em arquivo, ideal para desenvolvimento. |

-----

## ⚙️ Instalação e Configuração

Siga estes passos para configurar e rodar o projeto localmente.

### 1\. Clonar o Repositório

```bash
git clone https://github.com/JoaoPedro-Nascente/joao-pedro-desafio.git
cd joao-pedro-desafio
```

### 2\. Configurar o Ambiente Virtual

É altamente recomendado usar um ambiente virtual (`venv` ou `conda`) para isolar as dependências:

```bash
# Cria o ambiente virtual
python -m venv venv 

# Ativa o ambiente virtual (Linux/macOS)
source venv/bin/activate
# Ativa o ambiente virtual (Windows)
venv\Scripts\activate
```

### 3\. Instalar Dependências

Instale todos os pacotes necessários (Django, DRF, simplejwt, etc.):

```bash
pip install -r requirements.txt
```

### 4\. Preparar o Banco de Dados

Crie o arquivo do banco de dados e aplique as migrações:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5\. Criar Superusuário (Opcional, para Admin)

```bash
python manage.py createsuperuser
```

### 6\. Rodar o Projeto

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

A API estará acessível em `http://127.0.0.1:8000/`.

-----

## 🔒 Autenticação JWT e Rotas de Acesso

Todos os *endpoints* de transação são protegidos. O acesso deve ser feito usando um Access Token válido.

### 1\. Cadastro de Usuário (Público)

Cria uma nova conta de usuário para obter acesso à API.

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/register/` | Cria um novo usuário com `username` e `password`. |

**Corpo da Requisição:** `{"username": "...", "password": "..."}`

### 2\. Login e Obtenção de Tokens

Utilize este *endpoint* para obter o par de tokens.

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/token/` | Recebe `username` e `password`, retorna **`access`** e **`refresh`** tokens. |

### 3\. Uso do Access Token

Para acessar qualquer *endpoint* protegido, inclua o Access Token no cabeçalho `Authorization`:

```http
Authorization: Bearer <seu_access_token>
```

-----

## 🌐 Endpoints da API (Recurso: Transações)

A API gerencia o modelo `Transaction` com os campos `description`, `amount`, `type` (`income`/`expense`), e `date`.

| Rota | Método | Descrição | Autenticação |
| :--- | :--- | :--- | :--- |
| `/transactions/` | `POST` | Cria uma nova transação. **(Validações OBRIGATÓRIAS)** | Sim |
| `/transactions/` | `GET` | Lista transações. Permite filtros por `?description=` e `?type=`. Retorna apenas transações do usuário autenticado. | Sim |
| `/transactions/:id/` | `GET` | Obtém detalhes de uma transação específica. Retorna `404` se não existir. | Sim |
| `/transactions/:id/` | `PUT/PATCH` | Atualiza uma transação existente. | Sim |
| `/transactions/:id/` | `DELETE` | Exclui uma transação. Retorna `204 No Content`. | Sim |
| `/summary/` | `GET` | **Desafio de Lógica:** Calcula e retorna o saldo total (`total_income`, `total_expense`, `net_balance`). | Não |

## 💎 Requisitos Bônus Implementados

O projeto atende aos requisitos bônus de qualidade e funcionalidade:

1.  **Testes Automatizados:** Testes unitários foram escritos usando o framework de testes do Django para garantir a cobertura e o funcionamento dos *endpoints* CRUD e de validação.
2.  **Autenticação JWT:** A API está protegida via `djangorestframework-simplejwt`. Os *endpoints* de transação são restritos ao usuário autenticado e filtram os dados para exibir **apenas as transações pertencentes ao token**.
3.  **Padrões de Nomenclatura e Estrutura:** O código segue o padrão Python (`snake_case` para funções/variáveis e `PascalCase` para classes) e a estrutura do projeto garante a separação de responsabilidades (serializers, views, models).

-----

## 🧪 Como Rodar os Testes Automatizados

Para garantir que toda a lógica de negócio (CRUD, filtros, validações e o *endpoint* `/summary/`) está funcionando corretamente, execute o comando:

```bash
python manage.py test api_rest
```

Este comando irá criar um banco de dados de teste temporário, executar todos os testes da aplicação `api_rest` e reportar o resultado.