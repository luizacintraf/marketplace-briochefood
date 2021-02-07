# briocheFood
Python code develop as a backend for a bakery marketplace

### Requirements
sqlalchemy <br/>
bcrypt <br/>
pagarme<br/>
validate_docbr<br/>

### Instalation
After install dependencies <br/>
Create an account on [Pagar.me](https://dashboard.pagar.me/#/login)<br/>
Get your api key in [dashboard](https://dashboard.pagar.me/#/myaccount/apikeys)<br/>
Edit config/bakeryparam with the information of Brioche food (main recipient)<br/>
run setup.py

### Usage
Run main.py to interact with the application in console
Run runregisters.py to create one client and one bakery in database
Run runtests.py to test the functionalities


### Folder structure
        .
    ├── config
    │   ├── apikey.py                   # Store api key from pagarme
    │   ├── bakeryparam.py              # Brioche food parameters  
    │   └── recipient.py                # Store recipient id created in setup
    ├── controllers                     # Backend of application
    │   ├── client.py                   # Class with functions used in client view
    │   └── bakery.py                   # Class with functions used in bakery view
    └── database                        #files related with database
    │   ├── connect_database.py         # Connect to database
    │   ├── create_database.py          # Run database models and create database
    │   └── models.py                   # Database models
    └── partials                        #files called in main
    │   ├── bakery.py                   # User interactions with bakery
    │   ├── client.py                   # User interactions with client
    │   └── funtions.py                 # Useful functions
    └── programtests                    #tests
    │   ├── bakery.py                   # tests from bakery controller
    │   ├── clientwithoutregister.py    # tests from client without register
    │   ├── clientwithregister.py       # tests from client with register 
    │   ├── registerbakery.py           # create test bakery       
    │   └── registerclient.py           # create test client
    ├── setup.py                        #program setup
    ├── main.py                         #program main application
    ├── runregisters.py                 #create tests registers of client and bakery
    ├── runtests.py                     #run tests
    └── README.md                       #readme