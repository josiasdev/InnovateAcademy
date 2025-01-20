from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from app.Models.models import Curso
from sqlalchemy import func
from app.Database.database import get_session  
from typing import Dict,Any


router = APIRouter()

@router.post("/cursos", response_model=Curso)
def criar_curso(curso: Curso, session: Session = Depends(get_session)):
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso

@router.get("/cursos", response_model=list[Curso])
def listar_cursos(session: Session = Depends(get_session)):
    cursos = session.exec(select(Curso)).all()
    return cursos

@router.put("/cursos/{id_curso}")
def atualizar_curso(id_curso: int, curso_atualizado: Curso, session: Session = Depends(get_session)):
    curso = session.get(Curso, id_curso)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    update_data = curso_atualizado.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(curso, key, value)
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso

@router.delete("/cursos/{id_curso}")
def excluir_curso(id_curso: int, session: Session = Depends(get_session)):
    curso = session.get(Curso, id_curso)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    session.delete(curso)
    session.commit()
    return {"message": "Curso excluído com sucesso"}

@router.get("/cursos/quantidade")
def quantidade_cursos(session: Session = Depends(get_session)):
    try:
        total_cursos = session.exec(select(Curso)).all()
        return {"quantidade cursos: ": len(total_cursos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar os cursos: {str(e)}")

@router.get("/cursos/paginados", response_model=Dict[str, Any])
def paginacao_cursos(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session) ):
    total = session.execute(select(func.count(Curso.id_curso))).scalar_one_or_none() or 0
    
    result = session.execute(select(Curso).offset(offset).limit(limit))
    cursos = result.scalars().all()

    current_page = (offset // limit) + 1
    total_pages = (total // limit) + 1
        
    return{
        "data": cursos,
        "pagination": {
            "total": total,
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": limit
        }
    }