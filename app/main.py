from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm import Session 
from models import Aluno, Curso, Inscricao  
from database import get_db  

app = FastAPI()