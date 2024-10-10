**Sistema de Gerenciamento Acadêmico em Python**

  Este projeto foi desenvolvido em Python com o objetivo de criar um menu interativo para gerenciar informações de alunos e disciplinas em um banco de dados SQL e MongoDB (NoSQL). O sistema oferece diversas funcionalidades para cadastrar, consultar, alterar e remover alunos e disciplinas, além de permitir a vinculação entre eles. Ele também registra logs de operações no MongoDB, facilitando o acompanhamento das atividades realizadas.

**Funcionalidades**
O sistema possui um menu interativo que permite as seguintes operações:

Criar Tabela Aluno: Cria a tabela de alunos no banco de dados SQLite.
Criar Tabela Disciplina: Cria a tabela de disciplinas no banco de dados SQLite.
Criar Tabela Aluno_Disciplina: Cria a tabela que vincula alunos a disciplinas no banco de dados SQLite.
Cadastrar Aluno: Adiciona um novo aluno ao banco de dados.
Visualizar Aluno por ID: Exibe as informações de um aluno com base no seu ID.
Alterar Aluno por ID: Permite atualizar as informações de um aluno com base no seu ID.
Remover Aluno por ID: Exclui um aluno do banco de dados com base no seu ID.
Cadastrar Disciplina: Adiciona uma nova disciplina ao banco de dados.
Vincular Disciplina ao Aluno: Relaciona um aluno com uma disciplina.
Visualizar Disciplinas de um Aluno: Lista as disciplinas associadas a um aluno.
Verificar se o Aluno Cursa uma Disciplina: Confirma se o aluno está matriculado em uma disciplina específica.
Visualizar Logs: Exibe os logs registrados no MongoDB sobre as operações realizadas no sistema.
Encerrar: Finaliza o programa.

**Tecnologias Utilizadas**
Python 3.x: Linguagem de programação utilizada para o desenvolvimento do sistema.
SQLite: Banco de dados relacional utilizado para armazenar informações de alunos, disciplinas e suas associações.
MongoDB: Banco de dados NoSQL utilizado para armazenar os logs das operações do sistema.

**Bibliotecas**:
sqlite3: Usada para manipular o banco de dados SQLite.
pymongo: Utilizada para conectar e manipular o banco de dados MongoDB.
Estrutura de Pastas
appdb.db: Arquivo do banco de dados SQLite utilizado pelo sistema.
aluno.py: Contém a classe Aluno, que modela os alunos do sistema.
disciplina.py: Contém a classe Disciplina, que modela as disciplinas do sistema.
main.py: Arquivo principal que contém a lógica do menu interativo e as funções para manipular o banco de dados e logs.
