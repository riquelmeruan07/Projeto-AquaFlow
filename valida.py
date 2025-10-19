import os 
from datetime import datetime,timedelta
def limpaTerminal(): 
    #Função para limpar o terminal 
    return os.system('cls' if os.name == 'nt' else 'clear')

def validanome():
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
        else:
            return nome.strip(' ')
def validasenha():
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

def verificaemail(email):
    return email.endswith('@gmail.com') or email.endswith('@ufrpe.br')

def validaemail(): 
    while True:
        email = input("Digite o email: ").strip().lower()
        if email == '':
            print('\033[1;31mERRO! Entrada inválida\033[m')
            continue
        if not verificaemail(email):
            print('\033[1;31mERRO! O email deve conter "@gmail.com" ou "@ufrpe.br" (phdeoliveira14@gmail.com).\033[m')
            continue
        return email
    
def validastatus():
        status = input('Você é Cliente ou Entregador? ').strip().capitalize()
        while status not in ['Cliente', 'Entregador']:
            print("\033[1;31mOpção inválida.\033[m")
            status = input("Digite apenas [Cliente/Entregador]: ").strip().capitalize()
        if status == 'Cliente':
            print('\033[1;36mCadastro concluído como cliente\033[m')
        else:
            print('Cadastro concluído como entregador')
            
        return status
def validaproduto():
    while True:
        nome = input('Nome do produto: ').strip()
        if nome == '':
            print('\033[31;mERRO! Entrada inválida\033[m')
            continue
        temp = ''.join(nome.split(' '))
        if not temp.isalpha():
            print('\033[31mERRO! Digite um nome válido (somente letras)\033[m')
            continue
        else:
            return nome.strip(' ')
        
def validaqtd():
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
        else:
            return quantia

def ValidaValor():
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

def ValidaData():
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

        else:
            return data_validade
