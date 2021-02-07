# -*- coding: utf-8 -*-

#import libraries
import sys
from controllers.client import client
from controllers.bakery import bakery

newClient=client()
newBakery=bakery()

res,coment=newClient.register("Ana Julia","ana@email.com","39931810858", "+5511900067890", "SP", "São Paulo", "Cidade Nova São Miguel", "Rua Paulo Arms", "20","31330290", user="falso", password="")
if(res==400):
    print(coment)
    sys.exit()

newClient.shipping_address=newClient.billing_address

newClient.addBasket("1","pão francês","1.00","10")

print(newClient.calculateSubTotal())

shipping_fee=10

print(newClient.calculateTotal(10))

newBakery.id=1
recipient_id=newBakery.getRecipient()
print(recipient_id)
recipient_id=recipient_id[0]['id']
print(recipient_id)

newClient.card("4111111111111111","123","0922","Morpheus Fishburne")

res,coment=newClient.buy(recipient_id,shipping_fee,idbakery="1")
print(res)
print(coment)