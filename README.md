# Projeto AquaFlow

**Repositório AquaFlow - PISI1 - Projetos Interdiciplinares de Sistemas da Informação 1**                                                             
Desenvolvedores: Riquelme Ruan e Pedro H. de Oliveira                                                           
Docente Responsável: Cleyton Magalhães                                                        

Descrição de projeto: 
O AquaFlow é um sistema integrado de gerenciamento desenvolvido especialmente para depósitos de água, com o objetivo de otimizar a logística operacional, aprimorar a gestão comercial e fortalecer o relacionamento com os clientes. A plataforma permite acompanhar, em tempo real, o controle de estoques, pedidos e entregas, garantindo maior eficiência na distribuição e redução de custos. Com isso, o AquaFlow não apenas organiza o dia a dia do negócio, mas também cria condições para crescimento sustentável, melhoria contínua e competitividade no mercado.

## REQUISITOS FUNCIONAIS
 
###  1ª VA
RF001 - Menu inicial                                                                
RF002 -  Cadastro de Clientes                                                          
RF003 - Cadastro de Entregadores                                                                     
RF004 - Login                                          
RF005 - Configurações                                                                           
RF006 - Menu Compras                                     
RF007 - Menu Estoque                                                      
RF008 - Rankings                                                                                    
RF009 - Menu Principal                                          

###  2ª VA
RF010 - Interface do Sistema                                     
RF011 - Atualização Semanal dos Rankings                                            
RF012 - Metas Diárias para os Entregadores                                          
RF013 - Aviso sobre Baixo Estoque

## PRINCIPAIS FUNÇÕES DO CÓDIGO 

### AUTENTICAÇÃO DE USUÁRIO
- `MenuInicial()`: Menu inicial com opções de login e cadastro.
- `cadastrar()`: Cadastro de usuários com validação de e-mail, senha e nome.
- `login()`: Login do usuário

### Configurações da conta

- `configuracoes(email_logado)`: Acessa as configurações da conta do usuário.
- `MostraDados(email)`: Exibe informações da conta e pergunta se ele deseja mudar algo.
- `AtualizarDados(email_atual)`: Atualiza os dados do usuário
- `DeletarConta(email)`: Exclui a conta após a confirmação da senha do usuário


### Validações e Utilidades

- `limpaTerminal()`: Limpa a tela do terminal conforme o sistema operacional.
- `validaemail`: Verifica se o e-mail possui domínio permitido (`@gmail.com`, `@ufrpe.br`).
- `validasenha`: Valida senhas com base em regras de segurança (mín. 1 número, 1 maiúscula, e entre 4 a 8 caracteres).
