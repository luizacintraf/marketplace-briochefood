# -*- coding: utf-8 -*-

#import libraries
from database.connect_database import *
import bcrypt
import pagarme
import re
from validate_docbr import CNPJ
import requests

#athenticate api key
from config.apikey import api_key
pagarme.authentication_key(api_key)

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

class bakery():
    def register(self, user, password, name, legal_name, email, cnpj,  state, city, neighborhood, street, street_number,  zipcode, phone_number, phone_type, ddd, agencia, bank_code, conta, conta_dv, shipping_fee):
        """
        Esta função efetua o cadastro de uma padaria.
        Primeiro ela faz a verificação das entradas.
        Depois cadastra a padaria como recipirent na pagarme
        Depois cadastra a padaria no banco de dados

        Atributos:
            user: nome do usuário
            password: senha
            name: nome da padaria
            legal_name: nome juridico da padaria
            email: email da padaria
            cnpj: cnpj d apadaria
            state: Estado da padaria
            city: cidade da padaria
            neighborhood: bairro da padaria,
            street: rua da padaria
            street_number: Número da padaria
            zipcode: cep da padaria,
            phone_number: número de telefone,
            phone_type: tipo do número (ex: mobile)
            ddd: DDD do telefone
            agencia: agencia da padaria
            bank_code: código do banco
            conta: conta
            conta_dv: digito da conta
            shipping_fee: quanto será cobrado de frete
        """
        statuszip,res=getAddress(zipcode)
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(session.query(Bakery).filter_by(user=user).first() != None):
            return 400, "Nome de usuário já cadastrado"
        elif(session.query(Bakery).filter_by(email=email).first() != None):
            return 400, "Email já cadastrado"
        elif(not re.search(regex,email)):
            return 400, "Favor inserir um email válido"
        elif(len(password) < 6):
            return 400, "A senha deve ter pelo menos 6 caracteres"
        elif not( CNPJ().validate(cnpj)):
            return 400, "CNPJ inválido"
        elif not( phone_number.isdigit() or len(phone_number)<8):
            return 400, "Telefone inválido"
        elif not( ddd.isdigit() or len(ddd)!=2):
            return 400, "DDD inválido"
        elif not( agencia.isdigit() or len(agencia)!=4):
            return 400, "Agência inválida!"
        elif not(bank_code.isdigit() or len(bank_code)!=3):
            return 400, "Código do banco inválido!"
        elif not( conta.isdigit() or len(conta)!=5):
            return 400, "Conta inválida!"
        elif not( conta_dv.isdigit() or len(conta_dv)!=1):
            return 400, "Digito inválido!"
        elif not( shipping_fee.replace('.','',1).isdigit()):
            return 400, "Frete inválido!"
        elif(statuszip==400):
            return 400, "CEP inválido"
        else:
            try:
                params = {
                            'anticipatable_volume_percentage': '0',
                            'automatic_anticipation_enabled': 'false',
                            'transfer_day': '0',
                            'transfer_enabled': 'true',
                            'transfer_interval': 'daily',
                            'bank_account': {
                                'agencia': agencia,
                                'bank_code': bank_code,
                                'conta': conta,
                                'conta_dv': conta_dv,
                                "document_type": "cnpj",
                                'document_number': cnpj,
                                'legal_name': legal_name
                            },
                            'register_information': {
                                'type': 'corporation',
                                'document_number': cnpj,
                                'company_name': name,
                                'email': email,
                                'phone_numbers': [{
                                    "ddd": ddd,
                                    "number": phone_number,
                                    "type": phone_type

                                }]
                            }
                        }
                
                try: 
                    recipient = pagarme.recipient.create(params)
                except:
                    return 400, pagarme.recipient.create(params)['errors'][0]['message']
                session.add(Bakery(user=user, password=bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()), name=name, legal_name=legal_name, email=email, cnpj=cnpj, state=state, city=city, neighborhood=neighborhood, street=street, street_number=street_number,  zipcode=zipcode, phone_number=phone_number, phone_type=phone_type, ddd=ddd, agencia=agencia, bank_code=bank_code, conta=conta, conta_dv=conta_dv, shipping_fee=shipping_fee,recipient_id=recipient['id']))
                session.commit()
                session.flush()
                return 200, "Cadastro efetuado com sucesso"
            except ValueError:
                return 401, ValueError

    def login(self,user,password):
        """
        Efetua o login da padaria
        Primeiro verifica os parametros e depois efetua o login.
        Atributos:
            user(string): usuário
            password(string):senha
        """
        user=session.query(Bakery).filter_by(user=user).first()
        if(user==None):
            return 400, "Usuário e/ou senha incorretos"
        else:
            hashed=user.password
            if bcrypt.checkpw(password.encode("utf-8"), hashed):
                self.id=user.idbakery
                return 200, "Logado com sucesso"
            else:
                return 400, "Usuário e/ou senha incorretos"
    
    def productsRegister(self,name,price,description,quantity):
        """
        Registro dos produtos da padaria
        
        Atributos:
            name(string): nome da padaria
            price(float): preço do produto
            description (string): descrição do produto
            quantity(integer):quantidade do produto
        """
        if(self.id):
            try:
                session.add(Product(name=name, price=price,description=description,quantity=quantity,idbakery=self.id))
                session.commit()
                return 200, "Produto cadastrado!"
            except ValueError:
                return 401, ValueError
        else: 
            return 400, "Usuário não está logado!"

    def listProducts(self):
        """
        Lista os produtos da padaria
        """
        self.produtos=session.query(Product).join(Bakery).filter_by(idbakery=self.id).all()
        if(self.produtos==None):
            return 0
        else:
            return self.produtos

    def getRecipient(self):
        """
        Pega o objeto do receber no banco da pagarme
        """
        user=session.query(Bakery).filter_by(idbakery=self.id).first()
        recipient = pagarme.recipient.find_by({"id":user.recipient_id})
        return recipient

    def loadBakery(self):
        """
        Retorna os dados da padaria
        """
        user=session.query(Bakery).filter_by(idbakery=self.id).first()
        return user
    def recipientBalance(self):
        """
        Retorna o Saldo da padaria
        """
        user=session.query(Bakery).filter_by(idbakery=self.id).first()
        balance = pagarme.recipient.recipient_balance(user.recipient_id)
        return balance
    def loadAllBakeries(self):
        """
        Retorna um objeto com todas as padarias cadastradas
        """
        bakery=session.query(Bakery).all()
        return bakery
    def getOneProduct(self,id):
        """
        Retorna os dados de um produto
        """
        return session.query(Product).filter_by(idproduct=id).first()
    def loadAllProducts(self):
        """
        Retorna os dados de todos os produtos
        """
        return session.query(Product).all()









