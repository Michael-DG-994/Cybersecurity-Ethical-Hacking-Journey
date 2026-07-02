
benvenuto = "Hello, World!" #Definisco variabile 'Benvenuto' 

print(benvenuto.split(sep= ",")) #output è la lista di stringe separata da ',' come specificato

print(''.join(benvenuto)) #output sarà ora la stringa originale, che ho unito nuovamente con 'separatore'.join(stringa_originale)

welcome_py = " Welcome to Python!"

print(benvenuto + welcome_py) #output delle stringhe concatenate benvenuto + welcome_py che danno il prompt all'Utente di inserire dei dati

while True:
    username = input("Select your username") #prompt utente a inserire li suo username
    welcome_username = ["Welcome aboard ", username, ", Thanks for joining us!"] #creo una lista con le stringe necessarie per formulare il messaggio finale di avvio

    if isinstance(username, str) and len(username) > 1: #isinstance controlla che la variabile username sia una string, poi len controlla che username abbia almeno due caratteri
        break #esco da loop in quanto username è valido
    else:
        print("Your username is not valid, please use at least 2 characters and only valid symbols")

print(''.join(welcome_username)) #e finalmente le concateno in un singolo messaggio a schermo su terminale una volta che l'utente inserisce username valido




