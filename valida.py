import os 
from datetime import datetime,timedelta
import smtplib
import random
from email.mime.text import MIMEText
class Validador:
    
    @staticmethod
    def enviar_codigo_entregador(email_entregador):
        codigo = str(random.randint(100000, 999999))

        msg = MIMEText(f"Seu código de confirmação de entrega é: {codigo}")
        msg['Subject'] = "Código de Confirmação de Entrega"
        msg['From'] = "SEU_EMAIL@gmail.com"
        msg['To'] = email_entregador

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login("SEU_EMAIL@gmail.com", "SENHA_DO_APP")
                smtp.send_message(msg)

            print("\033[32mCódigo enviado para o entregador!\033[m")
            return codigo

        except Exception as e:
            print("\033[31mErro ao enviar o email para o entregador:", e, "\033[m")
            return None

    
    @staticmethod 
    def enviar_codigo(email_destino):
        codigo = str(random.randint(100000, 999999))

        msg = MIMEText(f"Seu código de verificação de pagamento é: {codigo}")
        msg['Subject'] = "Confirmação de Pagamento"
        msg['From'] = "pedroholive12@gmail.com"
        msg['To'] = email_destino

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login("pedroholive12@gmail.com", "fsmy nbti zpxd cbez")
                smtp.send_message(msg)

            print("\033[32mCódigo de verificação enviado para seu e-mail!\033[m")
            return codigo

        except Exception as e:
            print("Erro ao enviar email:", e)
            return None
    
    @staticmethod
    def limpa_terminal(): 
        #Função para limpar o terminal 
        return os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def valida_nome():
        #Função para inserir o nome e validá-lo
        while True:
            nome = input('Nome: ').strip()
            if nome == '':
                print('\033[1;31mERRO! Entrada inválida\033[m')
                continue
            temp = ''.join(nome.split(' ')) #PedroHenrique
            if not temp.isalpha():
                print('\033[1;31mERRO! Digite um nome válido (somente letras)\033[m')
                continue
            
            return nome
        
    @staticmethod
    def valida_senha():
        #Função para inserir a senha e validá-la
        while True:
            senha = input("Senha: ").strip()
            if senha == '':
                print('\033[1;31mERRO! Entrada inválida\033[m')
                continue
            if len(senha) < 4 or len(senha) > 8:
                print('\033[1;31mERRO! A senha deve conter entre 4 e 8 caracteres.(Ph783)\033[m')
                continue
            if senha == senha.lower():
                print('\033[1;31mERRO! Sua senha deve conter pelo menos uma letra maiúscula.(Ph783)\033[m')
                continue
            tem_numero = False
            for char in senha:
                if char.isdigit():
                    tem_numero = True
                    break
            if not tem_numero:
                print('\033[1;31mERRO! Sua senha deve conter pelo menos um número.(Ph783)\033[m')
                continue
            return senha
    @staticmethod
    def verifica_email(email):
        return email.endswith('@gmail.com') or email.endswith('@ufrpe.br')

    @staticmethod
    def valida_email():
        #Insere o email e faz suas validações 
        while True:
            email = input("Digite o email: ").strip().lower()
            if email == '':
                print('\033[1;31mERRO! Entrada inválida\033[m')
                continue
            if not Validador.verifica_email(email):
                print('\033[1;31mERRO! O email deve conter "@gmail.com" ou "@ufrpe.br" (phdeoliveira14@gmail.com).\033[m')
                continue
            return email
    @staticmethod
    def valida_status():
            status = input('Você é Cliente ou Entregador? ').strip().capitalize()
            while status not in ['Cliente', 'Entregador']:
                print("\033[1;31mOpção inválida.\033[m")
                status = input("Digite apenas [Cliente/Entregador]: ").strip().capitalize()
            if status == 'Cliente':
                print('\033[1;36mCadastro concluído como cliente\033[m')
            else:
                print('Cadastro concluído como entregador')
                
            return status
        
    @staticmethod    
    def valida_produto():
        while True:
            nome = input('Nome do produto: ').strip()
            if nome == '':
                print('\033[31;mERRO! Entrada inválida\033[m')
                continue
            temp = ''.join(nome.split(' '))
            if not temp.isalpha():
                print('\033[31mERRO! Digite um nome válido (somente letras)\033[m')
                continue
        
            return nome
    @staticmethod        
    def valida_qtd():
        while True:
            quantia = input('Digite a quantia do produto que será adicionada: ').strip()
            if quantia == '':
                print('\033[31;mERRO! Entrada inválida\033[m')
                continue
            if not quantia.isdigit():
                print('Digite apenas números')
                continue
            if int(quantia) <= 0:
                print('Não pode colocar uma quantia menor ou igual a zero.')
                continue
            
            return quantia
    @staticmethod
    def valida_valor():
        while True:
            valor = input('Digite a valor do produto que será adicionado: R$').strip()
            if valor == '':
                print('\033[31;mERRO! Entrada inválida\033[m')
                continue
            if not valor.isdigit():
                print('Digite apenas números')
                continue
            valor_prod = float(valor)
            if valor_prod <= 0:
                print('Não pode colocar uma valor menor ou igual a zero.')
                continue
            
            return f'R${float(valor):.2f}'
    @staticmethod
    def valida_data():
        while True:
            data_atual = datetime.now().date()
            limite_minimo = data_atual + timedelta(days=365)  
            try:
                data = input('Digite a data de validade do produto (DD/MM/AAAA): ').strip()
                data_validade = datetime.strptime(data, '%d/%m/%Y').date()
            except ValueError:
                print('\033[31mFormato inválido! Use o formato DD/MM/AAAA.\033[m')
                continue
            if data_validade <= limite_minimo:
                print('\033[31mInválido! A data de validade deve ser de pelo menos 1 ano à frente da data atual.\033[m')
                continue

            return data_validade
