import json
import menu
import valida
from time import sleep
import os
def MostrarDados(email):
    valida.limpaTerminal()
    with open ('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)
        
    print("\033[34m=== DADOS DE TODOS OS USUÁRIOS ===\033[m")
    for email, info in dados.items():
        print(f'\n Email :{email}')
        for chave, valor in info.items():
            print(f"{chave}: {valor}")
    deseja = input('Deseja atualizar algum desses dados? [s/n] ').strip().lower()

    while deseja not in ['s', 'n']:
        print('\033[1;31mA opção é inválida.\033[m')
        deseja = input('Digite apenas [s/n]: ').strip().lower()

    if deseja == 's':
        return AtualizarDados(email)
    elif deseja == 'n':
        return menu.menu_admin(email)
    
def AtualizarDados(email):
    valida.limpaTerminal()
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)
    print("=== Atualizar Usuário ===")
    email = valida.validaemail()  
    if email not in dados:
        print("\033[31mUsuário não encontrado!\033[m")
        sleep(2)
        return  
    print("\nDados atuais do usuário:")
    for chave, valor in dados[email].items():
        print(f"{chave}: {valor}")

    print("\nO que deseja alterar?")
    print("1 - Nome")
    print("2 - Senha")
    print("3 - Email")
    print("4 - Cancelar")

    opcao = input("Escolha uma opção: ").strip()
    if opcao == '1':
        novo_nome = valida.validanome()
        dados[email]['nome'] = novo_nome
    elif opcao == '2':
        nova_senha = valida.validasenha()
        dados[email]['senha'] = nova_senha
    elif opcao == '3':
        novo_email = valida.validaemail()
        dados[novo_email] = dados[email]  
        del dados[email]                 
    elif opcao == '4':
        print("Alteração cancelada.")
        return
    else:
        print("Opção inválida.")
        return
    with open('nome.json', 'w', encoding='utf-8') as arq:
        json.dump(dados, arq, ensure_ascii=False, indent=4)
    print("\033[32mDados atualizados com sucesso!\033[m")
    
def DeletarContaAdmin(email):
    valida.limpaTerminal()
    print("=== Deletar Conta (Admin) ===")

    email = valida.validaemail()  # Admin informa qual conta deletar

    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)

    if email not in dados:
        print("\033[31mUsuário não encontrado!\033[m")
        input("Pressione Enter para voltar...")
        return

    print(f"\nVocê está prestes a deletar a conta de: {email}")
    print(f"Nome: {dados[email].get('Nome')}")
    print(f"Senha {dados[email].get('Senha')}")

    confirma = input("\nTem certeza que deseja deletar esta conta? [s/n]: ").strip().lower()
    while confirma not in ['s', 'n']:
        print("\033[1;31mOpção inválida.\033[m")
        confirma = input("Digite apenas [s/n]: ").strip().lower()

    if confirma == 's':
        del dados[email] 

        with open('nome.json', 'w', encoding='utf-8') as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)

        print("\033[32mConta deletada com sucesso!\033[m")
        sleep(2)
    else:
        print("Exclusão cancelada.")
        sleep(1)
        
def AddEstoque(email):
    valida.limpaTerminal()
    print('\033[1;34mAdicione um novo produto no estoque\033[m')
    produto = valida.validaproduto()
    quantia = str(valida.validaqtd())
    valor = valida.ValidaValor()
    data = valida.ValidaData()
    
    if os.path.exists('produtos.json'):
        with open('produtos.json', 'r', encoding='utf-8') as arq:
            dados = json.load(arq)
    else:
        dados = {}
    
    dados[produto] = {"Quantidade no estoque": quantia, "Valor do produto": valor, "Data de validade":  data.strftime('%d/%m/%Y')}
    with open ('produtos.json', 'w', encoding='utf-8') as arq:
        json.dump(dados, arq, ensure_ascii=False, indent=4)
    
    print(f'O produto {produto} foi adicionado com sucesso')
    print('Retornando para o menu de estoque...')
    sleep(2)
    menu.Estoque(email)

def EditaEstoque(email):
    valida.limpaTerminal()
    if os.path.exists('produtos.json'):
        with open('produtos.json', 'r', encoding='utf-8') as arq:
            dados = json.load(arq)
    else:
        print("O estoque está vazio.")
        input("Pressione Enter para voltar...")
        return
    print('\033[1;34mLista de produtos: \033[m')
    produtos = list(dados.keys())
    for i, p in enumerate(produtos, start=1):
        print(f"{i} - {p}")

    # Escolha segura do produto
    while True:
        escolha = input('Digite o número do produto que deseja editar: ').strip()
        if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(produtos):
            print("Opção inválida. Digite um número da lista.")
            continue
        produto = produtos[int(escolha)-1]
        break
    
    if produto not in dados:
        print("Produto não encontrado no estoque.")
        return

    # Mostra dados atuais
    print(f"\nDados atuais de {produto}:")
    for chave, valor in dados[produto].items():
        print(f"{chave}: {valor}")

    print("\nO que deseja alterar?")
    print("1 - Quantidade e data de validade")
    print("2 - Valor")
    print("3 - Cancelar")

    opcao = input("Escolha uma opção: ").strip()

    if opcao == '1':
        # Alterar quantidade
        print(f"A quantidade atual é {dados[produto]['Quantidade no estoque']}")
        nova_quantidade = valida.validaqtd()
        dados[produto]['Quantidade no estoque'] = str(nova_quantidade)

        # Pergunta nova data de validade
        nova_data = valida.ValidaData()
        dados[produto]['Data de validade'] = nova_data.strftime('%d/%m/%Y')

        print(f"Quantidade de '{produto}' atualizada para {nova_quantidade} e data de validade para {nova_data.strftime('%d/%m/%Y')}.")

    elif opcao == '2':
        # Alterar valor
        print(f"Valor atual: {dados[produto]['Valor do produto']}")
        novo_valor = valida.ValidaValor()
        dados[produto]['Valor do produto'] = novo_valor
        print(f"Valor de '{produto}' atualizado para {novo_valor}.")

    elif opcao == '3':
        print("Edição cancelada.")
        sleep(2)
        menu.Estoque(email)
        return

    else:
        print("Opção inválida.")
        return

    # Salva alterações
    with open('produtos.json', 'w', encoding='utf-8') as arq:
        json.dump(dados, arq, ensure_ascii=False, indent=4)

    print("\033[32mProduto atualizado com sucesso!\033[m")
    print("\033[32mRetornando para o menu de estoque...\033[m")
    sleep(2)
    menu.Estoque(email)
    
def DeletarProduto(email):
    valida.limpaTerminal()
    with open('produtos.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)
        
    print('\033[1;34mLista de produtos: \033[m')
    produtos = list(dados.keys())
    for i, p in enumerate(produtos, start=1):
        print(f"{i} - {p}")
        
    while True:
        escolha = input('Digite o número do produto que deseja excluir: ').strip()
        if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(produtos):
            print("Opção inválida. Digite um número da lista.")
            continue
        produto = produtos[int(escolha)-1]
        break
    
    confirma = input(f"Tem certeza que deseja excluir o produto '{produto}'? [s/n]: ").strip().lower()
    while confirma not in ['s', 'n']:
        print("\033[1;31mOpção inválida.\033[m")
        confirma = input("Digite apenas [s/n]: ").strip().lower()

    if confirma == 's':
        del dados[produto]
        with open('produtos.json', 'w', encoding='utf-8') as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)
        print(f"\033[32mProduto '{produto}' deletado com sucesso!\033[m")
    else:
        print("Exclusão cancelada.")

    sleep(2)
    menu.Estoque(email)