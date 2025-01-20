from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from app.Models.models import Categoria
from sqlalchemy import func
from app.Database.database import get_session  
from typing import Dict, Any


router = APIRouter()

@router.post("/categoria", response_model=Categoria)
def criar_categoria(categoria: Categoria, session: Session = Depends(get_session)):
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

@router.get("/categoria", response_model=list[Categoria])
def listar_categoria(session: Session = Depends(get_session)):
    categoria = session.exec(select(Categoria)).all()
    return categoria

@router.put("/categoria/{id_categoria}")
def atualizar_categoria(id_categoria: int, categoria_atualizado: Categoria, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id_categoria)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    update_data = categoria_atualizado.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(categoria, key, value)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

@router.delete("/categoria/{id_categoria}")
def excluir_categoria(id_categoria: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id_categoria)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    session.delete(categoria)
    session.commit()
    return {"message": "Categoria excluída com sucesso"}

@router.get("/categoria/quantidade")
def quantidade_categoria(session: Session = Depends(get_session)):
    try:
        total_categoria = session.exec(select(Categoria)).all()
        return {"quantidade categoria:": len(total_categoria)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar as categorias: {str(e)}")

@router.get("/categoria/paginados", response_model=Dict[str, Any])
def paginacao_categoria(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session) ):
    total = session.execute(select(func.count(Categoria.id_categoria))).scalar_one_or_none() or 0
    
    result = session.execute(select(Categoria).offset(offset).limit(limit))
    categorias = result.scalars().all()  

    current_page = (offset // limit) + 1
    total_pages = (total // limit) + 1
        
    return{
        "data": categorias,
        "pagination": {
            "total": total,
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": limit
        }
    }