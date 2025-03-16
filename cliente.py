import socket
import json

def encode_message(msg_type, payload):
    """
    Codifica a mensagem de acordo com o protocolo:
      TIPO|TAMANHO|PAYLOAD
    """
    payload_str = payload.strip()
    length = len(payload_str)
    return f"{msg_type}|{length}|{payload_str}".encode('utf-8')

def decode_message(message):
    """
    Decodifica a mensagem recebida e retorna (msg_type, payload)
    """
    try:
        decoded = message.decode('utf-8')
        parts = decoded.split('|', 2)
        if len(parts) != 3:
            return None, None
        msg_type, size_str, payload = parts
        if int(size_str) != len(payload):
            print("Aviso: Tamanho informado difere do real.")
        return msg_type, payload
    except Exception as e:
        print("Erro ao decodificar mensagem:", e)
        return None, None

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 12345))
    
    try:
        while True:
            print("\nEscolha uma opção:")
            print("1. Registrar")
            print("2. Login")
            print("3. Adicionar Tarefa")
            print("4. Listar Tarefas")
            print("5. Remover Tarefa")
            print("6. Deixar um Comentário")
            print("7. Sair")
            
            opc = input("Opção: ").strip()
            
            if opc == "1":
                # Registro de usuário com nome, email e senha
                nome = input("Digite seu nome: ").strip()
                email = input("Digite seu email: ").strip()
                senha = input("Digite sua senha: ").strip()
                data = json.dumps({"nome": nome, "email": email, "senha": senha})
                message = encode_message("REGISTER", data)
            elif opc == "2":
                # Login com email e senha (dados enviados via JSON)
                email = input("Digite seu email: ").strip()
                senha = input("Digite sua senha: ").strip()
                data = json.dumps({"email": email, "senha": senha})
                message = encode_message("LOGIN", data)

            elif opc == "3":
                # Adicionar tarefa
                task_desc = input("Digite o nome da tarefa: ").strip()
                message = encode_message("TASK", task_desc)
            elif opc == "4":
                # Listar tarefas e aguardar ação do usuário para voltar ao menu
                message = encode_message("LIST", "")
                client.send(message)
                response = client.recv(4096)
                resp_type, resp_payload = decode_message(response)
                print("\n=== Lista de Tarefas ===")
                print(resp_payload)
                input("\nPressione Enter para voltar ao menu...")
                continue  # Volta para o início do loop
            elif opc == "5":
                # Remover tarefa a partir do nome informado pelo usuário
                task_name = input("Digite o nome da tarefa a ser removida: ").strip()
                message = encode_message("REMOVE_TASK", task_name)
            elif opc == "6":
                # Deixar um comentário em uma tarefa
                task_name = input("Digite o nome da tarefa para comentar: ").strip()
                comment = input("Digite seu comentário: ").strip()
                data = json.dumps({"task_name": task_name, "comment": comment})
                message = encode_message("COMMENT", data)
            elif opc == "7":
                print("Encerrando o cliente...")
                break
            else:
                print("Opção inválida!")
                continue

            # Envia a mensagem para o servidor e aguarda a resposta
            client.send(message)
            response = client.recv(1024)
            resp_type, resp_payload = decode_message(response)
            print(f"Servidor:({resp_type}) Mensagem: {resp_payload}")

    except KeyboardInterrupt:
        print("Encerrando o cliente...")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
