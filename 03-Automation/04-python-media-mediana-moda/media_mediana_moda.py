
#Calcolo Media, Mediana, Moda 


num_list=list()

while True:

   ninput= input("inserisci un numero, quando hai terminato manda invio senza alcun numero: ")

   if ninput.strip() == "": #invio senza numero esce da ciclo
    break
      
   try:
     
     num=float(ninput) #assegno a num i float di ninput
     num_list.append(num) #aggiungo alla lista num_list ogni numero num
     
   except ValueError: #se input è stringa o carattere non valido da errore
      print("Input non valido!")
      
#calcolo media       
sum_list = sum(num_list) #totale somma dei numeri nella lista
media = sum_list/len(num_list) #calcolo della media
print(f"La somma è: {sum_list}\nLa media è: {media}") #output di somma messo per test poi lasciato

#calcolo moda
repet = {} #dizionario dove associo ad ogni numero che funge da chiave il valore di quante volte è stato ripetuto
for num in num_list:
  repet[num] = num_list.count(num) #assegno a ogni numero inserito da utente il valore .count di quante volte è stato ripetuto in num_list

freq=max(repet.values()) #con max(repet.values) prendo il valore NON LA CHIAVE del numero ripetuto più volte nel dizionario repet ES: {1:1 , 2:5, 3:1} freq=5 
if freq<=1:
    print("Errore, Numeri non si ripetono") #aggiunto su revisione oggi, notato che non ci stava
else:
    moda=repet[freq] #la moda sarà quindi il numero chiave del dizionario con il valore associato frequenza
    print(f"La moda è: {moda}")



#calcolo mediana
def mediana_fnc():

    num_length = len(num_list) #la mediana si calcola in due modi a seconda se la quantità totale dei numeri inseriti è pari o dispari 

    if num_length % 2 == 0: #se la quantità di numeri nella lista num_list è pari 
      indirizzo1 = num_length//2 #devo prendere la metà INTERA (senza decimali)
      indirizzo2 = num_length//2-1 #devo prendere il numero prima della la metà INTERA
      mediana = (num_list[indirizzo1] + num_list[indirizzo2]) / 2 #infine devo fare la media tra indirizzo1 e indirizzo2, quella sarà la mediana
      #ESEMPIO:              num_list = [1,2,3,4] quantità numeri pari quindi dovrei fare (2+3)/2, 2 e 3 si trovano rispettivemante in num_list[indirizzo1] e num_list[indirizzo2] 
      print(f"La mediana è: {mediana}")
    else:
      mediana = (num_length)//2 #se il numero è dispari la mediana è facile, prendo la metà INTERA (senza decimali)
      print(f"La mediana è: {mediana}") #ESEMPIO:            num_list = [1,2,3,4,5], 5 numeri // 2 = 2.5 arrotondato a 3 diventa la posizione centrale della lista (non so se ottimale, non penso)

mediana_fnc() #richiamo la funzione che ho appena fatto per mediana







     
        
