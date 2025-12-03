import json
from valida import Validador


class GerenciadorBonificacoes:
    ARQ_USUARIOS = 'nome.json'

    def __init__(self, email):
        self.email = email

    def _carregar_usuarios(self):
        with open(self.ARQ_USUARIOS, 'r', encoding='utf-8') as arq:
            return json.load(arq)

    # -----------------------------
    # Histórico para ENTREGADOR
    # -----------------------------
    def mostrar_historico_entregador(self):
        """Mostra o histórico de bonificações do ENTREGADOR."""
        Validador.limpa_terminal()

        dados = self._carregar_usuarios()
        info = dados.get(self.email, {})

        print("\033[1;34m=== Histórico de Bonificações ===\033[m")
        bonificacoes = info.get("Bonificacoes", [])

        if bonificacoes:
            for b in bonificacoes:
                print(f"- {b}")
        else:
            print("Nenhuma bonificação registrada até o momento.")

        input("\nPressione Enter para voltar...")


    # -----------------------------
    # Histórico para CLIENTE
    # -----------------------------
    def mostrar_historico_cliente(self):
        """Mostra o histórico de bonificações do CLIENTE."""
        Validador.limpa_terminal()

        dados = self._carregar_usuarios()
        info = dados.get(self.email, {})

        nome = info.get("Nome", "Cliente")
        print("\n\033[1;34m=== Histórico de Bonificações ===\033[m")
        print(f"Cliente: {nome}\n")

        bonificacoes = info.get("Bonificacoes", [])

        if not bonificacoes:
            print("\033[33mNenhuma bonificação recebida até o momento.\033[m")
        else:
            for i, bonus in enumerate(bonificacoes, start=1):
                print(f"{i}º - {bonus}")

        input("\nPressione Enter para voltar...")
        
