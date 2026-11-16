# API de Gerenciamento de Estoque com IA

Projeto Final da disciplina de **Machine Learning e Deep Learning**.

- **Docente:** Gabriel Torres de Almeida
- **Discentes:** Rafael Bispo Gomes / Pedro da Silva

---

## 📌 Descrição do Projeto

Sistema inteligente de controle de estoque desenvolvido com **FastAPI**, **SQLAlchemy** e **SQLite**, integrado a uma camada de análise em **Pandas** e Inteligência Artificial generativa local via **Ollama**.

A IA é capaz de ler um snapshot tabular em memória (DataFrame), realizar agregações por categoria e responder a comandos complexos em linguagem natural, além de produzir relatórios executivos automatizados para suporte à tomada de decisão.

---

## 🚀 Estrutura do Repositório

```text
├── database.py       # Configuração da conexão SQLite e sessão do banco
├── models.py         # Modelo SQLAlchemy da entidade Produto
├── schemas.py        # Schemas Pydantic para validação e serialização
├── crud.py           # Operações de banco (Create, Read, Update, Delete)
├── ai_service.py     # Integração analítica com Pandas e IA local via Ollama
├── main.py           # Servidor FastAPI e mapeamento de todos os endpoints
├── populate.py       # Script utilitário para popular dados de teste realistas
├── requirements.txt  # Dependências do projeto
└── README.md         # Documentação completa
```

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **API Framework:** FastAPI
- **Servidor ASGI:** Uvicorn
- **ORM / Banco de Dados:** SQLAlchemy / SQLite
- **Validação de Dados:** Pydantic v2
- **Processamento de Dados:** Pandas
- **Inteligência Artificial:** Ollama (`gemma3:12b` ou outro modelo local)

---

## 📦 Instalação e Execução

### 1. Clonar o repositório
```bash
git clone https://github.com/pedrodsilval/projeto-final-estoque-ia.git
cd projeto-final-estoque-ia
```

### 2. Criar e ativar o ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Popular o banco com dados de teste
```bash
python populate.py
```

### 5. Iniciar a API
```bash
uvicorn main:app --reload --port 8000
```

A documentação interativa estará disponível em:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 Endpoints da API

### Gestão de Produtos
| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/produtos/` | Lista todos os produtos cadastrados |
| `POST` | `/produtos/` | Cadastra um novo produto |
| `GET` | `/produtos/{id}` | Consulta detalhes de um produto específico |
| `PUT` | `/produtos/{id}` | Atualiza dados ou saldo do produto |
| `DELETE` | `/produtos/{id}` | Remove um produto do estoque |
| `GET` | `/produtos/alerta-baixo` | Retorna produtos com saldo em nível crítico (<= estoque mínimo) |

### Inteligência Artificial (Pandas + Ollama)
| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/ia/pergunta` | Envia pergunta em linguagem natural para análise de estoque |
| `GET` | `/ia/relatorio` | Gera um resumo executivo automatizado do estoque em Markdown |
