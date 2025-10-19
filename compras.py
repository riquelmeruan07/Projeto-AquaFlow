import menu
import json
from time import sleep
import valida
from datetime import datetime
def RegistraCompra(email):
    valida.limpaTerminal()
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)
    with open('produtos.json', 'r', encoding='utf-8') as arquivo:
        produtos = json.load(arquivo)

    print('\033[1;34mLista de produtos: \033[m')
    produto = list(produtos.keys())
    for i, p in enumerate(produto, start=1):
        print(f"{i} - {p}")
        
    while True:
        escolha = input('Digite o número do produto que você comprou: ').strip()
        if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(produto):
            print('Opção inválida. Digite um número da lista')
            continue
        produto_escolhido = produto[int(escolha)-1]
        break
    
    estoque_atual = int(produtos[produto_escolhido]["Quantidade no estoque"])
    
    while True:
        qtd = int(input(f'Digite a quantidade de {produto_escolhido} que você comprou: '))
        if qtd > estoque_atual:
            print('Quantidade maior do que a contém no estoque. Tente novamente')
        else:
            break
    valor_unit = produtos[produto_escolhido]["Valor do produto"].replace("R$", "").replace(",", ".").strip()
    valor_unit = float(valor_unit)

    valor_total = valor_unit * qtd

    # Registrar compra no usuário
    compra = {
        "Produto": produto_escolhido,
        "Quantidade": qtd,
        "Valor Unitário": produtos[produto_escolhido]["Valor do produto"],
        "Valor Total": f"R${valor_total:.2f}",
        "Data": datetime.now().strftime("%d/%m/%Y")
    }

    if "compras" not in dados[email]:
        dados[email]["compras"] = []

    dados[email]["compras"].append(compra)

    # Salvar no nome.json
    with open('nome.json', 'w', encoding='utf-8') as arq:
        json.dump(dados, arq, ensure_ascii=False, indent=4)

    # Atualizar estoque no produtos.json
    produtos[produto_escolhido]["Quantidade no estoque"] = str(estoque_atual - qtd)

    with open('produtos.json', 'w', encoding='utf-8') as arquivo:
        json.dump(produtos, arquivo, ensure_ascii=False, indent=4)

    print("\033[1;32mCompra registrada e estoque atualizado com sucesso! Retornando para o menu de compras...\033[m")
    sleep(2)
    menu.Compras(email)
    
def HistoricoCompras(email):
    valida.limpaTerminal()

    # Carrega os dados dos usuários
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)

    # Verifica se o cliente tem registro de compras
    if "compras" not in dados[email] or not dados[email]["compras"]:
        print("\033[33mVocê ainda não realizou nenhuma compra. Voltando para o Menu de Compras...\033[m")
        sleep(2)
        menu.Compras(email)

    print("\033[1;34m=== Histórico de Compras ===\033[m")

    # Listar todas as compras
    for i, compra in enumerate(dados[email]["compras"], start=1):
        print(f"\nCompra {i}:")
        print(f"Produto: {compra['Produto']}")
        print(f"Quantidade: {compra['Quantidade']}")
        print(f"Valor Unitário: {compra['Valor Unitário']}")
        print(f"Valor Total: {compra['Valor Total']}")
        print(f"Data: {compra['Data']}")

    input("\nPressione Enter para voltar ao Menu de Compras...")
    sleep(1)
    menu.Compras(email)
    
def RegistraEntrega(email):
    valida.limpaTerminal()
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)
    with open('produtos.json', 'r', encoding='utf-8') as arquivo:
        produtos = json.load(arquivo)
    
    if "entregas" not in dados[email]:
        dados[email]["Entregas"] = []
    
    print('\033[1;34mRegistre suas entregas \033[m')
    print('\033[1;34mLista de produtos: \033[m')
    produto = list(produtos.keys())
    for i, p in enumerate(produto, start=1):
        print(f"{i} - {p}")
        
    while True:
        escolha = input('Digite o número do produto que você comprou: ').strip()
        if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(produto):
            print('Opção inválida. Digite um número da lista')
            continue
        produto_escolhido = produto[int(escolha)-1]
        break
    while True:
        qtd_entrega = input(f"Digite a quantidade entregue de '{produto_escolhido}': ").strip()
        if not qtd_entrega.isdigit() or int(qtd_entrega) <= 0:
            print("Digite um número válido maior que zero.")
            continue
        qtd_entrega = int(qtd_entrega)
        break

    # Pergunta email do cliente (opcional)
    email_cliente = input("Digite o email do cliente ou pressione Enter para entrega sem cliente: ").strip().lower()

    desconto_estoque = False
    if email_cliente == "" or email_cliente not in dados:
        print("\033[33mEntrega sem cliente registrado ou cliente não encontrado.\033[m")
        desconto_estoque = True
    else:
        print("\033[32mEntrega registrada para cliente cadastrado. Estoque não será descontado.\033[m")

    # Registra a entrega no histórico do entregador
    from datetime import datetime
    entrega = {
        "Produto": produto_escolhido,
        "Quantidade": qtd_entrega,
        "Data": datetime.now().strftime("%d/%m/%Y"),
        "Cliente": email_cliente if email_cliente != "" else "Sem cliente"
    }
    dados[email]["Entregas"].append(entrega)

    # Desconta do estoque se necessário
    if desconto_estoque:
        estoque_atual = int(produtos[produto_escolhido]["Quantidade no estoque"])
        produtos[produto_escolhido]["Quantidade no estoque"] = str(max(estoque_atual - qtd_entrega, 0))
        print(f"\033[32mEstoque atualizado! Nova quantidade de '{produto_escolhido}': {produtos[produto_escolhido]['Quantidade no estoque']}\033[m")

    # Salva arquivos
    with open('nome.json', 'w', encoding='utf-8') as arq:
        json.dump(dados, arq, ensure_ascii=False, indent=4)
    with open('produtos.json', 'w', encoding='utf-8') as arq:
        json.dump(produtos, arq, ensure_ascii=False, indent=4)

    print("\033[32mEntrega registrada com sucesso!\033[m")
    input("Pressione Enter para voltar ao menu...")
    menu.MenuPrincipalEntregador(email)
def HistoricoEntregas(email):
    
    valida.limpaTerminal()

    # Carrega os dados
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)
    
    entregas = dados[email].get("Entregas", [])

    if not entregas:
        print("\033[33mNenhuma entrega registrada até o momento.\033[m")
    else:
        print(f"\033[1;34m=== Histórico de Entregas de {dados[email]['Nome']} ===\033[m")
        for i, entrega in enumerate(entregas, start=1):
            print(f"{i}º Entrega:")
            print(f"  Produto: {entrega['Produto']}")
            print(f"  Quantidade: {entrega['Quantidade']}")
            print(f"  Data: {entrega['Data']}")
            print(f"  Cliente: {entrega['Cliente']}")
            print("-" * 30)

    input("\nPressione Enter para voltar ao menu...")
    menu.MenuEntregador(email)