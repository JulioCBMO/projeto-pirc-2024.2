import socket
import threading
from typing import List
from estrutura import ListaEncadeada
from modelos import Protocolo, TipoMensagem

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
                    print("Conexão fechada pelo cliente")
                    break
                
                print(f"Mensagem recebida: {mensagem}")
                
                # Processar mensagem
                try:
                    dados = Protocolo.decodificar(mensagem)
                    print(f"Dados decodificados: {dados}")
                    
                    resposta = self.processar_mensagem(dados)
                    print(f"Resposta processada: {resposta}")
                    
                    if resposta is None:
                        print("ERRO: Resposta é None!")
                        resposta = {
                            "tipo": TipoMensagem.ERRO,
                            "dados": {"mensagem": "Erro interno do servidor"}
                        }
                    
                    # Enviar resposta
                    resposta_codificada = Protocolo.codificar(resposta['tipo'], resposta['dados'])
                    print(f"Enviando resposta: {resposta_codificada}")
                    cliente_socket.send(resposta_codificada)
                except Exception as e:
                    print(f"Erro no processamento: {e}")
                    import traceback
                    traceback.print_exc()
                    
                    # Enviar erro ao cliente
                    erro_msg = {
                        "tipo": TipoMensagem.ERRO,
                        "dados": {"mensagem": f"Erro no servidor: {str(e)}"}
                    }
                    cliente_socket.send(Protocolo.codificar(TipoMensagem.ERRO, erro_msg['dados']))
        
        except Exception as e:
            print(f"Erro na conexão com cliente: {e}")
            import traceback
            traceback.print_exc()
        finally:
            cliente_socket.close()
            print("Conexão com cliente encerrada")
    
    def processar_mensagem(self, mensagem):
        tipo = mensagem['tipo']
        dados = mensagem['dados']
        
        # Lógica de processamento de diferentes tipos de mensagens
        if tipo == TipoMensagem.AUTENTICACAO:
            return self.autenticar(dados)
        elif tipo == TipoMensagem.CRIAR_PROJETO:
            return self.criar_projeto(dados)
        
        # Outros tipos de mensagem
        return {
            "tipo": TipoMensagem.ERRO,
            "dados": {"mensagem": "Tipo de mensagem não suportado"}
        }
    
    def autenticar(self, dados):
        print(f"Processando autenticação: {dados}")
        return {
            "tipo": TipoMensagem.AUTENTICACAO,
            "dados": {"status": "sucesso", "mensagem": "Autenticação realizada com sucesso"}
        }
    
    def criar_projeto(self, dados):
        print(f"Processando criação de projeto: {dados}")
        return {
            "tipo": TipoMensagem.CRIAR_PROJETO,
            "dados": {"status": "sucesso", "mensagem": "Projeto criado com sucesso"}
        }

if __name__ == "__main__":
    servidor = ServidorSocket()
    servidor.iniciar()