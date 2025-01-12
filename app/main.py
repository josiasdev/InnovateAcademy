from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm import Session 
from models import Aluno
from database import get_db  

app = FastAPI()

@app.post("/alunos")
def criar_aluno(nome_completo: str, descricao: str, contato_email: str, db: Session = Depends(get_db)):
    aluno = Aluno(nome_completo=nome_completo, descricao=descricao, contato_email=contato_email)
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno

@app.get("/alunos")
def listar_alunos(db: Session = Depends(get_db)):
    alunos = db.query(Aluno).all()
    return alunos

@app.put("/alunos/{id_aluno}")
def atualizar_aluno(id_aluno:int, nome_completo: str = None, descricao: str = None, contato_email: str = None, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id_aluno == id_aluno).first()
    
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    if nome_completo:
        aluno.nome_completo = nome_completo
    if descricao:
        aluno.descricao = descricao
    if contato_email:
        aluno.contato_email = contato_email
    
    db.commit()
    db.refresh(aluno)
    
    return aluno

@app.delete("/alunos/{id_aluno}")
def excluir_aluno(id_aluno: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id_aluno == id_aluno).first()

    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado") 

    db.delete(aluno) 
    db.commit()  

    return {"message": "Aluno excluído com sucesso"}

@app.get("/eventos/quantidade")
def quantidade_alunos(db:Session = Depends(get_db)):
    try:
        total_alunos = db.query(Aluno).count()  # Conta o número de registros na tabela Aluno
        return {"quantidade": total_alunos}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao contar os alunos")