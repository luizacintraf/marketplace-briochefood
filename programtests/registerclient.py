# -*- coding: utf-8 -*-

#import libraries
import sys
from controllers.client import client

newClient=client()

res,coment=newClient.register("Ana Julia","ana@email.com","11185304894", "+5511900067890", "SP", "São Paulo", "Cidade Nova São Miguel", "Rua Paulo Arms", "20","31330290", user="anajulia", password="123456")
if(res==400):
    print(coment)
    sys.exit()