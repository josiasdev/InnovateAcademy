from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from app.Models.models import Aluno
from sqlalchemy import func
from app.Database.database import get_session  
from typing import Dict, Any


router = APIRouter()

@router.post("/alunos", response_model=Aluno)
def criar_aluno(aluno: Aluno, session: Session = Depends(get_session)):
    session.add(aluno)
    session.commit()
    session.refresh(aluno)
    return aluno

@router.get("/alunos", response_model=list[Aluno])
def listar_alunos(session: Session = Depends(get_session)):
    alunos = session.exec(select(Aluno)).all()
    return alunos

@router.put("/alunos/{id_aluno}")
def atualizar_aluno(id_aluno: int, aluno_atualizado: Aluno, session: Session = Depends(get_session)):
    aluno = session.get(Aluno, id_aluno)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    update_data = aluno_atualizado.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(aluno, key, value)
    session.add(aluno)
    session.commit()
    session.refresh(aluno)
    return aluno

@router.delete("/alunos/{id_aluno}")
def excluir_aluno(id_aluno: int, session: Session = Depends(get_session)):
    aluno = session.get(Aluno, id_aluno)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    session.delete(aluno)
    session.commit()
    return {"message": "Aluno excluído com sucesso"}

@router.get("/eventos/quantidade")
def quantidade_alunos(session: Session = Depends(get_session)):
    try:
        total_alunos = session.exec(select(Aluno)).all()
        return {"quantidade alunos:": len(total_alunos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar os alunos: {str(e)}")

@router.get("/alunos/paginados", response_model=Dict[str, Any])
def paginacao_alunos(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session) ):
    total = session.execute(select(func.count(Aluno.id_aluno))).scalar_one_or_none() or 0
    
    result = session.execute(select(Aluno).offset(offset).limit(limit))
    alunos = result.scalars().all()  

    current_page = (offset // limit) + 1
    total_pages = (total // limit) + 1
        
    return{
        "data": alunos,
        "pagination": {
            "total": total,
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": limit
        }
    }