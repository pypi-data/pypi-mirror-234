import mysql.connector

global host_name
host_name = ""
global user_name
user_name = ""
global password_name
password_name = ""
global database_name
database_name = ""
global conexao
conexao = ""
global cursor
cursor = ""

def conectar(host_i:str,user_i:str,password_i:str,database_i:str):
    global host_name
    global user_name
    global password_name
    global database_name
    global cursor
    global conexao

    host_name = host_i
    user_name = user_i
    password_name = password_i
    database_name = database_i

    conexao = mysql.connector.connect(
    host= host_name,    
    user= user_name,
    password= password_name,
    database= database_name
    )
    cursor = conexao.cursor()


def criarConta(tabela:str,usuario:str,senha:str,nome_campo_usuario:str,nome_campo_senha:str):
    try:
        comando = f'INSERT INTO {tabela} ({nome_campo_usuario},{nome_campo_senha}) VALUES("{usuario}","{senha}")'
        cursor.execute(comando)
        conexao.commit()
        return True
    except:
        return False,"Algum Parâmetro Inválido Em 'criarConta()'"
    
def verificarConta(tabela:str,usuario:str,senha:str,numero_coluna_usuario:int,numero_coluna_senha:int):
    try:
        comando = f'SELECT * FROM {tabela}'
        cursor.execute(comando)
        varredura = cursor.fetchall()
        comando2 = f'SELECT MAX(id) as maxId FROM {tabela}'
        cursor.execute(comando2)
        num_id_str = cursor.fetchall()

        num_id_int = (num_id_str[0][0])

        for id in range(num_id_int):
            user_bd = (varredura[id][numero_coluna_usuario])
            senha_bd = (varredura[id][numero_coluna_senha])

            if (user_bd == f"{usuario}") and (senha_bd == f"{senha}"):
                return True
        else:
            return False

    except:
        return False, "Algo Deu Errado Em 'verificarConta()'"

def criarRegistro(tabela:str,registro:str,campo:str):
    try:
        comando = f'INSERT INTO {tabela} ({campo}) VALUES("{registro}")'
        cursor.execute(comando)
        conexao.commit()
        return True
    except:
        return False, "Algo Deu Errado Em 'criarRegistro()'"

def verificarRegistro(tabela:str,registro:str,numero_coluna:int):
    try:
        comando = f'SELECT * FROM {tabela}'
        cursor.execute(comando)
        varredura = cursor.fetchall()
        comando2 = f'SELECT MAX(id) as maxId FROM {tabela}'
        cursor.execute(comando2)
        num_id_str = cursor.fetchall()

        num_id_int = (num_id_str[0][0])

        for id in range(num_id_int):
            user_bd = (varredura[id][numero_coluna])

            if (user_bd == f"{registro}"):
                return True
        else:
            return False
    except:
        return False, "Algo Deu Errado Em 'verificarRegistro()'"
    
