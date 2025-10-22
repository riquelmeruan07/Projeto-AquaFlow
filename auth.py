import valida
import os
from time import sleep
import json
import login

def cadastrar():
    #Cadastro do cliente/entregador
    valida.limpaTerminal()
    print('\033[1;34mCadastro do usuário\033[m')
    nome = valida.validanome()
    email = valida.validaemail()
    senha = valida.validasenha()
    status = valida.validastatus()
     
    if os.path.exists('nome.json'):
        #Verifica se o arquivo já existe
        with open('nome.json', 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            if email in dados:
                print("\033[1;34mEmail já cadastrado no sistema. Estamos encaminhando você para o login...\033[m")
                sleep(2)
                login.login()
    else:
        dados = {}  # começa vazio
    
    dados[email] = {"Nome": nome, "Senha": senha, "Status": status}
    
        # Salva os dados no JSON
    with open('nome.json', 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    sleep(2)
    login.login()
