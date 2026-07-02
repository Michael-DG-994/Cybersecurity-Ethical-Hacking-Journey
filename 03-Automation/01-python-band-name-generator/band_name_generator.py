
#band_name_generator per consegna U1-S2-L2
#Partendo da input utente e da una lista pre-determinata di suffissi riceve in output un nome di una band.



sffxs = [" of steel", " of doom", " of pain", " of sorrow", " of torment", " of viciousness", " feat. Dave Mustaine", " of eternal suffering", " of carnage", "-tallica", " from outer space", " from hell", " from da hood", " of oblivion"]
import random #Carico il modulo "random" per usare la funzione random.choice() che mi permetterà di prendere casualmente un oggetto string casuale nella lista sffxs

#Corpo programma che svolge effettivamente la richiesta.

while True: #Necessario mettere tutto in un while così alla fine può iniziare da capo, non so se si può fa in maniera più carina ho trovato che così funziona
    print("Welcome to the EVIL Band Name Generator by Michael D.G., Press ENTER if you dare...") #Output richiesta iniziale di input per inviare generatore
    while True: #piccolo loop che controlla se l'utente ha effettivamente solo cliccato enter o ha inserito caratteri non validi
     if input("Press enter to continue...") != "": #lasciando "" vuoto solo l'input di enter può rompere il loop, tutto il resto causera il print sottostante
        print("Wrong input! try again!")
     else:
       break
    
    city_name = input("Insert your home town/city: ") #prompt di input nome città ad utente
    pet_name = input ("Now insert your pet's name or favorite animal: ") #prompt di input animale ad utente

    str_sum = city_name + "-" + pet_name #operatore string somma (dalla quale nome variabile) che ci serve per il nome band finale, dash in mezzo perchè non mi piaceva altrimenti il risultato
    band_name = str_sum + random.choice(sffxs) #un altro operatore string somma e finalmente la funzione random.choice che aggiunge un suffisso randomico dalla lista sffxs
    
    print("Your new super cool/evil band name is ", band_name , "! Isn't it awesome?!?!") #output del risultato finale!!!

#Fun fact: Dave mustaine NON ha scritto questo codice