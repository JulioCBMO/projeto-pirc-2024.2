from dataclasses import dataclass, field
from typing import List
from uuid import uuid4, UUID

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