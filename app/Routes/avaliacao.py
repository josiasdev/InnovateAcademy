from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from app.Models.models import Avaliacao
from sqlalchemy import func
from app.Database.database import get_session  
from typing import Dict,Any


router = APIRouter()

@router.post("/avaliacao", response_model=Avaliacao)
def criar_avaliacao(avaliacao: Avaliacao, session: Session = Depends(get_session)):
    session.add(avaliacao)
    session.commit()
    session.refresh(avaliacao)
    return avaliacao

@router.get("/avaliacao", response_model=list[Avaliacao])
def listar_avaliacao(session: Session = Depends(get_session)):
    avaliacao = session.exec(select(Avaliacao)).all()
    return avaliacao

@router.put("/avaliacao/{id_avaliacao}")
def atualizar_avaliacao(id_avaliacao: int, avaliacao_atualizado: Avaliacao, session: Session = Depends(get_session)):
    avaliacao = session.get(Avaliacao, id_avaliacao)
    if avaliacao is None:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    update_data = avaliacao_atualizado.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(avaliacao, key, value)
    session.add(avaliacao)
    session.commit()
    session.refresh(avaliacao)
    return avaliacao

@router.delete("/avaliacao/{id_avaliacao}")
def excluir_avaliacao(id_avaliacao: int, session: Session = Depends(get_session)):
    avaliacao = session.get(Avaliacao, id_avaliacao)
    if avaliacao is None:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    session.delete(avaliacao)
    session.commit()
    return {"message": "Avaliação excluída com sucesso"}

@router.get("/avaliacao/quantidade")
def quantidade_avaliacao(session: Session = Depends(get_session)):
    try:
        total_avaliacao = session.exec(select(Avaliacao)).all()
        return {"quantidade avaliacao:": len(total_avaliacao)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar as avaliações: {str(e)}")

@router.get("/avaliacao/paginados", response_model=Dict[str, Any])
def paginacao_avaliacao(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session) ):
    total = session.execute(select(func.count(Avaliacao.id_avaliacao))).scalar_one_or_none() or 0
    
    result = session.execute(select(Avaliacao).offset(offset).limit(limit))
    avaliacoes = result.scalars().all() 
    
    current_page = (offset // limit) + 1
    total_pages = (total // limit) + 1
        
    return{
        "data": avaliacoes,
        "pagination": {
            "total": total,
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": limit
        }
    }