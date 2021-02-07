#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import libraries
from partials.bakery import *
from partials.client import *
from partials.functions import *
 
def optionsGeral(option):
    """
    Esta função direciona para as opções
    Atributos:
        option(integer): opção selecionada
    """
    if(option=='1'):
        print("Você já possui cadastro? Digite C para seguir para o cadastro e L para login")
        optionsBakery(input())
    elif(option=='2'):
        clientMenu()
    else:
        print("Opção inválida! tente novamente!")
        optionsGeral(input())

def home():
    """
    Nesta função é imprimida a pagina inicial de opções
    """
    print("Seja bem vindo ao Brioche Food!")
    print("Qual tipo de usuário você é? Digite 1 para padeiro e 2 para consumidor")
    option=input()
    optionsGeral(option)

    
if __name__ == '__main__':  
    home()

    





    
        





        
            


