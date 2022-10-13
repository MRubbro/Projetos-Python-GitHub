import requests
import json
import sqlite3

conn = sqlite3.connect('./database.db') 

def escolha1():
    nome_player = input("Digite o nome do seu personagem: ")
    server = input("Digite agora o nome do servidor de seu personagem: ")  
   

    xivapi = requests.get (f"https://xivapi.com/character/search?name={nome_player}&server={server}")
    resultado = json.loads(xivapi.content)

    personagem_ID = resultado["Results"][0]["ID"]

    fc_info = requests.get(f"https://xivapi.com/character/{personagem_ID}?data=FC,FCM")
    fc_info_result = json.loads(fc_info.content)

    name_fc = fc_info_result["FreeCompany"]["Name"]
    members_fc = fc_info_result["FreeCompanyMembers"]

    print(name_fc)


    cursor = conn.cursor()
    for item in members_fc:
        cursor.execute(f" INSERT INTO Usuarios (lodestoneId, nome, nomeFc, servidor)  VALUES ('{str(item['ID'])}', '{item['Name']}', '{name_fc}','{item['Server']}' )") 
    
    conn.commit()
    conn.close()

    print('Dados inseridos com sucesso.')

#==============================================================
def main():
    print("Escolha as opções a seguir:")
    escolha = input("1 para adicionar, 2 para ver os detalhes de um personagem: ")
    if escolha == "1":
        escolha1()
        # vai para escolha 1 
    elif escolha == "2":
        escolha2()
        # vai para escolha 2
    else:
        print("esse não é um numero valido")    
            
    
def escolha2():


    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Usuarios;")
    for linha in cursor.fetchall():
        print(linha) 
    char_id = input("Escolha um jogador do banco de dados: ")
    cursor.execute(f"SELECT lodestoneId FROM Usuarios WHERE id = {char_id};")
    lodestone_id = cursor.fetchone()[0]
    print(lodestone_id)
    char = requests.get(f"https://xivapi.com/character/{lodestone_id}?data=FC,MIMO")
    char_info = json.loads(char.content)
    info_print = char_info["Character"]["Mounts"]["Minions"]
    
    print(f'{info_print["Name"], info_print["Server"], info_print["FreeCompanyName"]}')










main()
conn.close()