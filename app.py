import sqlite3 as sqli
import pymongo
from datetime import date
from aluno import Aluno
from disciplina import Disciplina

## construir a função que vai retornar
## a conexão com um banco de dados
def conectar_banco():
    try:
        con = sqli.connect("appdb.db")
        return con
    except sqli.Error as e:
        print("Erro ao conectar -", e)

# define a conexao do banco noSql
def conectar_mongo():
    try:
        conexao = pymongo.MongoClient('localhost')
        db = conexao['LogDocuments']
        print("Conexao criada com sucesso!")
    except Exception as e:
        print("Erro ao conectar com a base!")

    try:
        colecao = db.Log

        print("Coleção criada com sucesso!")
        return colecao
    except Exception as e:
        print("Erro ao criar coleção!")

## variavel global que terá a conexão com o db
conexao = conectar_banco()
colecao = conectar_mongo()

def gravar_log(dados):
    Log = {
        "data_insercao" : date.today().strftime('%d-%m-%y'),
        "dados" : dados
    }

    try:
        log_id = colecao.insert_one(Log).inserted_id
        print("Log gravado com sucesso. ID:", log_id)
    except Exception as e:
        print("Erro ao gravar log!")

def visualizar_log():
    try:
        logs = colecao.find()
        if logs:
            for log in logs:
                print("[", log['data_insercao'],"]:", log['dados'])

            print("Busca Concluida!")
        else:
            print("Log não encontrado.")
    except Exception as e:
        print("Erro ao consultar log.")

##função para criar a tabela
def criar_tabela_aluno():
    sql = """
            create table if not exists aluno (
                id integer not null primary key autoincrement,
                nome text not null,
                ra text not null,
                email text not null
            )
          """
    try:
        cursor = conexao.cursor()
        cursor.execute(sql)
        conexao.commit()

        log = "criacao tabela aluno"
        gravar_log(log)

        print("Tabela Aluno criado com sucesso!")
    except sqli.Error as e:
        print("Erro ao executar!")
        conexao.rollback()

def criar_tabela_disciplina():
    sql = """
            create table if not exists disciplina (
                codigo integer not null primary key autoincrement,
                nome text not null,
                carga_horaria real not null,
                nome_professor text not null
            )
          """
    try:
        cursor = conexao.cursor()
        cursor.execute(sql)
        conexao.commit()

        log = "criacao tabela disciplina"
        gravar_log(log)

        print("Tabela Disciplina criado com sucesso!")
    except sqli.Error as e:
        print("Erro ao executar!")
        conexao.rollback()

def criar_tabela_aluno_disciplina():
    sql = """
            create table if not exists aluno_disciplina (
                id_al_dis integer not null primary key autoincrement,

                id_aluno integer not null,
                codigo_disciplina integer not null,

                foreign key(id_aluno) references aluno(id),
                foreign key(codigo_disciplina) references disciplina(codigo)
            )
          """
    try:
        cursor = conexao.cursor()
        cursor.execute(sql)
        conexao.commit()

        log = "criacao tabela aluno_disciplina"
        gravar_log(log)

        print("Tabela Aluno Disciplina criado com sucesso!")
    except sqli.Error as e:
        print("Erro ao executar!")
        conexao.rollback()

def cadastrar_disciplina():
    nome = input("Digite o nome da disciplina: ")
    carga_horaria = input("Digite a carga horaria da materia: ")
    nome_professor = input("Digite o nome do professor: ")

    disciplina = Disciplina(nome, carga_horaria, nome_professor)

    sql = f"""
               insert into disciplina(nome, carga_horaria, nome_professor) values
               ('{disciplina.nome}', '{disciplina.carga_horaria}', '{disciplina.nome_professor}')    
           """ 
    try:
        cursor = conexao.cursor()
        codigo = cursor.execute(sql).lastrowid
        conexao.commit()

        log = "cadastro disciplina"
        gravar_log(log)

        print("Disciplina cadastrada - Codigo:", codigo)
    except Exception as e:
        print("Erro ao cadastrar disciplina!")

def vincular_aluno_disciplina():
    id = int(input("Informe o ID do aluno: "))
    if id <= 0:
        print("Id incorreto! Digite novamente!")
        vincular_aluno_disciplina()
    else:
        try:
            aluno = get_aluno_por_id(id)
            if aluno:
                codigo = int(input("Informe o ID da disciplina: "))
                if codigo <= 0:
                    print("Id incorreto! Digite novamente!")
                    vincular_aluno_disciplina()
                else:
                    sql = f"""
                        insert into aluno_disciplina(id_aluno, codigo_disciplina) values
                        ('{id}', '{codigo}')
                        """
                    try: 
                        cursor = conexao.cursor()
                        id_cadastrado = cursor.execute(sql).lastrowid
                        conexao.commit()

                        log = "vinculado disciplina aluno"
                        gravar_log(log)

                        print("Disciplina vinculada. ID:", id_cadastrado)
                    except Exception as e:
                        print("Erro ao inserir disciplina disciplina!")
            else:
                print("Aluno nao encontrado")
        except Exception as e:
            print("Erro ao procurar aluno")

def visualizar_disciplinas():
    id = int(input("Digite o id do aluno: "))
    if id <= 0:
        print("Id incorreto! Digite novamente!")
        visualizar_disciplinas()
    else:
        sql = f"""
                select d.nome
                  from disciplina d
            inner join aluno_disciplina ad on d.codigo = ad.codigo_disciplina
                 where ad.id_aluno = {id}
                """
        try:
            cursor = conexao.cursor()
            cursor.execute(sql)
            disciplinas = cursor.fetchall()

            log = "visualizado disciplina"
            gravar_log(log)

            if disciplinas:
                print("Lista de Disciplinas do aluno: \n")
                for disciplina in disciplinas:
                    print(f"Nome da Disciplina: {disciplina[0]}")    
            else:
                print("Não há disciplinas cadastradas!!!")
        except sqli.Error as e:
            print("Erro ao executar!")

def verifica_aluno_disciplinas():
    id = int(input("Digite o id do aluno: "))
    if id <= 0:
        print("Id incorreto! Digite novamente!")
        verifica_aluno_disciplinas()
    else: 
        codigo = int(input("Digite o codigo da disciplina: "))
        if codigo <= 0:
            print("codigo incorreto! Digite novamente!")
            verifica_aluno_disciplinas()
        else:
            sql = f"""
                SELECT COUNT(*) 
                FROM aluno_disciplina 
                WHERE id_aluno = {id} 
                AND codigo_disciplina = {codigo}
            """
            try:
                cursor = conexao.cursor()
                cursor.execute(sql)
                disciplinas = cursor.fetchall()

                if disciplinas:
                    print("O aluno cursa a disciplina")
                    print("Disciplina: ", codigo)
                else:
                    print("O aluno não cursa a disciplina!!!")
            except sqli.Error as e:
                print("Erro ao executar!")

##funções auxiliares
def get_aluno_por_id(id):
    sql = f"""
        select * from aluno where id = {id}
    """
    cursor = conexao.cursor()
    resultado = cursor.execute(sql).fetchone()
    
    if resultado:
        return Aluno(resultado[1], resultado[2], resultado[3], resultado[0])
    return None

## criando uma função para inserir valores no banco:
def criar_aluno():
    nome = input("Digite o nome:")
    ra = input("Digite o ra:")
    email = input("Digite o email:")
    #objeto da classe aluno
    aluno = Aluno(nome, ra, email)

    sql = f"""
            insert into Aluno(nome, ra, email) values 
            ('{aluno.nome}', '{aluno.ra}', '{aluno.email}')
          """
    try:
        cursor = conexao.cursor()
        id = cursor.execute(sql).lastrowid
        conexao.commit()

        log = "inserido aluno"
        gravar_log(log)

        print("Aluno inserido - Id:", id)
    except sqli.Error as e:
        conexao.rollback()
        print("Erro ao cadastrar aluno")

def visualizar_aluno_por_id():
    id = int(input("Informe o ID para consultar o aluno:"))
    
    if id <= 0:
        print("Id incorreto! Digite novamente!")
        visualizar_aluno_por_id()
    else :
        try:
            aluno = get_aluno_por_id(id)
            if aluno:
                print(f"""Aluno encontrado! \n
                        Nome: {aluno.nome} \n
                        RA: {aluno.ra} \n
                        E-mail: {aluno.email}
                    """)
                log = "visualizacao aluno"
                gravar_log(log)
                
                print("Busca Concluida!")
            else:
                print("Aluno não existe!")
        except sqli.Error as e:
            print("Erro ao executar a query!")

def remover_aluno_por_id():
    id = int(input("Informe o ID para deletar o aluno:"))
    if id <= 0:
        print("Id incorreto, digite novamente")
        remover_aluno_por_id()
    else :
        try:
            aluno = get_aluno_por_id(id)
            if aluno:
                sql = f"""
                    delete from aluno where id = {id}
                """
                cursor = conexao.cursor()
                cursor.execute(sql)
                conexao.commit() #sempre utilizado quando ALTERAMOS o db

                log = "removido aluno"
                gravar_log(log)

                print("Aluno deletado com sucesso!")
            else:
                print("Aluno não existe!")
        except sqli.Error as e:
            print("Erro ao deletar o aluno!")
            conexao.rollback()

def alterar_aluno_por_id():
    id = int(input("Informe o ID do aluno para alterar:"))
    if id <= 0:
        print("Id incorreto! digite novamente!")
        alterar_aluno_por_id()
    else:
        aluno = get_aluno_por_id(id)
        if aluno:
            print(f"Nome: {aluno.nome}, RA: {aluno.ra}, Email: {aluno.email}")
            nome = input("Nome atualizado:")
            email = input("Email atualizado:")
            if nome == "" and email == "":
                print("Nada a ser alterado")
                return        
            
            sql = f"update aluno set"
            virgula = ""
            
            if nome != "" and email != "":
                virgula = ","
            if nome != "":
                sql += f" nome = '{nome}' {virgula}"
            if email != "":
                sql += f" email = '{email}'"

            sql += f" where id = {id}"
            try:
                cursor = conexao.cursor()
                cursor.execute(sql)
                conexao.commit()

                log = "alterado aluno"
                gravar_log(log)

                print("Aluno atualizado com sucesso!")
            except sqli.Error as e:
                print("Erro ao executar atualização!")
                conexao.rollback()

def main() :
    while True:
        print("""
                Digite 1 para criar a tabela Aluno:\n
                Digite 2 para criar a tabela Disciplina:\n
                Digite 3 para criar a tabela Aluno_Disciplina:\n
                Digite 4 para cadastrar um Aluno:\n
                Digite 5 para visualizar um Aluno por ID:\n
                Digite 6 para alterar um Aluno por ID:\n
                Digite 7 para deletar um Aluno por ID:\n
                Digite 8 para cadastrar uma Disciplina:\n
                Digite 9 para vincular disciplina ao aluno:\n
                Digite 10 para visualizar as disciplinas de um Aluno:\n
                Digite 11 para verificar se o aluno cursa a disciplina:\n
                Digite 12 para visualizar o log:\n
                Digite 13 para encerrar:
                """)

        opcao = int(input("Digite uma opção: "))

        if opcao == 1:
            criar_tabela_aluno()
        elif opcao == 2:
            criar_tabela_disciplina()
        elif opcao == 3:
            criar_tabela_aluno_disciplina()
        elif opcao == 4:
            criar_aluno()
        elif opcao == 5:
            visualizar_aluno_por_id()
        elif opcao == 6:
            alterar_aluno_por_id()
        elif opcao == 7:
            remover_aluno_por_id()
        elif opcao == 8:
            cadastrar_disciplina()
        elif opcao == 9:
            vincular_aluno_disciplina()
        elif opcao == 10:
            visualizar_disciplinas()
        elif opcao == 11:
            verifica_aluno_disciplinas()
        elif opcao == 12:
            visualizar_log()
        elif opcao == 13:
            return
       
main()
    




















