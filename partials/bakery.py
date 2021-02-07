# -*- coding: utf-8 -*-

#import libraries
from controllers.client import client
from controllers.bakery import bakery
from partials.functions import *


sessionBakery=bakery()

def bakeryMenu():
    """
    Menu de opções de ações para a padaria
    """
    print("O que você gostaria de fazer?")
    print("     Digite P para cadastrar produtos")
    print("     Digite V para ver os produtos da sua lojinha")
    print("     Digite S para verificar o seu saldo")
    print("     Digite X para sair")
    optionsBakery(input())

def optionsBakery(option):
    """
    Direcionamento das ações
    """
    if(option=='P'):
        productsRegister()
    elif(option=='L'):
        loginBakery()
    elif(option=='C'):
        bakeryRegister()
    elif(option=='V'):
        listBakeryProducts()
        print(" ")
        print("----------------------------------")
        bakeryMenu()
    elif(option=='S'):
        showFunds()

    elif(option=='M'):
        bakeryMenu()
    elif(option=='X'):
        exit
    else:
        print("Opção inválida! tente novamente!")
        optionsBakery(input())

def showFunds():
    funds=sessionBakery.recipientBalance()
    print("Saldo a receber: R$%0.2f"%(funds['waiting_funds']['amount']/100))
    print("Saldo transferido: R$%0.2f"%(funds['transferred']['amount']/100))
    print("Saldo disponivel: R$%0.2f"%(funds['available']['amount']/100))

    print(" ")
    print("----------------------------------")
    bakeryMenu()

def productsRegister():
    """
    Esta função pede os dados da padaria para realizar o registro
    """
    print("Digite as informações do seu produto")
    continuar='1'
    while continuar=='1':
        name=input("Nome do produto:    ")
        price=input("Preço do produto:   ")
        description=input("Descrição do produto:   ")
        quantity=input("Quantidade do produto:   ")
        status,res=sessionBakery.productsRegister(name,price,description,quantity)
        
        if(status==200):
            print(res)
            print("Digite 1 para adicionar mais produtos, M para voltar ao seu menu de opções")
            continuar=input()
        else:
            print(res)
            exit
    print("Saindo da edição de produtos...")
    optionsBakery(continuar)

def listBakeryProducts():
    """
    Esta função lista os produtos da padaria
    """
    if(len(sessionBakery.listProducts())==0):
        print("Não há produtos cadastrados")
    else:
        for product in sessionBakery.listProducts():
            printProducts(product)

def loginBakery():
    """
    Esta função efetua o login da padaria
    """
    print("Insira seus dados para login")
    status=0
    while (status!=200):
        user=input("Nome de usuário:    ")
        senha=input("Senha:    ")
        status,res=sessionBakery.login(user,senha)
        print(res)
    bakeryMenu()

def bakeryRegister():
    """
    Esta função pede ao usuário os dados para fazer o cadastro
    """
    print("Insira seus dados para cadastrar")
    status=400
    while (status!=200):

        user=input("Nome de usuário:    ")
        password=input("Senha:             ")
        name=input("Nome fantasia da padaria:    ")
        legal_name= input("Nome juridico da padaria:    ")
        email=input("Email:      ")
        cnpj=input("CNPJ:                ")

        ddd=input("DDD:     ")
        phone_number=input("Tel:                 ")
        phone_type=input("Tipo do telefone(ex: mobile):    ")

        street,street_number,neighborhood,state,zipcode,city=askAddress()

        print("Insira seus dados bancarios para receber os pagamentos")
        agencia=input("Agencia:         ")
        bank_code=input("Codigo do banco:     ")
        conta=input("Conta:      ")
        conta_dv=input("Digito:    ")

        print("Insira os dados do frete")
        shipping_fee=input("Frete unico:      ")

        status,res=sessionBakery.register(user, password, name, legal_name, email, cnpj,  state, city, neighborhood, street, street_number,  zipcode, phone_number, phone_type, ddd, agencia, bank_code, conta, conta_dv, shipping_fee)
        print(res)
    loginBakery()



    




