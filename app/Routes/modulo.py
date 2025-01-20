from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from app.Models.models import Modulo
from sqlalchemy import func
from app.Database.database import get_session  
from typing import Dict,Any


router = APIRouter()

@router.post("/modulos", response_model=Modulo)
def criar_modulo(modulo: Modulo, session: Session = Depends(get_session)):
    session.add(modulo)
    session.commit()
    session.refresh(modulo)
    return modulo

@router.get("/modulos", response_model=list[Modulo])
def listar_modulos(session: Session = Depends(get_session)):
    modulos = session.exec(select(Modulo)).all()
    return modulos

@router.put("/modulos/{id_modulo}")
def atualizar_modulo(id_modulo: int, modulo_atualizado: Modulo, session: Session = Depends(get_session)):
    modulo = session.get(Modulo, id_modulo)
    if modulo is None:
        raise HTTPException(status_code=404, detail="Modulo não encontrado")
    update_data = modulo_atualizado.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(modulo, key, value)
    session.add(modulo)
    session.commit()
    session.refresh(modulo)
    return modulo

@router.delete("/modulos/{id_modulo}")
def excluir_modulo(id_modulo: int, session: Session = Depends(get_session)):
    modulo = session.get(Modulo, id_modulo)
    if modulo is None:
        raise HTTPException(status_code=404, detail="Modulo não encontrado")
    session.delete(modulo)
    session.commit()
    return {"message": "Modulo excluído com sucesso"}

@router.get("/modulos/quantidade")
def quantidade_modulos(session: Session = Depends(get_session)):
    try:
        total_modulos = session.exec(select(Modulo)).all()
        return {"quantidade modulos:": len(total_modulos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar os modulos: {str(e)}")

@router.get("/modulos/paginados", response_model=Dict[str, Any])
def paginacao_modulos(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session) ):
    total = session.execute(select(func.count(Modulo.id_modulo))).scalar_one_or_none() or 0
    
    result = session.execute(select(Modulo).offset(offset).limit(limit))
    modulos = result.scalars().all() 

    current_page = (offset // limit) + 1
    total_pages = (total // limit) + 1
        
    return{
        "data": modulos,
        "pagination": {
            "total": total,
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": limit
        }
    }