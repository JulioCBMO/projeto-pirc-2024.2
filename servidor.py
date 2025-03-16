import socket
import threading
import json

# ================================================================
# Estruturas para gestão de usuários
# ================================================================

# Dicionário global para armazenar usuários (chave: email)
users = {}
users_lock = threading.Lock()

class User:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

# ================================================================
# Estrutura de Dados Customizada: Lista Encadeada para Tarefas
# ================================================================

class Task:
    def __init__(self, nome, descricao=""):
        self.nome = nome              # Nome (único) da tarefa
        self.descricao = descricao    # Descrição adicional da tarefa
        self.comments = []            # Lista de comentários (strings)
        self.next = None              # Ponteiro para o próximo nó

class TaskLinkedList:
    def __init__(self):
        self.head = None

    def add_task(self, nome, descricao=""):
        new_task = Task(nome, descricao)
        if self.head is None:
            self.head = new_task
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_task

    def remove_task(self, nome):
        current = self.head
        prev = None
        while current:
            if current.nome == nome:
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                return True
            prev = current
            current = current.next
        return False

    def add_comment(self, nome, comment):
        current = self.head
        while current:
            if current.nome == nome:
                current.comments.append(comment)
                return True
            current = current.next
        return False

    def list_tasks(self):
        tasks = []
        current = self.head
        while current:
            comment_str = ", ".join(current.comments) if current.comments else "Sem comentários"
            tasks.append(f"{current.nome}: {current.descricao} [Comentários: {comment_str}]")
            current = current.next
        return tasks

# Instância global da lista de tarefas e lock para acesso concorrente
tasks_list = TaskLinkedList()
tasks_lock = threading.Lock()

# ================================================================
# Funções de Protocolo de Aplicação
# ================================================================

def encode_message(msg_type, payload):
    """
    Codifica a mensagem conforme o protocolo: "TIPO|TAMANHO|PAYLOAD"
    """
    payload_str = payload.strip()
    length = len(payload_str)
    return f"{msg_type}|{length}|{payload_str}".encode('utf-8')

def decode_message(message):
    """
    Decodifica a mensagem recebida e retorna uma tupla (msg_type, payload).
    Em caso de erro, retorna (None, None).
    """
    try:
        decoded = message.decode('utf-8')
        parts = decoded.split('|', 2)
        if len(parts) != 3:
            return None, None
        msg_type, size_str, payload = parts
        if int(size_str) != len(payload):
            print("Aviso: Tamanho informado não confere com o payload recebido.")
        return msg_type, payload
    except Exception as e:
        print(f"Erro ao decodificar mensagem: {e}")
        return None, None

# ================================================================
# Função que trata cada conexão de cliente
# ================================================================

def handle_client(client_socket, address):
    print(f"[NOVA CONEXÃO] {address} conectado.")
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                print(f"[DESCONEXÃO] {address} encerrou a conexão.")
                break

            msg_type, payload = decode_message(data)
            if msg_type is None:
                response = encode_message("NACK", "Formato inválido de mensagem.")
            else:
                print(f"[{address}] Tipo: {msg_type} | Payload: {payload}")
                # Processa a mensagem com base no tipo
                if msg_type == "REGISTER":
                    # Espera payload JSON: {"nome": ..., "email": ..., "senha": ...}
                    try:
                        user_data = json.loads(payload)
                        nome = user_data.get("nome")
                        email = user_data.get("email")
                        senha = user_data.get("senha")
                        if not (nome and email and senha):
                            response = encode_message("NACK", "Dados incompletos para registro.")
                        else:
                            with users_lock:
                                if email in users:
                                    response = encode_message("NACK", f"Usuário com email {email} já existe.")
                                else:
                                    novo_usuario = User(nome, email, senha)
                                    users[email] = novo_usuario
                                    response = encode_message("ACK", f"Usuário {nome} registrado com sucesso.")
                    except Exception as e:
                        response = encode_message("NACK", "Erro ao processar registro: " + str(e))
                
                elif msg_type == "LOGIN":
                    
                    # Espera payload JSON: {"email": ..., "senha": ...}
                    try:
                        email = user_data.get("email")
                        senha = user_data.get("senha")
                        if not (email and senha):
                            response = encode_message("NACK", "Dados incompletos para login.")

                        else:
                            with users_lock:
                                usuario = users.get(email)
                            if usuario is None:
                                response = encode_message("NACK", "Usuário não encontrado.")
                            else:
                                if usuario.senha == senha:
                                    response = encode_message("ACK", f"Usuário {usuario.nome} autenticado com sucesso.")
                                else:
                                    response = encode_message("NACK", "Senha incorreta.")

                    except Exception as e:
                        response = encode_message("NACK", "Erro ao processar login: " + str(e))
                
                elif msg_type == "TASK":
                    # Espera payload JSON: {"nome": ..., "descricao": ...}
                    try:
                        task_data = json.loads(payload)
                        nome_tarefa = task_data.get("nome")
                        descricao = task_data.get("descricao", "")
                        if not nome_tarefa:
                            response = encode_message("NACK", "Nome da tarefa obrigatório.")
                        else:
                            with tasks_lock:
                                tasks_list.add_task(nome_tarefa, descricao)
                            response = encode_message("ACK", f"Tarefa '{nome_tarefa}' adicionada com sucesso.")
                    except Exception as e:
                        # Se o JSON falhar, trata payload como nome da tarefa simples
                        task_name = payload
                        with tasks_lock:
                            tasks_list.add_task(task_name)
                        response = encode_message("ACK", f"Tarefa '{task_name}' adicionada com sucesso (JSON falhou).")
                
                elif msg_type == "LIST":
                    with tasks_lock:
                        all_tasks = tasks_list.list_tasks()
                    tasks_str = "\n".join(all_tasks) if all_tasks else "Nenhuma tarefa cadastrada."
                    response = encode_message("ACK", tasks_str)
                
                elif msg_type == "REMOVE_TASK":
                    # Espera payload: nome da tarefa (texto simples)
                    task_name = payload.strip()
                    with tasks_lock:
                        removed = tasks_list.remove_task(task_name)
                    if removed:
                        response = encode_message("ACK", f"Tarefa '{task_name}' removida com sucesso.")
                    else:
                        response = encode_message("NACK", f"Tarefa '{task_name}' não encontrada.")
                
                elif msg_type == "COMMENT":
                    # Espera payload JSON: {"task_name": ..., "comment": ...}
                    try:
                        comment_data = json.loads(payload)
                        task_name = comment_data.get("task_name")
                        comment = comment_data.get("comment")
                        if not task_name or not comment:
                            response = encode_message("NACK", "Dados incompletos para comentário.")
                        else:
                            with tasks_lock:
                                commented = tasks_list.add_comment(task_name, comment)
                            if commented:
                                response = encode_message("ACK", f"Comentário adicionado à tarefa '{task_name}'.")
                            else:
                                response = encode_message("NACK", f"Tarefa '{task_name}' não encontrada.")
                    except Exception as e:
                        response = encode_message("NACK", "Erro ao processar comentário: " + str(e))
                
                else:
                    response = encode_message("NACK", "Tipo de mensagem desconhecido.")

            client_socket.send(response)
    except ConnectionResetError:
        print(f"[ERRO] {address} desconectou inesperadamente.")
    finally:
        client_socket.close()

# ================================================================
# Função principal para iniciar o servidor
# ================================================================

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen(5)
    print("[SERVIDOR ATIVO] Aguardando conexões na porta 12345...")
    while True:
        client_socket, address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()
        print(f"[CONEXÕES ATIVAS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
