from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from app.Models.models import Certificado
from sqlalchemy import func
from app.Database.database import get_session  
from typing import Dict,Any


router = APIRouter()

@router.post("/certificados", response_model=Certificado)
def criar_certificado(certificado: Certificado, session: Session = Depends(get_session)):
    session.add(certificado)
    session.commit()
    session.refresh(certificado)
    return certificado

@router.get("/certificados", response_model=list[Certificado])
def listar_certificados(session: Session = Depends(get_session)):
    certificados = session.exec(select(Certificado)).all()
    return certificados

@router.put("/certificados/{id_certificado}")
def atualizar_certificado(id_certificado: int, certificado_atualizado: Certificado, session: Session = Depends(get_session)):
    certificado = session.get(Certificado, id_certificado)
    if certificado is None:
        raise HTTPException(status_code=404, detail="Certificado não encontrado")
    update_data = certificado_atualizado.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(certificado, key, value)
    session.add(certificado)
    session.commit()
    session.refresh(certificado)
    return certificado

@router.delete("/certificados/{id_certificado}")
def excluir_certificado(id_certificado: int, session: Session = Depends(get_session)):
    certificado = session.get(Certificado, id_certificado)
    if certificado is None:
        raise HTTPException(status_code=404, detail="Certificado não encontrado")
    session.delete(certificado)
    session.commit()
    return {"message": "Certificado excluído com sucesso"}

@router.get("/certificados/quantidade")
def quantidade_certificados(session: Session = Depends(get_session)):
    try:
        total_certificados = session.exec(select(Certificado)).all()
        return {"quantidade certificados:": len(total_certificados)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar os certificados: {str(e)}")

@router.get("/certificados/paginados", response_model=Dict[str, Any])
def paginacao_certificados(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session) ):
    total = session.execute(select(func.count(Certificado.id_certificado))).scalar_one_or_none() or 0
    
    result = session.execute(select(Certificado).offset(offset).limit(limit))
    certificados = result.scalars().all() 

    current_page = (offset // limit) + 1
    total_pages = (total // limit) + 1
        
    return{
        "data": certificados,
        "pagination": {
            "total": total,
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": limit
        }
    }