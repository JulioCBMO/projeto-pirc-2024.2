# projeto-pirc-2024.2
Sistema de Gerenciamento de Tarefas

Autor:
Júlio César Batista de Medeiros Oliveira (20232370027)

Disciplinas
Estruturas de Dados 
Protocolos de Interconexão de Redes de Computadores (Prof. Leonidas Lima)

Descrição do Problema
Sistema de gerenciamento de tarefas, com comunicação via socket e protocolo próprio.

Pré-requisitos
Python 3.8+
Instalar dependências: pip install -r requirements.txt

Protocolo da Aplicação

- **TIPO**: Indica o tipo da mensagem, como `LOGIN`, `TASK`, `LIST` ou outros.
- **TAMANHO**: Número de caracteres do conteúdo do `<PAYLOAD>`.
- **PAYLOAD**: O conteúdo da mensagem, que será interpretado de acordo com o comando.

---

## Mensagens Disponíveis

### 1. LOGIN
- **Descrição**: Mensagem para autenticação do usuário.
- **Formato**:
- **Parâmetros**: `<NOME_USUARIO>`: Nome do usuário (string).
- **Resposta Esperada**:
- Sucesso:  
  ```
  ACK|<TAMANHO>|Usuário <nome> autenticado com sucesso.
  ```
- Erro:  
  ```
  NACK|<TAMANHO>|[Descrição do erro]
  ```

### 2. TASK
- **Descrição**: Mensagem para criação de uma nova tarefa.
- **Formato**:
- **Parâmetros**: `<DESCRICAO_TAREFA>`: Descrição detalhada da tarefa.
- **Resposta Esperada**:
- Sucesso:  
  ```
  ACK|<TAMANHO>|Tarefa adicionada com sucesso.
  ```
- Erro:
  ```
  NACK|<TAMANHO>|[Descrição do erro]
  ```

### 3. LIST
- **Descrição**: Mensagem para solicitar a listagem de todas as tarefas.
- **Formato**:
- **Parâmetros**: Nenhum.
- **Resposta Esperada**:
- Sucesso (tarefas existentes):
  ```
  ACK|<TAMANHO>|<TAREFA1>, <TAREFA2>, ...
  ```
- Caso não haja tarefas:
  ```
  ACK|<TAMANHO>|Nenhuma tarefa cadastrada.
  ```


## Regras Gerais

- O campo `<TAMANHO>` deve refletir exatamente o número de caracteres presentes em `<PAYLOAD>`.
- Em caso de erro de formatação, o servidor responderá com mensagem `NACK` informando o erro.
- Toda mensagem enviada deverá obedecer a este padrão para garantir a consistência e facilitar a comunicação entre os módulos.

## Execução:

Iniciar servidor: python servidor/servidor.py

Iniciar cliente: python cliente/cliente_gui.py
