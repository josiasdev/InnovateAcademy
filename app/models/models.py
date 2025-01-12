from pydantic import BaseModel
from datetime import datetime, time
from typing import List
from models import Modulo, Instrutor, Aluno, Certificado

class Curso(BaseModel):
    id_curso: int
    nome_curso: str
    descricao: str
    horas_totais: time
    modulos: List[Modulo]
    instrutor: List[Instrutor]
    alunos: List[Aluno]


class Aluno(BaseModel):
    id_aluno: int
    nome_completo: str
    descricao: str
    cursos_inscritos: List[Curso]
    certificados: List[Certificado]
    contato_email: str    


class Aula(BaseModel):
    id_aula: int
    titulo: str
    descricao: str
    duracao: time  # Em minutos
    material: str  # Link para material da aula
    modulo: List[Modulo]  # Relacionada ao módulo ao qual pertence


class Avaliacao(BaseModel):
    id_avaliacao: int
    curso: List[Curso]
    aluno: List[Aluno]
    nota: float
    comentario: str
    data_avaliacao: datetime

class Categoria(BaseModel):
    id_categoria: int
    nome_categoria: str
    descricao: str
    cursos: List[Curso] 
    data_criacao: datetime
    numero_cursos: int

class Certificado(BaseModel):
    id_certificado: int
    aluno: List[Aluno]
    curso: List[Curso]
    data_emissao: datetime
    codigo_verificacao: str  # Código único para verificar autenticidade


class Inscricao(BaseModel):
    id_inscricao: int
    aluno: List[Aluno]
    curso: List[Curso]
    data_inscricao: datetime
    status: str  # Exemplo: "Ativo", "Concluído", "Cancelado"
    progresso: float  # Percentual de conclusão (0.0 a 100.0)

class Instrutor(BaseModel):
    id_instrutor: int
    nome_completo: str
    descricao: str
    especialidade: str
    curso_ministrado: List[Curso]
    contato_email: str

class Modulo(BaseModel):
    id_modulo: int
    nome_modulo: str
    descricao: str
    curso: List[Curso]
    aulas: List[Aula]

class Suporte(BaseModel):
    id_suporte: int
    aluno: List[Aluno]
    curso: List[Curso]
    data_abertura: datetime
    descricao_problema: str
    status: str  # Exemplo: "Aberto", "Em Andamento", "Resolvido"