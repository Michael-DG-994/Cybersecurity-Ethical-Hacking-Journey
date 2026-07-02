#Funzione che calcoli la media mobile di una lista di numeri
1
numeri = list()

risultato = list() #per ora il risultato è una lista vuota dove assegnerò i valori delle medie una volta calcolato

def media_mobile (numeri, n): #definisco la funzione di media mobile
    
    for i in range (len(numeri)): #con i che è indice del ciclo e parte da 0 fino alla lunghezza della lista
        start= i-n+1 #con questo vediamo dove inizia la finestra
        if start < 0: #se è valore negativo voul dire che non abbiamo ancora abbastanza elementi
            start = 0 #quindi parte comunque da 0 finchè questo è il caso
        
        window= numeri[start:i+1] #una volta determinato l'inizio quindi, definiamo la finestra come la sezione della lista tra esso e l'indice+1 (indice parte da 0, n no, per quello)

        media = sum(window)/len(window) #la media sarà quindi la somma dei valori all'interno di questa finestra diviso per la quantità di numeri selezionati, che sarà n ma io posso anche definire come la len(window)

        risultato.append(media) #con append io posso andare ad aggiungere le medie che noi otteniamo nella lista di result

while True: #ciclo che mi serve per continuare a chiedere input numeri della lista finche non viene inserito un input vuoto
   
  ninput= input("inserisci un numero, quandi hai terminato manda invio senza alcun numero: ")
  if ninput == "": #input vuoto vuol dire che utente ha finito ha inserire numeri nella lista
     n=int(input("ora inserisci range finestra: "))
     media_mobile(numeri, n) #richiamo la funzione media_mobile
     print("la media mobile dei numeri nella tua lista è: ",risultato)
     break
  else: 
     nlist=int(ninput)
     numeri.append(nlist)
     print("questa è la tua lista: ", numeri)







    


     




        
     
    
    
