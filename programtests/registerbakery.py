# -*- coding: utf-8 -*-

#import libraries
from controllers.bakery import bakery
import sys

newBakery=bakery()

res,coment=newBakery.register("padariapaodoce", "123456", "Padaria pao doce", "Padaria ltda", "paodoce@email.com", "64800381000176",  "SP", "Guarulhos", "Jardim Novo Portugal", "Rua Viking", "21",  "07160420", "90021923", "mobile", "11", "5902", "001", "56789", "2", "10.00")
if(res==400):
    print(coment)
    sys.exit()