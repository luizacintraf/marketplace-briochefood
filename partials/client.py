
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import libraries
from controllers.client import client
from controllers.bakery import bakery
from partials.bakery import *
from partials.functions import *


#initialize variables
clientSession=client()
selectedBakery=0



def clientLogin():
    """
    Esta função é utilizada para pegar os parametros de login do usuário
    """
    print("Insira seus dados para login")
    status=0
    while (status!=200):
        user=input("Nome de usuário:    ")
        senha=input("Senha:    ")
        status,res=clientSession.login(user,senha)
        print(res)
    clientMenu()

def clientRegister():
    """
    Esta função pede ao usuário os dados para fazer o cadastro
    """
    print("Insira seus dados para cadastrar")
    status=400
    while (status!=200):
        user=input("Nome de usuário:    ")
        password=input("Senha:             ")
        name=input("Nome:    ")
        email=input("Email:      ")
        cpf=input("cpf:                ")
        phone_number=input("Tel:                 ")
        street,street_number,neighborhood,state,zipcode,city=askAddress()
        status,res=clientSession.register(name,email,cpf, phone_number, state, city, neighborhood, street, street_number,zipcode, user, password)
        print(res)

    clientLogin()

def showAllProducts():
    global selectedBakery
    """
    Esta função mostra todos os produtos disponiveis na loja e direcioan para o usuario adicionar ao carrinho.
    """
    for product in sessionBakery.loadAllProducts():
        printProducts(product)
    print("Digite o código do produto para adiciona-lo ao carrinho ou digite M para voltar ao menu de opções")
    option=input()
    while(option !='M' and not option.isdigit()):
         print("Opção inválida por favor digite novamente!")
         option=input()
    if(option !='M'):
        product=sessionBakery.getOneProduct(int(option))
        sessionBakery.id=product.idbakery
        if(len(clientSession.basket)==0):
            selectedBakery=product.idbakery
        checkCarrinho(int(option))
    else:
        optionsClient(option)

def checkout(): 
    """
    Esta função realiza o checkout do carrinho. Tendo duas opções:
    1. Cliente sem cadastro: são pedidas todas as informações necessárias para se realizar uma transação
    2. Cliente cadastrado: são pedidas apenas as informações não cadastradas
    """
    if(clientSession.id is None):
        print("Você deseja criar um cadastro (digite R), logar (digite L) ou continuar sem cadastro(digite S)?")
        option=input()
        if(option != 'S'):
            optionsClient(option)
        else:
            print("Digite suas informacoes pessoais")
            name= input("Nome completo:   ")
            email=input("Email:          ")
            cpf=input("CPF:          ")
            phone_number=input("Telefone:     ")
            print("Digite o endereço de cobrança")
            street,street_number,neighborhood,state,zipcode,city=askAddress()
            clientSession.register(name,email,cpf, phone_number, state, city, neighborhood, street, street_number,zipcode, user="falso", password="")
            print("O endereço de entrega é o mesmo da cobrança? Digite 1 para sim e 2 para não")
            option=invalidOptionList(input(),['1','2'])
            if(option=='1'):
                clientSession.shipping_address=clientSession.billing_address
            elif (option=='2'):
                street,street_number,neighborhood,state,zipcode,city=askAddress()
                clientSession.billing_adress=addressObject(street,street_number,neighborhood,state,zipcode,city)
            print("Digite os dados do cartão!")
            card_number=input("Digite o número do cartão:   ")
            card_cvv=input("Digite o cvv:    ")
            card_expiration_date=input("Digite a data de validade:   ")
            card_holder_name=input("Digite o nome como esta no cartao:  ")
            clientSession.card(card_number,card_cvv,card_expiration_date,card_holder_name)
            #clientSession.card={"card_number": card_number,"card_cvv": card_cvv,"card_expiration_date": card_expiration_date,"card_holder_name": card_holder_name}
            res,coment=clientSession.buy(sessionBakery.loadBakery().recipient_id,sessionBakery.loadBakery().shipping_fee,sessionBakery.id,name=name)
            print(coment)
            clientMenu()
    else:
            print("O endereço se entrega é o mesmo cadastrado? Digite 1 para sim e 2 para não")
            option=invalidOptionList(input(),['1','2'])
            if(option=='1'):
                clientSession.shipping_address=clientSession.address
            elif (option=='2'):
                street,street_number,neighborhood,state,zipcode,city=askAddress()
                clientSession.shipping_address=addressObject(street,street_number,neighborhood,state,zipcode,city)
            print("O endereço de cobrança é o mesmo da entrega ou é o mesmo cadastrado? Digite 1 para usar o endereço cadastrado, 2 para utilizar o endereço de entrega e 3 para digitar um novo")
            option=invalidOptionList(input(),['1','2','3'])
            if(option=='1'):
                clientSession.billing_address=clientSession.address
            elif (option=='2'):
                clientSession.billing_address=clientSession.shipping_address
            elif(option=='3'):
                street,street_number,neighborhood,state,zipcode,city=askAddress()
                clientSession.billing_address=addressObject(street,street_number,neighborhood,state,zipcode,city)
            print("Digite os dados do cartão!")
            card_number=input("Digite o número do cartão:   ")
            card_cvv=input("Digite o cvv:    ")
            card_expiration_date=input("Digite a data de validade:   ")
            card_holder_name=input("Digite o nome como esta no cartao:  ")
            #clientSession.card={"card_number": card_number,"card_cvv": card_cvv,"card_expiration_date": card_expiration_date,"card_holder_name": card_holder_name}
            clientSession.card(card_number,card_cvv,card_expiration_date,card_holder_name)
            res,coment=clientSession.buy(sessionBakery.loadBakery().recipient_id,sessionBakery.loadBakery().shipping_fee,sessionBakery.id)
            print(coment)
            clientMenu()

def showCart():
    """
    Essa função mostra todos os produtos no carrinho
    """
    if(len(clientSession.basket)==0):
        print("Seu carrinho está vazio, volte a nossa lojinha para adicionar produtos")
        clientMenu()
    else:
        bakerySelect=sessionBakery.loadBakery()
        print("Os seguintes itens estão no seu carrinho:")
        for product in clientSession.basket:
            print("*-------------*")
            print("Id: %s"%product['id'])
            print("Nome:"+product['title'])
            print("Preço unitario: R$%0.2f"%(float(product['unit_price'])))
            print("Quantidade: %s"%product['quantity'])
            print("Total: R$%0.2f"%(int(product['quantity']) * float(product['unit_price'])))
            print("*-------------*")
        print("Subtotal: R$%0.2f"%clientSession.calculateSubTotal())
        print("Frete: R$%0.2f"%bakerySelect.shipping_fee)
        print("Total: R$%0.2f"%(clientSession.calculateTotal(bakerySelect.shipping_fee)))
        print("Finalizar compra? Digite E para finalizar ou M para voltar ao menu")
        optionsClient(input())

def addToCart(code):
    """
    Esta função adiciona produtos no carrinho, perguntando a quantidade que o cliente deseja

    Atributos:
        code (integer): id do produto a ser checado
    """
    selectProduct=sessionBakery.getOneProduct(code)
    qntTotal=selectProduct.quantity
    print("Digite a quantidade")
    qnt=invalidOptionDigit(input())
    while(int(qnt)>int(qntTotal)):
        print("Não tem essa quantidade disponivel, por favor digite uma qunatidade menor")
        qnt=invalidOptionDigit(input())
    clientSession.addBasket(selectProduct.idproduct,selectProduct.name,selectProduct.price,qnt)
    print("Você deseja adicionar mais produtos no carrinho? Se sim digite 1, digite M para voltar ao menu e C para fechar o carrinho")
    option=input()
    if(option=='1'):
        chooseProducts()
    else:
        optionsClient(option)

def checkCarrinho(code):
    """
        Esta função checa se já a produtos no carrinho
        Caso o usuario pegue um produto de uma padaria e já tenha produtos de outra padaria no carrinho. É perguntado se ele gostaria de esvaziar o carrinho ou voltar a comprar na padaria anterior.

        Atributos:
            code (integer): id do produto a ser checado
    """
    global selectedBakery
    if(sessionBakery.id != selectedBakery and len(clientSession.basket)>0):
        print("Você já tem produtos no carrinho de outra padaria, gostaria de excluir e adicionar esse? Digite 1 para sim e 2 para voltar para a padaria que estava")
        option=invalidOptionList(input(),['1','2'])
        if(option=='1'):
            clientSession.basket=[]
            selectedBakery=sessionBakery.id
            addToCart(code)
        elif(option=='2'):
            sessionBakery.id=selectedBakery
            chooseProducts()
    else:
        addToCart(code)

def showBakeries():
    """
    Esta função mostra todas as opções de padarias e direciona para os produtos
    """
    global selectedBakery
    print("Aqui estão nossas deliciosas padarias")
    for bakery in sessionBakery.loadAllBakeries():
        print("*-------------*")
        print("codigo: %d"%bakery.idbakery)
        print("Nome:"+bakery.name)
        print("Rua:"+bakery.street)
        print("Bairro:"+bakery.neighborhood)
        print("*-------------*")
    print("Digite o código da padaria para visualizar seus produtos")
    id=input()
    sessionBakery.id=id
    
    if(len(clientSession.basket)==0):
        selectedBakery=id
    chooseProducts()

def chooseProducts():
    """
    Esta função mostra os produtos da padaria e direciona apara adicionar no carrinho
    """
    listBakeryProducts()
    print("Digite o codigo do produto para adicionar ao carrinho, digite P para escolher outra padaria ou digite M para voltar ao menu")
    option=input()
    while(option !='M'and option != 'P' and not option.isdigit()):
         print("Opção inválida por favor digite novamente!")
         option=input()
    if(option !='M'and option != 'P'):
        checkCarrinho(int(option))
    else:
        optionsClient(option)

def clientMenu():
    """
    esta função cria o menu de opções para o cliente
    """
    print("O que você gostaria de fazer?")
    print("     Digite R para realizar cadastro")
    print("     Digite L para efetuar login")
    print("     Digite B para escolher uma padaria")
    print("     Digite P para escolher um produto")
    print("     Digite C para visualizar seu carrinho")
    print("     Digite E para finalizar a compra")
    print("     Digite X para sair")
    optionsClient(input())

def optionsClient(option):
    """
    Esta função direciona o cliente de acordo com a opção selecionada

    Atributos:
        option(string): opção selecionada
    """
    if(option=='R'):
        clientRegister()
    elif(option=='L'):
        clientLogin()
    elif(option=='B'):
        showBakeries()
    elif(option=='P'):
        showAllProducts()        
    elif(option=="C"):
        showCart()
    elif(option=="E"):
        checkout()
    elif(option=="M"):
        clientMenu()
    else:
        "Opção inválida, tente novamente!"
        optionsClient(input())

  





