# API de Tarefas

API REST simples com FastAPI e banco SQLite, hospedada em uma VM na Azure.

## Tecnologias
- Python 3 + FastAPI
- SQLite
- Uvicorn

## Como rodar localmente
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

Documentação interativa: http://127.0.0.1:8000/docs

## Endpoints
| Método | Rota | Descrição |
|---|---|---|
| GET | / | Status da API |
| POST | /tarefas | Cria tarefa |
| GET | /tarefas | Lista tarefas |
| GET | /tarefas/{id} | Busca uma tarefa |
| PUT | /tarefas/{id} | Atualiza tarefa |
| DELETE | /tarefas/{id} | Remove tarefa |

## Autor
Seu Nome