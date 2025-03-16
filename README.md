# projeto-pirc-2024.2
Esse Sistema de Gerenciamento de Tarefas é uma aplicação cliente/servidor implementada em Python. Utiliza a API de sockets para comunicação entre os módulos e define um protocolo de aplicação personalizado para a troca de mensagens. A aplicação atende funcionalidades como registro e login de usuários, criação, listagem, remoção de tarefas e adição de comentários às tarefas, utilizando também estruturas de dados customizada para gerenciamento de tarefas.

Autor:
Júlio César Batista de Medeiros Oliveira (20232370027)

Disciplinas
Estruturas de Dados 
Protocolos de Interconexão de Redes de Computadores (Prof. Leonidas Lima)

## Descrição do Projeto

O SGT foi desenvolvido para facilitar o controle e a organização de tarefas em projetos colaborativos. Com uma arquitetura cliente/servidor, o sistema permite que os usuários se registrem, façam login e gerenciem tarefas por meio de comandos enviados via sockets. O servidor processa mensagens utilizando um protocolo personalizado e armazena as tarefas em uma lista encadeada, permitindo também a remoção de tarefas e a associação de comentários.

## Pré-requisitos
Python 3.x

Bibliotecas padrão: socket, threading, json

## Arquitetura e Tecnologias

Linguagem: Python 3.x

Comunicação: Sockets (TCP)

Estruturas de Dados Personalizadas: Lista encadeada para gerenciamento de tarefas

Formato das Mensagens: Protocolo customizado utilizando o padrão "TIPO|TAMANHO|PAYLOAD"

Formato dos Dados: JSON (para payloads estruturados, como dados de registro, login, criação de tarefa e comentário)

## Protocolo da Aplicação

Todas as mensagens trocadas entre o cliente e o servidor seguem o formato: TIPO|TAMANHO|PAYLOAD
TIPO: Identifica o comando, por exemplo: REGISTER, LOGIN, TASK, LIST, REMOVE_TASK, COMMENT.

TAMANHO: Número de caracteres do campo PAYLOAD.

PAYLOAD: Conteúdo da mensagem. Dependendo do comando, pode ser enviado como texto simples (por exemplo, o nome de uma tarefa) ou em formato JSON (por exemplo, dados de registro, login ou comentário).

Exemplo: Para registrar um usuário, o cliente envia:

REGISTER|55|{"nome": "Fulano", "email": "fulano@mail.com", "senha": "123456"}


## Funcionalidades

Registro de Usuários: Permite o cadastro de novos usuários fornecendo nome, email e senha. Os dados são armazenados em um repositório interno protegido por locks para evitar condições de corrida.

Login: Autenticação de usuários utilizando email e senha. Apenas usuários registrados podem se autenticar e acessar as demais funcionalidades.

Adição de Tarefa: Permite criar tarefas passando um nome único. As tarefas são armazenadas em uma lista encadeada que suporta inserção sequencial.

Listagem de Tarefas: Mostra todas as tarefas cadastradas (incluindo eventuais comentários). Na interface do cliente, a lista permanece na tela até que o usuário pressione Enter para retornar ao menu.

Remoção de Tarefa: Permite remover uma tarefa informando o seu nome. Caso a tarefa não seja encontrada, é retornada uma mensagem de erro.

Comentário em Tarefa: Adiciona comentários a uma determinada tarefa, associados por meio do nome da tarefa.

## Instruções para Execução

Servidor
Abra o terminal e navegue até o diretório do projeto.

Inicie o servidor: 
python server.py
O servidor ficará aguardando conexões na porta 12345.

Cliente
Em outra janela de terminal, navegue até o diretório do projeto.

Inicie o cliente:
python client.py
Siga as instruções exibidas, utilizando as opções do menu.

## Observações Finais

Segurança: Este projeto está em uma fase inicial. ainda vou implementar persistência de dados e melhorias na segurança (como o hash de senhas e validação robusta).

Extensões Futuras: Possíveis melhorias incluem a implementação de uma interface gráfica, a adição de logs detalhados, a criação de testes unitários.
