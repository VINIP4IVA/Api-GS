import sqlite3
from contextlib import contextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_PATH = "tarefas.db"

app = FastAPI(title="API de Tarefas", version="1.0.0")


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                concluida INTEGER NOT NULL DEFAULT 0,
                criada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


init_db()


class TarefaIn(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    concluida: bool = False


@app.get("/")
def raiz():
    return {"status": "online", "mensagem": "API de Tarefas funcionando"}


@app.post("/tarefas", status_code=201)
def criar(t: TarefaIn):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO tarefas (titulo, descricao, concluida) VALUES (?, ?, ?)",
            (t.titulo, t.descricao, int(t.concluida)),
        )
        novo = conn.execute(
            "SELECT * FROM tarefas WHERE id = ?", (cur.lastrowid,)
        ).fetchone()
    return dict(novo)


@app.get("/tarefas")
def listar():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM tarefas ORDER BY id").fetchall()
    return [dict(r) for r in rows]


@app.get("/tarefas/{tarefa_id}")
def buscar(tarefa_id: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return dict(row)


@app.put("/tarefas/{tarefa_id}")
def atualizar(tarefa_id: int, t: TarefaIn):
    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE tarefas SET titulo=?, descricao=?, concluida=? WHERE id=?",
            (t.titulo, t.descricao, int(t.concluida), tarefa_id),
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        row = conn.execute(
            "SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)
        ).fetchone()
    return dict(row)


@app.delete("/tarefas/{tarefa_id}")
def deletar(tarefa_id: int):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"mensagem": "Tarefa removida"}