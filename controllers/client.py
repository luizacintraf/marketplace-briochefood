# -*- coding: utf-8 -*-

#import libraries
from database.connect_database import *
import bcrypt
import re
import pagarme
from validate_docbr import CPF
from datetime import date
try: 
    from config.recipient import recipient_id as recipient_master
    #athenticate api key
    from config.apikey import api_key
    pagarme.authentication_key(api_key)
except:
    pass
import requests



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

class client():
    def __init__(self,basket=[]):
        self.basket=basket
        self.id=None
    def register(self,name,email,cpf, phone_number, state, city, neighborhood, street, street_number,zipcode, user="falso", password=""):
        """
        Aqui é feito o cadastro do cliente e a geração do objeto do costumer.
        Caso o cliente não queira se cadastrar, é enviado um id de um usuario anonimo ao costumer, devido as leis da LGPD só podem ser salvas as informações se o cliente autorizar.
        Caso contrário o cliente pede para cadastrar e cria um login e senha.
       

        Atributos:
            name (string): Nome do cliente
            email (string): Email do cliente
            cpf (integer): CPF do cliente
            phone_number (integer): Número de telefone
            state (string): Esatdo do cliente
            city (string): Cidade do cliente
            neighborhood (string): bairro do cliente
            street (string): Rua do cliente
            street_number (integer): Número da casa do cliente
            user(string): Nome do usuário
            password (string): Senha do usuário
        """
        statuszip,res=getAddress(zipcode)
        
        if len(re.findall('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',email))<0:
            return 400, "Favor inserir um email válido"
        elif(not CPF().validate(cpf)):
            return 400, "Favor inserir um cpf válido"
        elif(len(re.findall(r"\+?[\d]{8}",phone_number))<0):
            return 400, "Favor inserir um telefone válido"
        elif(statuszip==400):
            return 400, "CEP inválido"
        else:
            if(user=="falso"):
                userFind=session.query(Client).filter_by(user="Anonimo").first()
                self.id=userFind.idclient
                self.name=name
                self.customer_data = {
                    'external_id': str(userFind.idclient),
                    'name': name,
                    'type': 'individual',
                    'country': 'br',
                    'email': email,
                    'documents': [
                        {
                            'type': 'cpf',
                            'number': cpf
                        }
                    ],
                    'phone_numbers': [phone_number],
                    }
                self.billing_address=({'street':street,
                                    'street_number':street_number,
                                    'neighborhood':neighborhood,
                                    'state':state,
                                    'city':city,
                                    'country':'br',
                                    'zipcode':zipcode})
            else:

                if(session.query(Client).filter_by(user=user).first() != None):
                    return 400, "Nome de usuário já cadastrado"
                elif(session.query(Client).filter_by(email=email).first() != None):
                    return 400, "Email já cadastrado"
                elif(len(password) < 6):
                    return 400, "A senha deve ter pelo menos 6 caracteres"   
                else:
                    try: 
                        newClient=Client(user=user, password=bcrypt.hashpw(
                        password.encode("utf-8"), bcrypt.gensalt()), name=name,email=email,cpf=int(cpf), phone_number=int(phone_number),state=state, city=city, neighborhood=neighborhood, street=street, street_number=int(street_number), zipcode=int(zipcode))
                        session.add(newClient)
                        session.commit()
                        session.flush()
                        session.refresh(newClient)
                        self.customer_data = {
                            'external_id': str(newClient.idclient),
                            'name': name,
                            'type': 'individual',
                            'country': 'br',
                            'email': email,
                            'documents': [
                                {
                                    'type': 'cpf',
                                    'number': str(cpf)
                                }
                            ],
                            'phone_numbers': [str(phone_number)],
                        }
                        customer = pagarme.customer.create(self.customer_data)
                    except Exception as e: 
                        return 400, e
        return 200, self.customer_data
    def login(self,user,password):
        """
        Esta função efetua o login do cliente e retorna a variavel costumer_data

        Atriutos:
            user (string): usuário
            password(string) : senha
        """
        user=session.query(Client).filter_by(user=user).first()
        if(user==None):
            return 400, "Usuário e/ou senha incorretos"
        else:
            hashed=user.password
            if bcrypt.checkpw(password.encode("utf-8"), hashed):
                self.id=user.idclient
                self.name=user.name
                self.address={'street':user.street,
                'street_number':str(user.street_number),
                'neighborhood':user.neighborhood,
                'state':user.state,
                'city':user.city,
                'country':'br',
                'zipcode':str(user.zipcode)}
                self.customer_data = {
                    'external_id': str(user.idclient),
                    'name': user.name,
                    'type': 'individual',
                    'country': 'br',
                    'email': user.email,
                    'documents': [
                        {
                            'type': 'cpf',
                            'number': str(user.cpf)
                        }
                    ],
                    'phone_numbers': ["+"+str(user.phone_number)],
                }
                return 200, "Logado com sucesso"
            else:
                return 400, "Usuário e/ou senha incorretos"
    def addBasket(self,id,name,price,qnt):
        """
        Esta função adiciona itens ao carrinho
        Atributos:
            id (integer): id do produto
            name (string): nome do produto
            price (string): preço do produto
            qnt (integer): quantidade do produto 
        """
        self.basket.append({"id": str(id),"title": name,"unit_price": price,"quantity": str(qnt),"tangible": True})
    def calculateSubTotal(self):
        """
        Calcula o Subtotal da compra baseada nos itens do carrinho
        """
        if(len(self.basket) !=0):
            return sum([int(x['quantity'])*float(x['unit_price']) for x in self.basket])
    def calculateTotal(self,shipping_fee):
        """
        Calcula o Total da compra
        Atributos: 
            shipping_fee (float): frete da compra
        """
        if(len(self.basket) !=0):
            return self.calculateSubTotal() + shipping_fee
    def card(self, card_number,card_cvv,card_expiration_date,card_holder_name):
        """
        Cria um objeto do cartão e adiicona esse atributo
        Atributos:
            card_number(str): número do cartão
            card_cvv (str): CVV do cartão
            card_expiration(str): data de validade
            card_holder_name(str): Nome no cartão
        """
        self.card= {"card_number": card_number,"card_cvv": card_cvv,"card_expiration_date": card_expiration_date,"card_holder_name": card_holder_name}
        return self.card
    def buy(self,recipient_id,shipping_fee, idbakery, billing_addres="billing_addres", customer_data="customer_data", shipping_address="shipping_address", name="name",card="card"):
        """
        Realiza a compra dos produtos e atualiza os bancos
        Atributos:
            recipient_id (integer) : id do recebedor
            shipping_fee (float): frete da compra
            idbakery(int): Id da padaria
            billing_addres(dict): Endereço do pagamento
            customer_data(dict):Dados do comprador
            shipping_address (dict): Endereço de entrega
            name (string): Nome do comprador
        """
        if(name=="name"):
            name=self.name
        if(billing_addres=="billing_addres"):
            billing_address=self.billing_address
        if(shipping_address=="shipping_address"):
            shipping_address=self.shipping_address
        if(customer_data=="customer_data"):
            customer_data=self.customer_data
        if(card=="card"):
            card=self.card
        
        basket=self.basket
        
        total=self.calculateTotal(shipping_fee)*100

        

        for item in basket:
            item["unit_price"]=int((float(item["unit_price"])*100))

        
        params = {
            "amount": total,
            "card_number": card['card_number'],
            "card_cvv": card['card_cvv'],
            "card_expiration_date": card['card_expiration_date'],
            "card_holder_name": card['card_holder_name'],
            "customer": customer_data,
            "billing": {
                "name": name,
                "address":billing_address
            },
            "shipping": {
            "name": name,
            "fee": shipping_fee,
            "delivery_date": date.today().strftime("%Y-%m-%d"),
            "expedited": True,
            "address": shipping_address
            },
            "items": basket,
            "split_rules": [
                {
                "recipient_id": recipient_id,
                "percentage": 85,
                "liable": False,
                "charge_processing_fee": True
                },
                {
                "recipient_id": recipient_master,
                "percentage": 15,
                "liable": True,
                "charge_processing_fee": True
                }
                
            ]
        }
        try: 
            pagarme.transaction.create(params)
            
            order=Order(idclient=self.id,idbakery=idbakery,total=(total/100))
            for item in self.basket:
                product=session.query(Product).filter_by(idproduct=int(item['id'])).first()
                newQuantity=product.quantity-int(item['quantity'])
                session.query(Product).filter_by(idproduct=int(item['id'])).update({Product.quantity: newQuantity})
                session.commit()
                order.products.append(product)
            session.add(order)
            session.commit()
            session.flush()
            session.refresh(order)

            self.basket=[]
            
            return 200,"Transação efetuada com sucesso"
        except Exception as e: 
            return 400, e


    
            
