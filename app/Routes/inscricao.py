from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from app.Models.models import Inscricao
from sqlalchemy import func
from app.Database.database import get_session  
from typing import Dict,Any


router = APIRouter()

@router.post("/inscricoes", response_model=Inscricao)
def criar_inscricao(inscricao: Inscricao, session: Session = Depends(get_session)):
    session.add(inscricao)
    session.commit()
    session.refresh(inscricao)
    return inscricao

@router.get("/inscricoes", response_model=list[Inscricao])
def listar_inscricoes(session: Session = Depends(get_session)):
    inscricoes = session.exec(select(Inscricao)).all()
    return inscricoes

@router.put("/inscricoes/{id_inscricao}")
def atualizar_inscricoes(id_inscricao: int, inscricao_atualizado: Inscricao, session: Session = Depends(get_session)):
    inscricao = session.get(Inscricao, id_inscricao)
    if inscricao is None:
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")
    update_data = inscricao_atualizado.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(inscricao, key, value)
    session.add(inscricao)
    session.commit()
    session.refresh(inscricao)
    return inscricao

@router.delete("/inscricoes/{id_inscricao}")
def excluir_inscricao(id_inscricao: int, session: Session = Depends(get_session)):
    inscricao = session.get(Inscricao, id_inscricao)
    if inscricao is None:
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")
    session.delete(inscricao)
    session.commit()
    return {"message": "Inscrição excluída com sucesso"}

@router.get("/inscricoes/quantidade")
def quantidade_inscricoes(session: Session = Depends(get_session)):
    try:
        total_inscricoes = session.exec(select(Inscricao)).all()
        return {"quantidade inscricoes:": len(total_inscricoes)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar as inscrições: {str(e)}")

@router.get("/inscricoes/paginados", response_model=Dict[str, Any])
def paginacao_inscricoes(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session) ):
    total = session.execute(select(func.count(Inscricao.id_inscricao))).scalar_one_or_none() or 0
    
    result = session.execute(select(Inscricao).offset(offset).limit(limit))
    inscricoes = result.scalars().all()

    current_page = (offset // limit) + 1
    total_pages = (total // limit) + 1
        
    return{
        "data": inscricoes,
        "pagination": {
            "total": total,
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": limit
        }
    }