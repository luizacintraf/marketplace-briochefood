# -*- coding: utf-8 -*-

#import libraries
from database.create_database import create
from controllers.client import client
from config.bakeryparam import params
import pagarme

#create databases
create()

#add a anonymos user to the Client database to use in the without register client
res,coment=client().register("Anonimo","anonimo@email.com","63433237832", "+5511999999999", "", "", "", "", "1", "63035250", user="Anonimo", password="anonimus1")


#Ask for pagarme API KEY and save in the file
print("Digite sua API KEY")
key=input()
file=open('config/apikey.py','w')
file.write(("api_key='"+key+"'"))
file.close()

#Register recipient in pagarme
pagarme.authentication_key(key)
recipient = pagarme.recipient.create(params)

#Add recipient id in config
file=open('config/recipient.py','w')
file.write("recipient_id='"+recipient['id']+"'")
file.close()

