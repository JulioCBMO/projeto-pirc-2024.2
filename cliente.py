from dataclasses import dataclass, field
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum, auto
from typing import List, Dict
from marshmallow import Schema, fields, validate, ValidationError
from estrutura.py import ListaEncadeada,  FilaEncadeada


@dataclass
class Usuario:
    id: UUID = field(default_factory=uuid4)
    nome: str = ""
    email: str = ""
    senha: str = ""
    projetos: List[UUID] = field(default_factory=list)
    
    def adicionar_projeto(self, projeto_id: UUID):
        if projeto_id not in self.projetos:
            self.projetos.append(projeto_id)
    
    def remover_projeto(self, projeto_id: UUID):
        if projeto_id in self.projetos:
            self.projetos.remove(projeto_id)
    
    def validar_senha(self, senha_tentativa: str) -> bool:
        # Implementação simples - substituir por hash seguro
        return self.senha == senha_tentativa

class StatusTarefa(Enum):
    PENDENTE = auto()
    EM_PROGRESSO = auto()
    CONCLUIDA = auto()

class PrioridadeTarefa(Enum):
    BAIXA = auto()
    MEDIA = auto()
    ALTA = auto()

@dataclass
class Tarefa:
    id: UUID = field(default_factory=uuid4)
    titulo: str = ""
    descricao: str = ""
    status: StatusTarefa = StatusTarefa.PENDENTE
    prioridade: PrioridadeTarefa = PrioridadeTarefa.BAIXA
    data_criacao: datetime = field(default_factory=datetime.now)
    data_conclusao: datetime = None
    responsavel_id: UUID = None
    projeto_id: UUID = None

    def atualizar_status(self, novo_status: StatusTarefa):
        self.status = novo_status
        if novo_status == StatusTarefa.CONCLUIDA:
            self.data_conclusao = datetime.now()

    def atribuir_responsavel(self, responsavel_id: UUID):
        self.responsavel_id = responsavel_id

class StatusProjeto(Enum):
    PLANEJAMENTO = auto()
    EM_ANDAMENTO = auto()
    CONCLUIDO = auto()

@dataclass
class Projeto:
    id: UUID = field(default_factory=uuid4)
    nome: str = ""
    descricao: str = ""
    data_inicio: datetime = field(default_factory=datetime.now)
    data_conclusao: datetime = None
    status: StatusProjeto = StatusProjeto.PLANEJAMENTO
    membros: List[UUID] = field(default_factory=list)
    tarefas: List[UUID] = field(default_factory=list)

    def adicionar_membro(self, membro_id: UUID):
        if membro_id not in self.membros:
            self.membros.append(membro_id)

    def remover_membro(self, membro_id: UUID):
        if membro_id in self.membros:
            self.membros.remove(membro_id)

    def adicionar_tarefa(self, tarefa_id: UUID):
        if tarefa_id not in self.tarefas:
            self.tarefas.append(tarefa_id)

    def atualizar_status(self, novo_status: StatusProjeto):
        self.status = novo_status
        if novo_status == StatusProjeto.CONCLUIDO:
            self.data_conclusao = datetime.now()


class UsuarioSchema(Schema):
    nome = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    senha = fields.Str(required=True, validate=validate.Length(min=6))

class TarefaSchema(Schema):
    titulo = fields.Str(required=True, validate=validate.Length(min=2, max=200))
    descricao = fields.Str(validate=validate.Length(max=1000))
    status = fields.Str(validate=validate.OneOf(['PENDENTE', 'EM_PROGRESSO', 'CONCLUIDA']))
    prioridade = fields.Str(validate=validate.OneOf(['BAIXA', 'MEDIA', 'ALTA']))

class ProjetoSchema(Schema):
    nome = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    descricao = fields.Str(validate=validate.Length(max=500))
    status = fields.Str(validate=validate.OneOf(['PLANEJAMENTO', 'EM_ANDAMENTO', 'CONCLUIDO']))

def validar_usuario(dados):
    try:
        return UsuarioSchema().load(dados)
    except ValidationError as err:
        return {"erro": err.messages}

def validar_tarefa(dados):
    try:
        return TarefaSchema().load(dados)
    except ValidationError as err:
        return {"erro": err.messages}

def validar_projeto(dados):
    try:
        return ProjetoSchema().load(dados)
    except ValidationError as err:
        return {"erro": err.messages}

class RepositorioBase:
    def __init__(self):
        self._dados: Dict[UUID, object] = {}

    def adicionar(self, objeto):
        self._dados[objeto.id] = objeto
        return objeto.id

    def buscar_por_id(self, id: UUID):
        return self._dados.get(id)

    def listar(self) -> List:
        return list(self._dados.values())

    def atualizar(self, id: UUID, objeto):
        if id in self._dados:
            self._dados[id] = objeto
            return True
        return False

    def remover(self, id: UUID):
        if id in self._dados:
            del self._dados[id]
            return True
        return False

class RepositorioUsuario(RepositorioBase):
    def buscar_por_email(self, email: str):
        return next((usuario for usuario in self.listar() if usuario.email == email), None)

class RepositorioProjeto(RepositorioBase):
    def buscar_por_membro(self, membro_id: UUID):
        return [projeto for projeto in self.listar() if membro_id in projeto.membros]

class RepositorioTarefa(RepositorioBase):
    def buscar_por_projeto(self, projeto_id: UUID):
        return [tarefa for tarefa in self.listar() if tarefa.projeto_id == projeto_id]

    def buscar_por_responsavel(self, responsavel_id: UUID):
        return [tarefa for tarefa in self.listar() if tarefa.responsavel_id == responsavel_id]

class GerenciadorRepositorios:
    def __init__(self):
        self.usuarios = RepositorioUsuario()
        self.projetos = RepositorioProjeto()
        self.tarefas = RepositorioTarefa()
        
        # Estruturas para rastreamento
        self.historico_usuarios = ListaEncadeada()
        self.fila_tarefas = FilaEncadeada()

    def registrar_usuario(self, usuario: Usuario):
        self.usuarios.adicionar(usuario)
        self.historico_usuarios.adicionar(usuario)
        return usuario.id

    def criar_projeto(self, projeto: Projeto):
        return self.projetos.adicionar(projeto)

    def criar_tarefa(self, tarefa: Tarefa):
        tarefa_id = self.tarefas.adicionar(tarefa)
        self.fila_tarefas.enfileirar(tarefa)
        return tarefa_id

    def listar_tarefas_pendentes(self):
        return [tarefa for tarefa in self.fila_tarefas if tarefa.status != 'CONCLUIDA']