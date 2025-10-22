import json
import valida
import menu

def RegistraEntrega(email):
    #Para o entregador poder registrar as entregas que ele fez e ir pro ranking
    valida.limpaTerminal()
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)
    with open('produtos.json', 'r', encoding='utf-8') as arquivo:
        produtos = json.load(arquivo)
    
    if "Entregas" not in dados[email]:
        dados[email]["Entregas"] = []
    
    print('\033[1;34mRegistre suas entregas \033[m')
    print('\033[1;34mLista de produtos: \033[m')
    produto = list(produtos.keys())
    for i, p in enumerate(produto, start=1):
        print(f"{i} - {p}")
        
    while True:
        escolha = input('Digite o número do produto que você comprou: ').strip()
        if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(produto):
            print('\033[1;31mOpção inválida. Digite um número da lista \033[m')
            continue
        produto_escolhido = produto[int(escolha)-1]
        break
    while True:
        qtd_entrega = input(f"Digite a quantidade entregue de '{produto_escolhido}':  ").strip()
        if not qtd_entrega.isdigit() or int(qtd_entrega) <= 0:
            print("\033[1;31mDigite um número válido maior que zero.\033[m")
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
    #Para o entregador conferir o histórico de entregas dele
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
    menu.MenuPrincipalEntregador(email)