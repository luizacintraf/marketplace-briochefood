
# -*- coding: utf-8 -*-

#import libraries
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Sequence
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

#base para os modelos
Base = declarative_base()

#criar tabela relacional
OrdersProducts= Table(
    "orders_has_products",
    Base.metadata,
    Column("idorderproduct", Integer, primary_key=True),
    Column("idorder", Integer, ForeignKey("orders.idorder")),
    Column("idproduct", Integer, ForeignKey("products.idproduct"))
)

#modelo da padaria
class Bakery(Base):
    __tablename__ = "bakeries"
    idbakery= Column(Integer, Sequence('bakery_id_seq'), primary_key=True)
    user=Column(String)
    password=Column(String)
    name = Column(String)
    legal_name=Column(String)
    email=Column(String)
    cnpj=Column(Integer)
    street=Column(String)
    street_number=Column(Integer)
    neighborhood=Column(String)
    city=Column(String)
    state=Column(String)
    zipcode=Column(Integer)
    phone_number=Column(Integer)
    phone_type=Column(Integer)
    ddd=Column(Integer)
    agencia=Column(Integer)
    bank_code=Column(Integer)
    conta=Column(Integer)
    conta_dv=Column(Integer)
    shipping_fee=Column(Float)
    recipient_id=Column(String)
    products = relationship("Product", backref=backref("bakeries"))
    orders = relationship("Order", backref=backref("bakeries"))
    
    def __repr__(self):
        return "<Bakery(idbakery='%d',user='%s',password='%s',name='%s',legal_name='%s',email='%s',cnpj='%d', street='%s', street_number='%d', neighborhood='%s', city='%s', state='%s',  zipcode='%d', phone_number='%d', phone_type= '%s', ddd='%d', agencia='%d', bank_code='%d',conta='%d',conta_dv='%d',shippin_fee='%f')>"%(self.idbakery,self.user,self.password,self.name,self.legal_name, self.email,self.cnpj,self.street,self.street_number, self.neighborhood,self.city,self.state, self.zipcode, self.phone_number, self.phone_type, self.ddd,self.agencia,self.bank_code,self.conta,self.conta_dv,self.shipping_fee)
 
#modelo do produto
class Product(Base):
    __tablename__ = "products"
    idproduct = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    name=Column(String)
    price=Column(Float)
    description=Column(String)
    quantity=Column(Integer)
    idbakery = Column(Integer, ForeignKey("bakeries.idbakery"))
    orders = relationship(
        "Order", secondary=OrdersProducts, back_populates="products"
    )
    def __repr__(self):
         return "<Product(idproduct='%d', name='%s', price='%f', description='%s', quantity='%d',idbakery='%d', order='%s')>" % (
                                 self.idproduct, self.name, self.price, self.description,self.quantity, self.idbakery, self.orders)

#modelo do cliente
class Client(Base):
    __tablename__ = "clients"
    idclient= Column(Integer,Sequence('client_id_seq'),  primary_key=True)
    user=Column(String)
    password=Column(String)
    name=Column(String)
    email=Column(String)
    cpf=Column(Integer)
    street=Column(String)
    street_number=Column(Integer)
    neighborhood=Column(String)
    city=Column(String)
    state=Column(String)
    country=Column(String)
    zipcode=Column(Integer)
    phone_number=Column(String)
    orders = relationship("Order", backref=backref("clients"))

    def __repr__(self):
        return "<CLient(idclient='%d',user='%s',password='%s',name='%s',email='%s',cpf='%d', street='%s', street_number='%d', neighborhood='%s', city='%s', state='%s', country='%s', zipcode='%d', phone_number='%s')>"%(self.idclient,self.user,self.password,self.name,self.email,self.cpf,self.street,self.street_number, self.neighborhood,self.city,self.state, self.country,self.zipcode, self.phone_number)

#modelo do pedido
class Order(Base):
    __tablename__ = "orders"
    idorder= Column(Integer, Sequence('order_id_seq'), primary_key=True)
    idclient = Column(Integer,ForeignKey("clients.idclient"))
    idbakery=Column(Integer, ForeignKey("bakeries.idbakery"))
    total=Column(Float) 
    products= relationship(
        "Product", secondary=OrdersProducts, back_populates="orders"
    )
    def __repr__(self):
        return "<Order( idcliente='%d', idbakery='%d', total='%f')>" % (
                                self.idclient, self.idbakery,self.total)



