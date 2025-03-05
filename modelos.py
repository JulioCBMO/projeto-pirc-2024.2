import json
from enum import Enum, auto

class TipoMensagem(Enum):
    AUTENTICACAO = auto()
    CRIAR_PROJETO = auto()
    LISTAR_PROJETOS = auto()
    CRIAR_TAREFA = auto()
    LISTAR_TAREFAS = auto()
    ERRO = auto()

class Protocolo:
    @staticmethod
    def codificar(tipo: TipoMensagem, dados: dict) -> bytes:
        """
        Codifica uma mensagem para transmissão por socket
        
        Formato: 
        {
            "tipo": enum,
            "dados": objeto
        }
        """
        mensagem = {
            "tipo": tipo.name,
            "dados": dados
        }
        return json.dumps(mensagem).encode('utf-8')
    
    @staticmethod
    def decodificar(mensagem: bytes) -> dict:
        """
        Decodifica mensagem recebida por socket
        """
        try:
            mensagem_dict = json.loads(mensagem.decode('utf-8'))
            return {
                "tipo": TipoMensagem[mensagem_dict['tipo']],
                "dados": mensagem_dict['dados']
            }
        except (json.JSONDecodeError, KeyError) as e:
            return {
                "tipo": TipoMensagem.ERRO,
                "dados": {"erro": str(e)}
            }