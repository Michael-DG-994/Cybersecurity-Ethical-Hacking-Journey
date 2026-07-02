
#calcolo perimetro e area di forme geometriche a partire da input utente

while True: #ciclo infinito così a fine operazione inizia nuovamente
   
    pi= 3.14 #potrei semplicemente importale il modulo math e usare math.pi, ma non lo farò ora
    #quindi definisco e basta un pi arrotondato alle sue prime 2 cifre decimali

    #import math

    def quad_calc (): #definisco funzione calcolo di quadrato
        try:
            lato_q = float(input("Inserisci lunghezza lato in cm: ")) #fa in modo che valorie sia float
            perimetro_q = lato_q*4
            area_q = lato_q**2 
            print(f"--- Il perimetro del quadrato è: {perimetro_q}cm e l'area è: {area_q}cm^2 ---")
        except ValueError: #se utente inserisce input che non è numerico valido da questo errore
            print("--- Hai inserito un input non valido! ---")
        
    def rect_calc (): #definisco funzione calcolo rettangolo
        try:
            base_r = float(input("Inserisci lunghezza della base in cm: "))
            altezza_r = float(input("Inserisci lunghezza dell'altezza lato in cm: "))
            perimetro_r = (base_r*2)+(altezza_r*2)
            area_r = base_r * altezza_r
            print(f"--- Il perimetro del rettangolo è: {perimetro_r}cm e l'area è: {area_r}cm^2 ---")
        except ValueError:
            print("--- Hai inserito un input non valido! ---")

    def circle_calc (): #definisco la funzione calcolo cerchio
        try:
            raggio = float(input("Inserisci lunghezza del raggio in cm: ")) 
            perimetro_c = pi*raggio*2
            #perimetro_c = math.pi * raggio*2
            area_c = pi*(raggio**2)
            #area_c = math.pi * (raggio**2)
            print(f"--- Il perimetro del cerchio è: {perimetro_c}cm e l'area è: {area_c}cm^2 ---")
        except ValueError:
            print("--- Hai inserito un input non valido! ---")

    forma = input("Inserisci la forma geometrica tra le seguenti: \n-- Quadrato --\n-- Rettangolo --\n-- Cerchio --\n").lower().strip()
    #qua metto prompt a utente di scegliere la forma geometrica, con .lower() e .strip() metto tutto in
    #lowercase e rimuovo accidentali spazi vuoti inseriti

    if forma == "quadrato": #controllo se input combacia con una delle forme disponibili
        quad_calc()
    elif forma == "rettangolo":
        rect_calc()
    elif forma == "cerchio":
        circle_calc()
    else:
        print("Input non valido: hai scelto una forma non supportata.") #in caso di input diverso