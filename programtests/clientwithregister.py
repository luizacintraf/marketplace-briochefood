# -*- coding: utf-8 -*-

#import libraries
import sys
from controllers.client import client
from controllers.bakery import bakery

newClient=client()
newBakery=bakery()

res,coment=newClient.login("anajulia","123456")
if(res==400):
    print(coment)
    sys.exit()

newClient.billing_address=newClient.address
newClient.shipping_address=newClient.address

newClient.addBasket("2","pão doce","1.50","10")

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



