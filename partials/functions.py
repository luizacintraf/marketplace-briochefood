
# -*- coding: utf-8 -*-
import requests

def invalidOptionList(option,options):
    """
    Essa função verifica se a opção selecionada esta na lista de opções fornecidas
    """
    while (option not in options):
        print("Opção inválida digite novamente!")
        option=input()
    return option

def invalidOptionDigit(option):
    """
    Essa função verifica se a opção selecionada é um inteiro
    """
    while (not option.isdigit()):
        print("Opção inválida digite novamente!")
        option=input()
    return option

def askAddress():
    """
    Essa função busca um endereço baseada no cep fornecido, e retorna um endereço completo
    """
    status=400
    while status==400:
        zipcode=input("Digite o CEP:   ")
        status,res=getAddress(zipcode)
        if(status==400):
            print(res)
    print("Rua:  "+res['street'])
    print("Bairro:  "+res['neighborhood'])
    print("Cidade: "+res['city'] )
    print("Estado: "+res['state'])
    print("Digite 1 para confirmar as informações, ou 2 para digitar o cep novamente")
    option=invalidOptionList(input(),['1','2'])
    if(option=='1'):
        street_number=input("Número:  ")
        street_number=invalidOptionDigit(street_number)
        return res['street'],street_number,res['neighborhood'] ,res['state'] ,res['zipcode'] ,res['city']
    elif(option=='2'):
        askAddress()

def printProducts(product):
    """"
    Esta função imprime os dados do produto
    """
    print("*-------------*")
    print("Id:"+str(product.idproduct))
    print("Nome:"+product.name)
    print("Preço: R$%0.2f"%(product.price))
    print("Descrição:"+product.description)
    print("*-------------*")

def addressObject(street,street_number,city,neighborhood,state,zipcode):
    """
    Esta função faz um objeto do endereço
    Atributos:
            state (string): Estado
            city (string): Cidade 
            neighborhood (string): bairro 
            street (string): Rua 
            street_number (integer): Número da casa
            zipcode(onteger): CEP
    """
    return {'street':street,
    'street_number':street_number,
    'neighborhood':neighborhood,
    'state':state,
    'city':city,
    'country':'br',
    'zipcode':zipcode}

def getAddress(zipcode):
    """
    Esta função retorna o endereço, dado o cep
    Atributos:
        zipcode (integer): cep para pesquisa
    """
    response=requests.get("https://api.pagar.me/1/zipcodes/"+zipcode).json()
    if 'errors' in response.keys():
        return 400,response['errors'][0]['message'] 
    else:
        return 200,response
