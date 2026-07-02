
#programma che chieda a utente di inserire una stringa e successivamente conti le occorrenze di ogni parola.

while True:

    def recur_count():
        user_str =str(input("Inserisci testo: ")).lower()
        word_list = user_str.split() #divido la string user in "parole" ma queste ancora contengono caratteri non esclusivamente alfabetici
        
        print(f"-----Lista di ogni parola o carattere inserita: {word_list}-----") #test

        clean_list=[]

        for word in word_list: #per ogni parola controllo se i character sono alfabetici
            clean_word = "".join(char for char in word if char.isalpha()) #unisce i caratteri in una parola se sono alfabetici, rimuove quelli non, controlla carattere per carattere che sia con .isalpha in clean_word
            if clean_word: 
                clean_list.append(clean_word) #aggiungiamo la parola pulita alla lista di parole pulite
        
        print(f"-----Lista di ogni parola, priva di caratteri o numeri, inserita: {clean_list}-----") #test


        recur= {} #faccio un dizionario di rioccorrenze così assegno un valore a ogni parola che farà da chiave
        for word in clean_list:
            recur[word] = clean_list.count(word) #assegno a ogni chiave "word" il valore di .count nella clean list della parola stessa, .count conta quante volte quel valore è trovao all'interno di clean_list
        print(f"##### Ogni parola e le sue corrispettive rioccorrenze: #####\n {recur}") #output finale del dizionario con ogni parola e il valore associato ovvero quante volte è stata ripetuta

    recur_count() #richiamo la funzione

