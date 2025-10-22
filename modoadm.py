import json
import menu
import valida
from time import sleep
import os
def MostrarDados(email_admin):
    #Mostra os dados de todos os usuários
    valida.limpaTerminal()
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)

    print("\033[1;34m=== VISUALIZAÇÃO DE DADOS ===\033[m")
    print("1 - Ver clientes")
    print("2 - Ver entregadores")
    print("3 - Ver todos\n")

    opcao = input("Escolha uma opção: ").strip()
    while opcao not in ['1', '2', '3']:
        print("\033[31mOpção inválida.\033[m")
        opcao = input("Escolha uma opção válida (1-3): ").strip()
    sleep(2)
    print("\n\033[34m=== DADOS DOS USUÁRIOS ===\033[m")

    for email, info in dados.items():
        status = info.get("Status", "Cliente").capitalize()

        # Filtros conforme escolha do admin
        if opcao == '1' and status != "Cliente":
            continue
        elif opcao == '2' and status != "Entregador":
            continue

        print(f"\n📧 \033[1;33mEmail:\033[m {email}")
        print(f"👤 Nome: {info.get('Nome', 'Não informado')}")
        print(f"🧾 Status: {status}")
        print(f"🔐 Senha: {info.get("Senha", '---')}")

        # CLIENTE
        if status == "Cliente":
            compras = info.get("compras", [])
            if compras:
                print("\n🛒 Compras:")
                for i, compra in enumerate(compras, 1):
                    print(f"   {i}. Produto: {compra['Produto']}")
                    print(f"      Quantidade: {compra['Quantidade']}")
                    print(f"      Valor Unitário: {compra['Valor Unitário']}")
                    print(f"      Valor Total: {compra['Valor Total']}")
                    print(f"      Data: {compra['Data']}")
            else:
                print("\n🛒 Compras: Nenhuma registrada")

            bonificacoes = info.get("Bonificacoes", [])
            if bonificacoes:
                print("\n🎁 Bonificações:")
                for i, bonus in enumerate(bonificacoes, 1):
                    print(f"   {i}. {bonus}")
            else:
                print("\n🎁 Bonificações: Nenhuma registrada")

        # ENTREGADOR
        elif status == "Entregador":
            entregas = info.get("Entregas", [])
            if entregas:
                print("\n📦 Entregas:")
                for i, entrega in enumerate(entregas, 1):
                    print(f"   {i}. Produto: {entrega['Produto']}")
                    print(f"      Quantidade: {entrega['Quantidade']}")
                    print(f"      Data: {entrega['Data']}")
                    print(f"      Cliente: {entrega['Cliente']}")
            else:
                print("\n📦 Entregas: Nenhuma registrada")

            bonificacoes = info.get("Bonificacoes", [])
            if bonificacoes:
                print("\n💰 Histórico de Bonificações:")
                for i, bonus in enumerate(bonificacoes, 1):
                    print(f"   {i}. {bonus}")
            else:
                print("\n💰 Histórico de Bonificações: Nenhum registrado")

            if info.get("Ultimo Mês bonificado"):
                print(f"\n🗓️ Último mês bonificado: {info['Ultimo Mês bonificado']}")

            if "Saldo" in info:
                print(f"💳 Saldo: R$ {info['Saldo']}")

        print("\n" + "-" * 55)

    # Pergunta se quer atualizar algum dado
    deseja = input('\nDeseja atualizar algum desses dados? [s/n] ').strip().lower()
    while deseja not in ['s', 'n']:
        print('\033[1;31mA opção é inválida.\033[m')
        deseja = input('Digite apenas [s/n]: ').strip().lower()

    if deseja == 's':
        return AtualizarDados(email_admin)
    elif deseja == 'n':
        return menu.menu_admin(email_admin)
    
def AtualizarDados(admin_email):
    #Função criada para o administrador atualizar o dado de algum usuário
    valida.limpaTerminal()
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)

    print("\n\033[1;34m=== Atualizar Usuário ===\033[m")
    print("\033[34mDigite o email do cliente/entregador que deseja atualizar\033[m")
    email = valida.validaemail()  
    if email not in dados:
        print("\033[31mUsuário não encontrado!\033[m")
        sleep(2)
        return  

    info = dados[email]
    sleep(2)
    print("\n\033[1;34m=== Dados atuais do usuário ===\033[m")
    print(f"👤 Nome: {info.get('Nome', '---')}")
    print(f"🔐 Senha: {info.get('Senha', '---')}")
    print(f"🧾 Status: {info.get('Status', 'Cliente')}")

    # Mostrar compras, se houver
    compras = info.get("compras", [])
    if compras:
        print("\n🛒 Compras:")
        for i, compra in enumerate(compras, 1):
            print(f"   {i}. Produto: {compra['Produto']}")
            print(f"      Quantidade: {compra['Quantidade']}")
            print(f"      Valor Unitário: {compra['Valor Unitário']}")
            print(f"      Valor Total: {compra['Valor Total']}")
            print(f"      Data: {compra['Data']}")
    else:
        print("\n🛒 Compras: Nenhuma registrada")

    # Mostrar bonificações
    bonificacoes = info.get("Bonificacoes", [])
    if bonificacoes:
        print("\n🎁 Bonificações:")
        for i, bonus in enumerate(bonificacoes, 1):
            print(f"   {i}. {bonus}")
    else:
        print("\n🎁 Bonificações: Nenhuma registrada")

    print("\nO que deseja alterar?")
    print("1 - Nome")
    print("2 - Senha")
    print("3 - Email")
    print("4 - Cancelar")

    opcao = input("Escolha uma opção: ").strip()
    if opcao == '1':
        novo_nome = valida.validanome()
        dados[email]['Nome'] = novo_nome
    elif opcao == '2':
        nova_senha = valida.validasenha()
        dados[email]['Senha'] = nova_senha
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
    #Deletar conta de algum usuário
    valida.limpaTerminal()
    print("\033[1;34m=== Deletar Conta (Admin) ===\033[m")
    print("\033[34mDigite o email do cliente/entregador que deseja atualizar\033[m")
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
    #Adicionar o produto no estoque
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
    #Editar o estoque
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
    #Deletar o produto do banco de dados
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

def DeletarCompras(email):
    #Deletar alguma compra do usuário que foi registrada incorretamente
    valida.limpaTerminal()
    
    # Carrega os dados
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)

    # Filtra clientes com compras
    clientes_com_compras = [email for email, info in dados.items() if "compras" in info and info["compras"]]

    if not clientes_com_compras:
        print("Nenhum cliente possui compras registradas.")
        sleep(2)
        return

    # Lista clientes
    print("\033[1;34mClientes com compras:\033[m")
    for i, email_cliente in enumerate(clientes_com_compras, start=1):
        print(f"{i} - {dados[email_cliente]['Nome']} ({email_cliente})")

    # Seleciona cliente
    while True:
        escolha = input("Digite o número do cliente para deletar compras: ").strip()
        if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(clientes_com_compras):
            print("Opção inválida.")
            continue
        cliente_selecionado = clientes_com_compras[int(escolha)-1]
        break

    compras_cliente = dados[cliente_selecionado]["compras"]

    # Lista compras do cliente
    print(f"\nCompras de {dados[cliente_selecionado]['Nome']}:")
    for i, compra in enumerate(compras_cliente, start=1):
        print(f"{i} - {compra['Produto']} | Quantidade: {compra['Quantidade']} | Valor Total: {compra['Valor Total']} | Data: {compra['Data']}")

    # Seleciona compra
    while True:
        escolha_compra = input("Digite o número da compra que deseja deletar (ou '0' para cancelar): ").strip()
        if escolha_compra == '0':
            print("Operação cancelada.")
            sleep(1)
            return
        if not escolha_compra.isdigit() or int(escolha_compra) < 1 or int(escolha_compra) > len(compras_cliente):
            print("Opção inválida.")
            continue
        compra_deletar = int(escolha_compra)-1
        break

    # Deleta a compra
    del compras_cliente[compra_deletar]

    # Atualiza o JSON
    with open('nome.json', 'w', encoding='utf-8') as arq:
        json.dump(dados, arq, ensure_ascii=False, indent=4)

    print("Compra deletada com sucesso!")
    sleep(2)
    menu.menu_admin(email)
    
def DeletarEntregas(email_admin):
    #Deletar alguma entrega que foi registrada de forma incorreta
    valida.limpaTerminal()
    
    # Carrega os dados
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)

    # Filtra entregadores com entregas
    entregadores_com_entregas = [email for email, info in dados.items() if info.get("Status") == "Entregador" and info.get("Entregas")]

    if not entregadores_com_entregas:
        print("Nenhum entregador possui entregas registradas.")
        sleep(2)
        return

    # Lista entregadores
    print("\033[1;34mEntregadores com entregas:\033[m")
    for i, email_entregador in enumerate(entregadores_com_entregas, start=1):
        print(f"{i} - {dados[email_entregador]['Nome']} ({email_entregador})")

    # Seleciona entregador
    while True:
        escolha = input("Digite o número do entregador para deletar uma entrega: ").strip()
        if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(entregadores_com_entregas):
            print("Opção inválida.")
            continue
        entregador_selecionado = entregadores_com_entregas[int(escolha)-1]
        break

    entregas_entregador = dados[entregador_selecionado]["Entregas"]

    # Lista entregas do entregador
    print(f"\nEntregas de {dados[entregador_selecionado]['Nome']}:")
    for i, entrega in enumerate(entregas_entregador, start=1):
        cliente = entrega.get("Cliente", "Sem cliente")
        produto = entrega.get("Produto", "")
        qtd = entrega.get("Quantidade", "")
        data = entrega.get("Data", "")
        print(f"{i} - Produto: {produto} | Cliente: {cliente} | Quantidade: {qtd} | Data: {data}")

    # Seleciona entrega
    while True:
        escolha_entrega = input("Digite o número da entrega que deseja deletar (ou '0' para cancelar): ").strip()
        if escolha_entrega == '0':
            print("Operação cancelada.")
            sleep(1)
            return
        if not escolha_entrega.isdigit() or int(escolha_entrega) < 1 or int(escolha_entrega) > len(entregas_entregador):
            print("Opção inválida.")
            continue
        entrega_deletar = int(escolha_entrega)-1
        break

    # Deleta a entrega
    del entregas_entregador[entrega_deletar]

    # Atualiza o JSON
    with open('nome.json', 'w', encoding='utf-8') as arq:
        json.dump(dados, arq, ensure_ascii=False, indent=4)

    print("Entrega deletada com sucesso!")
    sleep(2)
    menu.menu_admin(email_admin)
