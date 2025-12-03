# admin_usuarios.py
import json
from time import sleep
from valida import Validador

import os

class AdminUsuarios:
    ARQ_USUARIOS = 'nome.json'

    def __init__(self, email_admin):
        self.email_admin = email_admin

    def _carregar_dados(self):
        try:
            with open(self.ARQ_USUARIOS, 'r', encoding='utf-8') as arq:
                return json.load(arq)
        except json.JSONDecodeError:
            print(f"\n\033[31m⚠️ O arquivo '{self.ARQ_USUARIOS}' está inválido (JSON malformado ou vazio).\033[m")
            sleep(2)
            return {}
        except FileNotFoundError:
            print(f"\n\033[31m⚠️ O arquivo '{self.ARQ_USUARIOS}' não existe.\033[m")
            sleep(2)
            return {}

    def _salvar_dados(self, dados):
        with open(self.ARQ_USUARIOS, 'w', encoding='utf-8') as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)

    # ========== MOSTRAR DADOS ==========
    def mostrar_dados(self):
        dados = self._carregar_dados()
        if not dados:
            return(self.email_admin)
        
        Validador.limpa_terminal()
        print("\033[1;34m=== VISUALIZAÇÃO DE DADOS ===\033[m")
        print("1 - Ver clientes")
        print("2 - Ver entregadores")
        print("3 - Ver todos\n")

        opcao = input("Escolha uma opção: ").strip()
        while opcao not in ['1', '2', '3']:
            print("\033[31mOpção inválida.\033[m")
            opcao = input("Escolha uma opção válida (1-3): ").strip()
        sleep(2)
        
        Validador.limpa_terminal
        print("\n\033[34m=== DADOS DOS USUÁRIOS ===\033[m")

        for email, info in dados.items():
            status = info.get("Status", "Cliente").capitalize()

            if opcao == '1' and status != "Cliente":
                continue
            elif opcao == '2' and status != "Entregador":
                continue

            print(f"\n📧 \033[1;33mEmail:\033[m {email}")
            print(f"👤 Nome: {info.get('Nome', 'Não informado')}")
            print(f"🧾 Status: {status}")
            print(f"🔐 Senha: {info.get('Senha', '---')}")

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

        deseja = input('\nDeseja atualizar algum desses dados? [s/n] ').strip().lower()
        while deseja not in ['s', 'n']:
            print('\033[1;31mA opção é inválida.\033[m')
            deseja = input('Digite apenas [s/n]: ').strip().lower()

        if deseja == 's':
            return self.atualizar_dados()
        else:
            sleep(3)
            return 

    # ========== ATUALIZAR DADOS ==========
    def atualizar_dados(self):
        Validador.limpa_terminal()
        dados = self._carregar_dados()
        if not dados:
            return

        print("\n\033[1;34m=== Atualizar Usuário ===\033[m")
        print("\033[34mDigite o email do cliente/entregador que deseja atualizar\033[m")
        email = Validador.valida_email()
        if email not in dados:
            print("\033[31mUsuário não encontrado!\033[m")
            sleep(2)
            return

        info = dados[email]
        sleep(1)
        print("\n\033[1;34m=== Dados atuais do usuário ===\033[m")
        print(f"👤 Nome: {info.get('Nome', '---')}")
        print(f"🔐 Senha: {info.get('Senha', '---')}")
        print(f"🧾 Status: {info.get('Status', 'Cliente')}")

        compras = info.get("compras", [])
        if compras:
            print("\n🛒 Compras:")
            for i, compra in enumerate(compras, 1):
                print(f"   {i}. {compra['Produto']} | {compra['Quantidade']} | {compra['Valor Total']} | {compra['Data']}")
        else:
            print("\n🛒 Compras: Nenhuma registrada")

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
            novo_nome = Validador.valida_nome()
            dados[email]['Nome'] = novo_nome
        elif opcao == '2':
            nova_senha = Validador.valida_senha()
            dados[email]['Senha'] = nova_senha
        elif opcao == '3':
            novo_email = Validador.valida_email()
            dados[novo_email] = dados[email]
            del dados[email]
        elif opcao == '4':
            print("Alteração cancelada.")
            return
        else:
            print("Opção inválida.")
            return

        self._salvar_dados(dados)
        print("\033[32mDados atualizados com sucesso!\033[m")
        sleep(1)

    # ========== DELETAR CONTA (USUÁRIO) ==========
    def deletar_conta_admin(self):
        Validador.limpa_terminal()
        dados = self._carregar_dados()
        if not dados:
            return

        print("\033[1;34m=== Deletar Conta (Admin) ===\033[m")
        print("\033[34mDigite o email do cliente/entregador que deseja deletar\033[m")
        email = Validador.validaemail()

        if email not in dados:
            print("\033[31mUsuário não encontrado!\033[m")
            input("Pressione Enter para voltar...")
            return

        print(f"\nVocê está prestes a deletar a conta de: {email}")
        print(f"Nome: {dados[email].get('Nome')}")
        print(f"Senha: {dados[email].get('Senha')}")

        confirma = input("\nTem certeza que deseja deletar esta conta? [s/n]: ").strip().lower()
        while confirma not in ['s', 'n']:
            print("\033[1;31mOpção inválida.\033[m")
            confirma = input("Digite apenas [s/n]: ").strip().lower()

        if confirma == 's':
            del dados[email]
            self._salvar_dados(dados)
            print("\033[32mConta deletada com sucesso!\033[m")
            sleep(2)
        else:
            print("Exclusão cancelada.")
            sleep(1)

    # ========== DELETAR COMPRAS ==========
    def deletar_compras(self):
        Validador.limpa_terminal()
        dados = self._carregar_dados()
        if not dados:
            return

        clientes_com_compras = [email for email, info in dados.items() if "compras" in info and info["compras"]]

        if not clientes_com_compras:
            print("Nenhum cliente possui compras registradas.")
            sleep(2)
            return

        print("\033[1;34mClientes com compras:\033[m")
        for i, email_cliente in enumerate(clientes_com_compras, start=1):
            print(f"{i} - {dados[email_cliente]['Nome']} ({email_cliente})")

        while True:
            escolha = input("Digite o número do cliente para deletar compras: ").strip()
            if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(clientes_com_compras):
                print("Opção inválida.")
                continue
            cliente_selecionado = clientes_com_compras[int(escolha)-1]
            break

        compras_cliente = dados[cliente_selecionado]["compras"]

        print(f"\nCompras de {dados[cliente_selecionado]['Nome']}:")
        for i, compra in enumerate(compras_cliente, start=1):
            print(f"{i} - {compra['Produto']} | Quantidade: {compra['Quantidade']} | Valor Total: {compra['Valor Total']} | Data: {compra['Data']}")

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

        del compras_cliente[compra_deletar]
        self._salvar_dados(dados)

        print("Compra deletada com sucesso!")
        sleep(2)
        return 

    # ========== DELETAR ENTREGAS ==========
    def deletar_entregas(self):
        Validador.limpa_terminal()
        dados = self._carregar_dados()
        if not dados:
            return

        entregadores_com_entregas = [
            email for email, info in dados.items()
            if info.get("Status") == "Entregador" and info.get("Entregas")
        ]

        if not entregadores_com_entregas:
            print("Nenhum entregador possui entregas registradas.")
            sleep(2)
            return

        print("\033[1;34mEntregadores com entregas:\033[m")
        for i, email_entregador in enumerate(entregadores_com_entregas, start=1):
            print(f"{i} - {dados[email_entregador]['Nome']} ({email_entregador})")

        while True:
            escolha = input("Digite o número do entregador para deletar uma entrega: ").strip()
            if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(entregadores_com_entregas):
                print("Opção inválida.")
                continue
            entregador_selecionado = entregadores_com_entregas[int(escolha)-1]
            break

        entregas_entregador = dados[entregador_selecionado]["Entregas"]

        print(f"\nEntregas de {dados[entregador_selecionado]['Nome']}:")
        for i, entrega in enumerate(entregas_entregador, start=1):
            cliente = entrega.get("Cliente", "Sem cliente")
            produto = entrega.get("Produto", "")
            qtd = entrega.get("Quantidade", "")
            data = entrega.get("Data", "")
            print(f"{i} - Produto: {produto} | Cliente: {cliente} | Quantidade: {qtd} | Data: {data}")

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

        del entregas_entregador[entrega_deletar]
        self._salvar_dados(dados)

        print("Entrega deletada com sucesso!")
        sleep(2)
        return
