from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from app.Models.models import Aula
from sqlalchemy import func
from app.Database.database import get_session  
from typing import Dict, Any


router = APIRouter()

@router.post("/aulas", response_model=Aula)
def criar_aula(aula: Aula, session: Session = Depends(get_session)):
    session.add(aula)
    session.commit()
    session.refresh(aula)
    return aula

@router.get("/aulas", response_model=list[Aula])
def listar_aulas(session: Session = Depends(get_session)):
    aulas = session.exec(select(Aula)).all()
    return aulas

@router.put("/aulas/{id_aula}")
def atualizar_aula(id_aula: int, aula_atualizado: Aula, session: Session = Depends(get_session)):
    aula = session.get(Aula, id_aula)
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula não encontrada")
    update_data = aula_atualizado.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(aula, key, value)
    session.add(aula)
    session.commit()
    session.refresh(aula)
    return aula

@router.delete("/aulas/{id_aula}")
def excluir_aula(id_aula: int, session: Session = Depends(get_session)):
    aula = session.get(Aula, id_aula)
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula não encontrada")
    session.delete(aula)
    session.commit()
    return {"message": "Aula excluída com sucesso"}

@router.get("/aulas/quantidade")
def quantidade_aulas(session: Session = Depends(get_session)):
    try:
        total_aulas = session.exec(select(Aula)).all()
        return {"quantidade aulas:": len(total_aulas)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar as aulas: {str(e)}")

@router.get("/aulas/paginados", response_model=Dict[str, Any])
def paginacao_aulas(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session) ):
    total = session.execute(select(func.count(Aula.id_aula))).scalar_one_or_none() or 0
    
    result = session.execute(select(Aula).offset(offset).limit(limit))
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