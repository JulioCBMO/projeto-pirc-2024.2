import socket
import threading
from typing import List
from estruturas.lista_encadeada import ListaEncadeada
from protocolo import Protocolo, TipoMensagem

class ServidorSocket:
    def __init__(self, host='localhost', porta=5000):
        self.host = host
        self.porta = porta
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.porta))
        
        # Estruturas para gerenciar clientes e sessões
        self.clientes: ListaEncadeada = ListaEncadeada()
        self.sessoes_ativas: ListaEncadeada = ListaEncadeada()
    
    def iniciar(self):
        self.socket.listen(5)
        print(f"Servidor iniciado em {self.host}:{self.porta}")
        
        while True:
            cliente_socket, endereco = self.socket.accept()
            print(f"Conexão de {endereco}")
            
            # Criar thread para cada cliente
            thread_cliente = threading.Thread(
                target=self.tratar_cliente, 
                args=(cliente_socket,)
            )
            thread_cliente.start()
    
    def tratar_cliente(self, cliente_socket):
        try:
            while True:
                # Receber mensagem
                mensagem = cliente_socket.recv(1024)
                if not mensagem:
                    break
                
                # Processar mensagem
                dados = Protocolo.decodificar(mensagem)
                resposta = self.processar_mensagem(dados)
                
                # Enviar resposta
                cliente_socket.send(Protocolo.codificar(resposta['tipo'], resposta['dados']))
        
        except Exception as e:
            print(f"Erro no cliente: {e}")
        finally:
            cliente_socket.close()
    
    def processar_mensagem(self, mensagem):
        tipo = mensagem['tipo']
        dados = mensagem['dados']
        
        # Lógica de processamento de diferentes tipos de mensagens
        if tipo == TipoMensagem.AUTENTICACAO:
            return self.autenticar(dados)
        elif tipo == TipoMensagem.CRIAR_PROJETO:
            return self.criar_projeto(dados)
        # Outros tipos de mensagem...
        
        return {
            "tipo": TipoMensagem.ERRO,
            "dados": {"mensagem": "Tipo de mensagem não suportado"}
        }
    
    def autenticar(self, dados):
        # Lógica de autenticação
        pass
    
    def criar_projeto(self, dados):
        # Lógica de criação de projeto
        pass

if __name__ == "__main__":
    servidor = ServidorSocket()
    servidor.iniciar()