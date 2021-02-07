
# -*- coding: utf-8 -*-

#import libraries
from controllers.bakery import bakery

newBakery=bakery()

newBakery.login("padariapaodoce", "123456")

newBakery.productsRegister("pão francês","1.00","pão francês crocante","300")

newBakery.productsRegister("pão doce","1.50","pão doce fofinho","300")

print(newBakery.listProducts())

print(newBakery.getRecipient())

print(newBakery.recipientBalance())




