from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from app.Models.models import Suporte
from sqlalchemy import func
from app.Database.database import get_session  
from typing import Dict,Any


router = APIRouter()

@router.post("/suportes", response_model=Suporte)
def criar_suporte(suporte: Suporte, session: Session = Depends(get_session)):
    session.add(suporte)
    session.commit()
    session.refresh(suporte)
    return suporte

@router.get("/suportes", response_model=list[Suporte])
def listar_suportes(session: Session = Depends(get_session)):
    suportes = session.exec(select(Suporte)).all()
    return suportes

@router.put("/suportes/{id_suporte}")
def atualizar_suporte(id_suporte: int, suporte_atualizado: Suporte, session: Session = Depends(get_session)):
    suporte = session.get(Suporte, id_suporte)
    if suporte is None:
        raise HTTPException(status_code=404, detail="Suporte não encontrado")
    update_data = suporte_atualizado.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(suporte, key, value)
    session.add(suporte)
    session.commit()
    session.refresh(suporte)
    return suporte

@router.delete("/suportes/{id_suporte}")
def excluir_suporte(id_suporte: int, session: Session = Depends(get_session)):
    suporte = session.get(Suporte, id_suporte)
    if suporte is None:
        raise HTTPException(status_code=404, detail="Suporte não encontrado")
    session.delete(suporte)
    session.commit()
    return {"message": "Suporte excluído com sucesso"}

@router.get("/suportes/quantidade")
def quantidade_suportes(session: Session = Depends(get_session)):
    try:
        total_suportes = session.exec(select(Suporte)).all()
        return {"quantidade suportes:": len(total_suportes)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar os suportes: {str(e)}")

@router.get("/suportes/paginados", response_model=Dict[str, Any])
def paginacao_suportes(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session) ):
    total = session.execute(select(func.count(Suporte.id_suporte))).scalar_one_or_none() or 0
    
    result = session.execute(select(Suporte).offset(offset).limit(limit))
    suportes = result.scalars().all() 

    current_page = (offset // limit) + 1
    total_pages = (total // limit) + 1
        
    return{
        "data": suportes,
        "pagination": {
            "total": total,
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": limit
        }
    }