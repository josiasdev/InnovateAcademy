from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from app.Models.models import Instrutor
from sqlalchemy import func
from app.Database.database import get_session  
from typing import Dict,Any


router = APIRouter()

@router.post("/instrutores", response_model=Instrutor)
def criar_instrutor(instrutor: Instrutor, session: Session = Depends(get_session)):
    session.add(instrutor)
    session.commit()
    session.refresh(instrutor)
    return instrutor

@router.get("/instrutores", response_model=list[Instrutor])
def listar_instrutores(session: Session = Depends(get_session)):
    instrutores = session.exec(select(Instrutor)).all()
    return instrutores

@router.put("/instrutores/{id_instrutor}")
def atualizar_instrutor(id_instrutor: int, instrutor_atualizado: Instrutor, session: Session = Depends(get_session)):
    instrutor = session.get(Instrutor, id_instrutor)
    if instrutor is None:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")
    update_data = instrutor_atualizado.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(instrutor, key, value)
    session.add(instrutor)
    session.commit()
    session.refresh(instrutor)
    return instrutor

@router.delete("/instrutores/{id_instrutor}")
def excluir_instrutor(id_instrutor: int, session: Session = Depends(get_session)):
    instrutor = session.get(Instrutor, id_instrutor)
    if instrutor is None:
        raise HTTPException(status_code=404, detail="Instrutor não encontrada")
    session.delete(instrutor)
    session.commit()
    return {"message": "Instrutor excluído com sucesso"}

@router.get("/instrutores/quantidade")
def quantidade_instrutores(session: Session = Depends(get_session)):
    try:
        total_instrutores = session.exec(select(Instrutor)).all()
        return {"quantidade instrutores:": len(total_instrutores)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar os instrutores: {str(e)}")

@router.get("/instrutores/paginados", response_model=Dict[str, Any])
def paginacao_instrutores(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session) ):
    total = session.execute(select(func.count(Instrutor.id_instrutor))).scalar_one_or_none() or 0
    
    result = session.execute(select(Instrutor).offset(offset).limit(limit))
    instrutores = result.scalars().all() 

    current_page = (offset // limit) + 1
    total_pages = (total // limit) + 1
        
    return{
        "data": instrutores,
        "pagination": {
            "total": total,
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": limit
        }
    }