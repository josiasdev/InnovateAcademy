from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base 
from sqlalchemy import Column, Integer, String, ForeignKey, Time, Float, DateTime

Base = declarative_base()

class Curso(Base):
    __tablename__ = 'cursos'
    id_curso = Column(Integer, primary_key=True, index=True)
    nome_curso = Column(String, nullable=False)
    descricao = Column(String)
    categoria_id = Column(Integer, ForeignKey('categorias.id_categoria'))
    horas_totais = Column(Time)
    modulos = relationship('Modulo', back_populates='curso')
    instrutor_id = Column(Integer, ForeignKey('instrutores.id_instrutor'))
    instrutor = relationship('Instrutor', back_populates='curso_ministrado')
    alunos = relationship('Inscricao', back_populates='curso')
    categoria = relationship("Categoria", back_populates="cursos")


class Aluno(Base):
    __tablename__ = 'alunos'
    id_aluno = Column(Integer, primary_key=True)
    nome_completo = Column(String, nullable=False)
    descricao = Column(String)
    contato_email = Column(String, nullable=False)
    cursos_inscritos = relationship('Inscricao', back_populates='aluno')
    certificados = relationship('Certificado', back_populates='aluno')

class Aula(Base):
    __tablename__ = 'aulas'
    id_aula = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String)
    duracao = Column(Time)  # Em minutos
    material = Column(String)  # Link para material da aula
    modulo_id = Column(Integer, ForeignKey('modulos.id_modulo'))
    modulo = relationship('Modulo', back_populates='aulas')


class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    id_avaliacao = Column(Integer, primary_key=True)
    curso_id = Column(Integer, ForeignKey('cursos.id_curso'))
    aluno_id = Column(Integer, ForeignKey('alunos.id_aluno'))
    nota = Column(Float, nullable=False)
    comentario = Column(String)
    data_avaliacao = Column(DateTime, default=datetime.utcnow)

    curso = relationship('Curso')
    aluno = relationship('Aluno')


class Categoria(Base):
    __tablename__ = 'categorias'
    id_categoria = Column(Integer, primary_key=True, index=True)
    nome_categoria = Column(String, nullable=False)
    descricao = Column(String)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    cursos = relationship('Curso', back_populates='categoria')


# 1:1 Certificado e Aluno
class Certificado(Base):
    __tablename__ = 'certificados'
    id_certificado = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id_aluno'))
    curso_id = Column(Integer, ForeignKey('cursos.id_curso'))
    data_emissao = Column(DateTime, default=datetime.utcnow)
    codigo_verificacao = Column(String, unique=True, nullable=False)

    aluno = relationship('Aluno', back_populates='certificados')
    curso = relationship('Curso')


# N:N Curso e Aluno atráves de Inscricao
class Inscricao(Base):
    __tablename__ = 'inscricoes'
    id_inscricao = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id_aluno'))
    curso_id = Column(Integer, ForeignKey('cursos.id_curso'))
    data_inscricao = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False)  # Exemplo: "Ativo", "Concluído", "Cancelado"
    progresso = Column(Float, default=0.0)  # Percentual de conclusão (0.0 a 100.0)

    aluno = relationship('Aluno', back_populates='cursos_inscritos')
    curso = relationship('Curso', back_populates='alunos')


class Instrutor(Base):
    __tablename__ = 'instrutores'
    id_instrutor = Column(Integer, primary_key=True)
    nome_completo = Column(String, nullable=False)
    descricao = Column(String)
    especialidade = Column(String)
    contato_email = Column(String, nullable=False)
    curso_ministrado = relationship('Curso', back_populates='instrutor')

# 1:N Curso e Modulo.
class Modulo(Base):
    __tablename__ = 'modulos'
    id_modulo = Column(Integer, primary_key=True)
    nome_modulo = Column(String, nullable=False)
    descricao = Column(String)
    curso_id = Column(Integer, ForeignKey('cursos.id_curso'))

    curso = relationship('Curso', back_populates='modulos')
    aulas = relationship('Aula', back_populates='modulo')


class Suporte(Base):
    __tablename__ = 'suportes'
    id_suporte = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id_aluno'))
    curso_id = Column(Integer, ForeignKey('cursos.id_curso'))
    data_abertura = Column(DateTime, default=datetime.utcnow)
    descricao_problema = Column(String)
    status = Column(String, nullable=False)  # Exemplo: "Aberto", "Em Andamento", "Resolvido"

    aluno = relationship('Aluno')
    curso = relationship('Curso')