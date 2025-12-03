import json
from datetime import datetime
from valida import Validador
from time import sleep

class Entregador:
    ARQ_USUARIOS = 'nome.json'
    ARQ_PRODUTOS = 'produtos.json'

    def __init__(self, email):
        self.email = email  # email do entregador logado

    def _carregar_usuarios(self):
        with open(self.ARQ_USUARIOS, 'r', encoding='utf-8') as arq:
            return json.load(arq)

    def _salvar_usuarios(self, dados):
        with open(self.ARQ_USUARIOS, 'w', encoding='utf-8') as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)

    def _carregar_produtos(self):
        with open(self.ARQ_PRODUTOS, 'r', encoding='utf-8') as arq:
            return json.load(arq)

    def _salvar_produtos(self, produtos):
        with open(self.ARQ_PRODUTOS, 'w', encoding='utf-8') as arq:
            json.dump(produtos, arq, ensure_ascii=False, indent=4)

    # ===================== REGISTRAR ENTREGA =====================
    def registrar_entrega(self):
        """Permite ao entregador registrar uma nova entrega e atualizar ranking/estoque."""
        Validador.limpa_terminal()

        dados = self._carregar_usuarios()
        produtos = self._carregar_produtos()

        # Garante que o entregador tenha a lista "Entregas"
        if "Entregas" not in dados[self.email]:
            dados[self.email]["Entregas"] = []

        print('\033[1;34mRegistre suas entregas \033[m')
        print('\033[1;34mLista de produtos: \033[m')
        lista_produtos = list(produtos.keys())
        for i, p in enumerate(lista_produtos, start=1):
            print(f"{i} - {p}")

        # Escolha do produto
        while True:
            escolha = input('Digite o número do produto que você entregou: ').strip()
            if (not escolha.isdigit() or 
                int(escolha) < 1 or 
                int(escolha) > len(lista_produtos)):
                print('\033[1;31mOpção inválida. Digite um número da lista \033[m')
                continue
            produto_escolhido = lista_produtos[int(escolha) - 1]
            break

        # Quantidade entregue
        while True:
            qtd_entrega = input(
                f"Digite a quantidade entregue de '{produto_escolhido}':  "
            ).strip()
            if not qtd_entrega.isdigit() or int(qtd_entrega) <= 0:
                print("\033[1;31mDigite um número válido maior que zero.\033[m")
                continue
            qtd_entrega = int(qtd_entrega)
            break

        # E-mail do cliente (opcional)
        email_cliente = input(
            "Digite o email do cliente ou pressione Enter para entrega sem cliente: "
        ).strip().lower()

        desconto_estoque = False
        if email_cliente == "" or email_cliente not in dados:
            print("\033[33mEntrega sem cliente registrado ou cliente não encontrado.\033[m")
            desconto_estoque = True
        else:
            print("\033[32mEntrega registrada para cliente cadastrado. Estoque não será descontado.\033[m")
            
        codigo = Validador.enviar_codigo_entregador(self.email)
        if not codigo:
            print("\033[31mFalha ao enviar código. Cancelando entrega.\033[m")
            return

        print("\n\033[34mDigite o código recebido no seu email.\033[m")
        tent = 3
        while tent > 0:
            cod = input("Código: ").strip()
            if cod == codigo:
                print("\033[32mEntrega confirmada!\033[m")
                break
            tent -= 1
            print(f"\033[31mCódigo errado. Tentativas restantes: {tent}\033[m")

        print("\033[32mEntrega confirmada com sucesso!\033[m")
        
        if tent == 0:
            print("\033[31mFalha ao confirmar entrega.\033[m")
            return
        
        for compra in dados[email_cliente].get("compras", []):
            if compra["Produto"] == produto_escolhido and compra["Status"] == "Em trânsito":
                compra["Status"] = "Entregue"
                break
            
            
        # Registro da entrega
        entrega = {
            "Produto": produto_escolhido,
            "Quantidade": qtd_entrega,
            "Data": datetime.now().strftime("%d/%m/%Y"),
            "Cliente": email_cliente if email_cliente != "" else "Sem cliente",
            "Status" : "Entregue"
        }
        dados[self.email]["Entregas"].append(entrega)

        # Atualiza estoque se for entrega “sem cliente”
        if desconto_estoque:
            estoque_atual = int(produtos[produto_escolhido]["Quantidade no estoque"])
            novo_estoque = max(estoque_atual - qtd_entrega, 0)
            produtos[produto_escolhido]["Quantidade no estoque"] = str(novo_estoque)
            print(
                f"\033[32mEstoque atualizado! Nova quantidade de "
                f"'{produto_escolhido}': {produtos[produto_escolhido]['Quantidade no estoque']}\033[m"
            )

        # Salva alterações
        self._salvar_usuarios(dados)
        self._salvar_produtos(produtos)

        print("\033[32mEntrega registrada com sucesso!\033[m")
        input("Pressione Enter para voltar ao menu...")
        sleep(2)


    # ===================== HISTÓRICO DE ENTREGAS =====================
    def historico_entregas(self):
        """Mostra o histórico de entregas do entregador logado."""
        Validador.limpa_terminal()
        dados = self._carregar_usuarios()

        entregas = dados[self.email].get("Entregas", [])

        if not entregas:
            print("\033[33mNenhuma entrega registrada até o momento.\033[m")
        else:
            print(f"\033[1;34m=== Histórico de Entregas de {dados[self.email]['Nome']} ===\033[m")
            for i, entrega in enumerate(entregas, start=1):
                print(f"{i}º Entrega:")
                print(f"  Produto: {entrega['Produto']}")
                print(f"  Quantidade: {entrega['Quantidade']}")
                print(f"  Data: {entrega['Data']}")
                print(f"  Cliente: {entrega['Cliente']}")
                print("-" * 30)

        input("\nPressione Enter para voltar ao menu...")
        sleep(2)
        
    META_ENTREGAS_DIARIAS = 10 

    # ===================== METAS E PROGRESSO =====================
    def verificar_meta_diaria(self):
        """Calcula o progresso de entregas de hoje e compara com a meta."""
        Validador.limpa_terminal()

        dados = self._carregar_usuarios()
        entregas = dados[self.email].get("Entregas", [])
        
        # 1. Definir a data de hoje para comparação
        hoje = datetime.now().strftime("%d/%m/%Y")
        
        # 2. Contar as entregas feitas hoje
        entregas_hoje = 0
        for entrega in entregas:
            # Assumindo que a data está no formato "%d/%m/%Y"
            if entrega["Data"] == hoje: 
                entregas_hoje += entrega["Quantidade"] # Soma a quantidade de itens entregues
                
        # 3. Calcular o progresso e o status
        meta = self.META_ENTREGAS_DIARIAS
        restante = max(0, meta - entregas_hoje)

        print(f"\033[1;34m=== Meta Diária de Entregas ({hoje}) ===\033[m")
        print(f"  Metas a cumprir: {meta} entregas")
        print(f"  Entregas realizadas hoje: {entregas_hoje}")
        print("-" * 35)

        if entregas_hoje >= meta:
            print("\033[1;32m🎉 PARABÉNS! Meta diária atingida e superada!\033[m")
        else:
            print(f"\033[1;33m⚠️ Faltam {restante} entregas para atingir a meta de hoje.\033[m")

        input("\nPressione Enter para voltar ao menu...")
        sleep(2)
