# Projeto AquaFlow

**Repositório AquaFlow - PISI1 - Projetos Interdiciplinares de Sistemas da Informação 1**                                                             
Desenvolvedores: Riquelme Ruan e Pedro H. de Oliveira                                                           
Docente Responsável: Cleyton Magalhães                                                        

Descrição de projeto: 
O AquaFlow é um sistema integrado de gerenciamento desenvolvido especialmente para depósitos de água, com o objetivo de otimizar a logística operacional, aprimorar a gestão comercial e fortalecer o relacionamento com os clientes. A plataforma permite acompanhar, em tempo real, o controle de estoques, pedidos e entregas, garantindo maior eficiência na distribuição e redução de custos. Com isso, o AquaFlow não apenas organiza o dia a dia do negócio, mas também cria condições para crescimento sustentável, melhoria contínua e competitividade no mercado.

## REQUISITOS FUNCIONAIS
 
###  1ª RELEASE                                                                
RF001 - Menu inicial                                                                                                                  
RF002 -  Cadastro de Clientes                                                                                                                   
RF003 - Cadastro de Entregadores                                                                                                                       
RF004 - Login                                                                                
RF005 - Configurações                                                                                                                 
RF006 - Menu Compras                                                                       
RF007 - Menu Estoque                                                                                        
RF008 - Rankings                                                                                                                            
RF009 - Menu Principal   
RF010 - MODO ADM                         
RF011 - Bonificações 

###  2ª RELEASE
RF012 - Interface do Sistema                                                               
RF013 - Atualização Semanal dos Rankings                                                                                         
RF014 - Metas Diárias para os Entregadores                                                                            
RF015 - Aviso sobre Baixo Estoque                                                

## PRINCIPAIS FUNÇÕES DO CÓDIGO

### Autenticação de Usuário

- `MenuInicial()`: Menu inicial com opções de login e cadastro.
- `cadastrar()`: Cadastro de usuários com validação de e-mail, senha e nome.
- `login()`: Login do usuário

### Configurações da conta

- `configuracoes(email_logado)`: Acessa as configurações da conta do usuário.
- `MostraDados(email)`: Exibe informações da conta e pergunta se ele deseja mudar algo.
- `AtualizarDados(email_atual)`: Atualiza os dados do usuário
- `DeletarConta(email)`: Exclui a conta após a confirmação da senha do usuário

### Compras e Entregas
- `RegistraCompra(email)`: Para o cliente poder registrar a compra que foi realizada
- `HistoricoCompras(email)`: Para o cliente poder conferir suas últimas compras
- `RegistraEntrega(email)`: Para os entregadores poderem registrar suas entregas
- `RegistraEntrega(email)`: Para os entregadores poderem conferir suas últimas entregas

### Rankings e Histórico de Bonificações

- `Rankings(email_usuario)`: Ranking com os clientes que mais compraram no mês
- `RankingEntregadores(email)`: Ranking com os entregadores que mais fizeram entregas
- `HistoricoBonificacoesEntregador(email)`: Histórico de bonificações que os entregadores receberam ao longo dos meses
- `HistoricoBonificacoesCliente(email)`: Histórico de bonificações que os clientes receberam ao longo dos meses

 ### Modo ADM

 - `MostrarDados(email_admin)`: Mostra os dados de todos clientes e entregadores
 - `AtualizarDados(admin_email)`: Pode atualizar os dados de todos os clientes e entregadores
 - `DeletarContaAdmin(email)`: Pode deletar a conta de qualquer usuário
 - `AddEstoque(email)`: Adicionar produto no estoque
 - `EditaEstoque`: Edita algum produto do estoque
 - `DeletarProduto`: Deletar algum produto
 - `DeletarCompra(email)`: Deleta alguma compra que foi adicionada incorretamente
 - `DeletarEntrega(email)`: Deleta alguma entrega

### Validações e Utilidades

- `limpaTerminal()`: Limpa a tela do terminal conforme o sistema operacional.
- `validaemail()`: Verifica se o e-mail possui domínio permitido (`@gmail.com`, `@ufrpe.br`).
- `validasenha()`: Valida senhas com base em regras de segurança (mín. 1 número, 1 maiúscula, e entre 4 a 8 caracteres).
- `validastatus()`: Verifica se o usuário é um Cliente ou Entregador.
- `validaproduto()`: Verifica se o o produto foii inserido corretamente
- `validaqtd()`: Valida a quantidade que o usuário digitou
- `validavalor()`: Valida o valor que foi adiicionado para o produto
- `ValidaData()`: Valida a data de validade do produto

## TECNOLOGIAS UTILIZADAS

| Tecnologias         | Utilidade |
|---------------------|-----------|
| Python 3.13.7       | Linguagem principal de desenvolvimento do sistema. |
| Draw.io             | Design de fluxogramas. |
| Json                | Armazenamento de dados |

## BIBLIOTECAS

| Biblioteca | Utilidade |
|------------|-----------|
| `datetime` | Manipulação e formatação de datas e horários. |
| `os`       | Interação com o sistema operacional (pastas, arquivos, terminal). |
| `time`     | Controle de tempo, delays e marcação temporal. |
| `sys`      |Interação com o ambiente operacional do Python |
