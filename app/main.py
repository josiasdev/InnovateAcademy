from fastapi import FastAPI
from app.Database.database import create_db_and_tables
from app.Routes import alunos, cursos, aulas, avaliacao, categoria, certificado, inscricao, instrutor, modulo,suporte

create_db_and_tables()
app = FastAPI()

app.include_router(alunos.router, tags=["Alunos"])
app.include_router(cursos.router, tags=["Cursos"])
app.include_router(aulas.router, tags=["Aulas"])
app.include_router(avaliacao.router, tags=["Avaliação"])
app.include_router(categoria.router, tags=["Categoria"])
app.include_router(certificado.router, tags=["Certificado"])
app.include_router(inscricao.router, tags=["Inscrição"])
app.include_router(instrutor.router, tags=["Instrutor"])
app.include_router(modulo.router, tags=["Modulo"])
app.include_router(suporte.router, tags=["Suporte"])