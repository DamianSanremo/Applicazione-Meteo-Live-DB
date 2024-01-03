######################################
#   APPLICAZIONE METEOLIVE DB        #
#                                    #   
# Studente:     Damian Dutka         #
# Matricola     2941875              #
# Esame:        BASI DI DATI 1       #
# Codice esame: 27667                #
# Universita' di Genova              #
# Facolta' di Ingegneria Informatica #
######################################

from tkinter import * 
from tkinter import ttk, messagebox
from datetime import datetime
import locale
import requests
import sqlite3
import io
from io import BytesIO
from urllib.request import urlopen
from PIL import Image, ImageTk


#Creo una finestra del programma di dimensioni 340x400 e fornisco un titolo al nome del programma
finestra = Tk()
finestra.title("Applicazione MeteoLive DB")
finestra.geometry("340x400")

# Funzione per convertire la direzione del vento da gradi in punti cardinali   
def get_wind_direction(wind_direction):
    if wind_direction > 337.5 or wind_direction <= 22.5:
           return 'Nord'
    elif 22.5 < wind_direction <= 67.5:
           return 'Nord-Est'
    elif 67.5 < wind_direction <= 112.5:
           return 'Est'
    elif 112.5 < wind_direction <= 157.5:
           return 'Sud-Est'
    elif 157.5 < wind_direction <= 202.5:
           return 'Sud'
    elif 202.5 < wind_direction <= 247.5:
           return 'Sud-Ovest'
    elif 247.5 < wind_direction <= 292.5:
           return 'Ovest'
    elif 292.5 < wind_direction <= 337.5:
           return 'Nord-Ovest'

# Funzione per scaricare l'immagine della città dall'API, ridimensionarla e visualizzarla
def load_city_image():
    city = city_search_box.get()
    
    # Unsplash access key
    access_key = 'Vxk_ofMGMVZibPzYhWdkXmMtNewaY0h4yq9UkB3p0NY'
    url = f'https://api.unsplash.com/photos/random?query={city}&order_by=popular&client_id={access_key}'

    # Risposta dall'API di Unsplash e scaricamento dell'immagine
    response = requests.get(url)
    response.raise_for_status()
    image_data = response.json()
    image_url = image_data['urls']['regular']
    image_response = requests.get(image_url)
    image_response.raise_for_status()

    # Apre l'immagine tramite libreria PIL
    image = Image.open(BytesIO(image_response.content))

    # Ridimensiona l'immagine a 340 pixel di larghezza mantenendo la proporzione
    original_width, original_height = image.size
    target_width = 340
    target_height = int((target_width / original_width) * original_height)
    image = image.resize((target_width, target_height))

    # Converte da PIL a PhotoImage della libreria Tkinter
    pil_image = ImageTk.PhotoImage(image)

    # Aggiorna il label con la nuova immagine
    label_api_unsplash.config(image=pil_image)
    label_api_unsplash.image = pil_image  # Keep a reference to avoid garbage collection        
        
# Funzione per scaricare i dati dall'API OpenWeather
def fetch_weather_data():
    # Prende l'input della città dall'utente e fa l'output con la prima lettera sempre in maiuscolo
    city = city_search_box.get().capitalize()
    # Imposta date time in lingua italiana
    global today_date
    locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')
    today_date = datetime.now().strftime("%a, %d %B %Y").title()
    # Costruisce l'url per L'API request e lo esegue
    api_key = 'a0e78d3b449db7059df0a38abd3952f8'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}&lang=it'
    response = requests.get(url)
    # Controlla se la richiesta e' andata a buon fine (status code 200)
    if response.status_code == 200:
        # Analizza la risposta JSON e estrae i dati richiesti
        data = response.json() 
        weather = data['weather'][0]['description']
        weather_icon = data['weather'][0]['icon']
        icon_url = f'http://openweathermap.org/img/wn/{weather_icon}@2x.png'
        # Scarica e visualizza l'icona meteo direttamente 
        icon_data = requests.get(icon_url).content
        # Converte in PhotoImage e ridimensiona 
        global icon_image
        icon_image = ImageTk.PhotoImage(Image.open(BytesIO(icon_data)).resize((40, 40)))
        temperature = round(data['main']['temp'], 1)
        temp_min = round(data['main']['temp_min'], 1)
        temp_max = round(data['main']['temp_max'], 1)
        humidity = data['main']['humidity']
        wind_speed = round(data['wind']['speed'] * 3.6, 1)
        wind_direction = data['wind']['deg']
        direction_of_wind = get_wind_direction(wind_direction)

        # Formatta la data nel formato giorno-mese-anno per utilizzarla nel database
        date_of_today = datetime.now().strftime("%d-%m-%Y")
      
        return date_of_today, city, weather, temperature, temp_min, temp_max, humidity, wind_speed, direction_of_wind
    else:
        # Mosta un messaggio d'errore se c'e' un problema con l'API request
        messagebox.showerror("Error", "Attenzione! Nome inserito errato o inesistente o problema di connessione. Riprova!")
        return None  # Fa un return None per indicare l'errore

		
# Funzione per connettersi al database table memorizzando i dati recuperati dall'API
def connect_and_store_in_database():
    date_of_today, city, weather, temperature, temp_min, temp_max, humidity, wind_speed, direction_of_wind = fetch_weather_data()

    # Connessione al database tramite libreria sqlite3
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    try:
        sql_statement = '''
        INSERT INTO weather_data (date_of_today, city, weather, temperature, temp_min, temp_max, humidity, wind_speed, direction_of_wind)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        # Inserisce i dati nel table
        cursor.execute(sql_statement, (
        date_of_today, city, weather, temperature, temp_min, temp_max, humidity, wind_speed, direction_of_wind))

        # Conferma le modifiche
        conn.commit()
        update_labels()
    except Exception as e:
        print(f'Errore durante la creazione del table o in inserimento: {e}' )
    finally:
        # Chiude la connessione nel blocco 'finally' anche se c'e un'eccezione
        conn.close()
        database()


# Funzione che aggiorna i widget labels        
def update_labels():
    global today_date
    date_of_today, city, weather, temperature, temp_min, temp_max, humidity, wind_speed, direction_of_wind = fetch_weather_data()
    city_label.config(text=city)
    today_date_label.config(text=today_date)       	
    icona_meteo_label.config(image=icon_image)
    descrizione_meteo_label.config(text=weather) 
    temperatura_label.config(text=f"{temperature}°")
    temp_min_label.config(text=temp_min)
    temp_max_label.config(text=temp_max)
    humidity_label.config(text=humidity)
    wind_speed_label.config(text=f"{wind_speed} KM / H")
    wind_direction_label.config(text=direction_of_wind)                    

# Funzione cerca azionata dal pulsante button_find_city_weather
def search():
    connect_and_store_in_database()
    load_city_image()    
    
# Funzione azionata dal pulsante button_mostra_database che allarga la finestra fino a 740pixel 
def mostra_database():
    finestra.geometry('740x400')

# Funzione azionata dal pulsante button_indietro che riduce la finestra alla dimensione originaria
def indietro():
    finestra.geometry('340x400')    
    
# Funzione che inserisce un testo placeholder nel search box e lo elimina quando l'utente clicca sul search_box   
def placeholder(event):
    if city_search_box.get() == placeholder_text:
        city_search_box.delete(0, END)
        city_search_box.configure(show="")
        
# Funzione delete_row
def delete_row():
    selected_item = tree.selection()
    if selected_item:
        # Riceve l'ID della riga selezionata
        selected_id = tree.item(selected_item, 'values')[0]

        # Connette al database tramite libreria sqlite3
        conn = sqlite3.connect('weather_data.db')
        cursor = conn.cursor()

        # Elimina la riga dal database in base all'ID e chiude la connessione
        cursor.execute('DELETE FROM weather_data WHERE ID = ?', (selected_id,))
        conn.commit()
        conn.close()

        # Elimina l'elemento anche dal widget Treeview
        tree.delete(selected_item)

	      # Aggiorna la tabella visualizzata tramite widget Treeview chimando la funzione 
        database()            
        
		
##########-----I WIDGET LABELS-----##########

# Sfondo del programma
sfondo = PhotoImage(file='sfondo_app.png')
label_sfondo = Label(finestra, image=sfondo)

# Immagine della citta'
default = PhotoImage(file='default.png')
label_api_unsplash = Label(finestra, image=default) 

# Casella di ricerca citta'
city_search_box = Entry(finestra, font=("Roboto", 14, "normal"), bd=0, highlightthickness=0)
placeholder_text = "Inserisci citta'..."
city_search_box.insert(0, placeholder_text)
city_search_box.bind("<FocusIn>", placeholder)

# Pulsante cerca meteo
button_find_city_weather = PhotoImage(file='button_find_city_weather_40x40.png')
search_weather_button = Button(finestra, image=button_find_city_weather, command=search, borderwidth=0, relief="flat", bg='white', activebackground='#414041')

# Citta'
city = "Genova"
city_label = Label(finestra, text=city, font=("Roboto Condensed", 34), bg='white', fg="#414041")

# Data di oggi
today_date = "Ven, 22 Dicembre 2023"
today_date_label = Label(finestra, text=today_date, font=("Roboto Condensed", 11 ), bg='white', fg="#414041")

# Icona meteo
icona_meteo_default = PhotoImage(file='default_icon.png')
icona_meteo_label = Label(finestra, image=icona_meteo_default)

# Descrizione del meteo
descrizione_meteo = "nubi sparse"
descrizione_meteo_label = Label(finestra, text=descrizione_meteo, font=("Roboto Condensed", 18 , "italic" , "normal" ), bg='white', fg="#414041")

# Temperatura
temperatura = "12.5°"
temperatura_label = Label(finestra, text=temperatura, font=("Roboto Condensed", 54), bg='white', fg="#414041")

# Massima
temp_max = "14"
temp_max_label = Label(finestra, text=temp_max, font=("Roboto", 10, "bold"), bg='white', fg="#414041")

# Minima
temp_min = "11"
temp_min_label = Label(finestra, text=temp_min, font=("Roboto", 10 , "bold"), bg='white', fg="#414041")

# Umidita'
humidity = "37"
humidity_label = Label(finestra, text=humidity, font=("Roboto", 10 , "bold"), bg='white', fg="#414041")

# Velocita' del Vento
wind_speed = "5 KM / H"
wind_speed_label = Label(finestra, text=wind_speed, font=("Roboto", 10 , "bold"), bg='white', fg="#414041")

# Direzione del vento
wind_direction = "Nord-Est"
wind_direction_label = Label(finestra, text=wind_direction, font=("Roboto", 10 , "bold"), bg='white', fg="#414041")

# Pulsante mostra database
button_mostra_database = PhotoImage(file='button_mostra_database.png')
mostra_database_button = Button(finestra, image=button_mostra_database, command=mostra_database, borderwidth=0, relief="flat", bg='white', activebackground='white', bd=0, highlightthickness=0)

# Casella di testo del database
search_box_database = Entry(finestra, font=("Roboto", 14, "normal"), bd=0, highlightthickness=0)

# Pulsante cancella riga della tabella del database
button_delete = PhotoImage(file='button_delete.png')
delete_button = Button(finestra, image=button_delete, command=delete_row, borderwidth=0, relief="flat", bg="#414041", activebackground='#414041', bd=0, highlightthickness=0)

# Pulsante indietro (la finestra torna alla dimensione originaria)
button_indietro = PhotoImage(file='button_indietro.png')
indietro_button = Button(finestra, image=button_indietro, command=indietro, borderwidth=0, relief="flat", bg="#414041", activebackground='#414041', bd=0, highlightthickness=0)

##########-----POSIZIONE DEI WIDGET LABELS-----##########

# Sfondo del programma
label_sfondo.place(x=0, y=0, width=740, height=400)

# Immagine della citta'
label_api_unsplash.place(x=0, y=0, width=340, height=200) 

# Casella di ricerca citta'
city_search_box.place(x=120, y=0, width=160, height=40)

# Pulsante di ricerca meteo
search_weather_button.place(x=267, y=0, width=40, height=40) 

# Citta'
city_label.place(x=20,y=205 , height=40)

# Data di oggi
today_date_label.place(x=20,y=246 , height=20)

# Icona meteo
icona_meteo_label.place(x=20, y=271, width=40, height=40)

# Descrizione condizione meteo
descrizione_meteo_label.place(x=68,y=272, height=36)

# Temperatura
temperatura_label.place(x=20,y=320, height=60)

# Massima
temp_max_label.place(x=230,y=317, height=18)

# Minima
temp_min_label.place(x=283,y=317, height=18)

# Umidita'
humidity_label.place(x=231,y=336, height=18)

# Velocita' del vento
wind_speed_label.place(x=231,y=355, height=18)

# Direzione del vento
wind_direction_label.place(x=231,y=373, height=18)
    
# Pulsante mostra database    
mostra_database_button.place(x=249, y=205)

# Casella di testo database
search_box_database.place(x=453, y=67, width=142, height=30)

# Pulsante cancella riga nella tabella del database
delete_button.place(x=660, y=316)

# Pulsante indietro (la finestra torna alla dimensione originaria)
indietro_button.place(x=360, y=316)


######-----TREEVIEW E DATABASE-----######

# Funzione per filtrare le righe in cui è presente la keyword inserita
def filter_by_keyword(entry, all_rows):
    keyword = entry.get().lower()

    if all_rows is not None:
        for item in tree.get_children():
            tree.delete(item)

        filtered_rows = [row for row in all_rows if any(keyword in str(value).lower() for value in row)]

        for row in filtered_rows:
            item_id = tree.insert('', 'end', values=row)

# Funzione che crea un database o si connette al database esistente, verifica se la table e' esistene o la crea,
# recupera i dati dalla tabella ordinandoli in base all'ID e li visualizza in un widget Treeview.
def database():
    global tree, all_rows 

    # Creazione del database o connessione al database se e' esistente
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    # Crea 'weather_data' table o verifica se esiste gia'
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                        date_of_today TEXT, 
                        city TEXT, 
                        weather TEXT, 
                        temperature REAL, 
                        temp_min REAL, 
                        temp_max REAL, 
                        humidity INTEGER, 
                        wind_speed REAL, 
                        direction_of_wind TEXT
                    )''')

    # Recupera tutte le righe dalla tabella in ordine decrescente in base a ID e memorizza nella variabile all_rows
    cursor.execute('SELECT * FROM weather_data ORDER BY ID DESC')
    all_rows = cursor.fetchall()
    conn.close()

    # Crea il widget Treeview
    tree = ttk.Treeview(finestra)

    # Defisce le colonne
    tree['columns'] = (
        'ID',
        'Data',
        'Citta',
        'Descrizione Meteo',
        'Temperatura',
        'Minima',
        'Massima',
        'Umidita',
        'Vento',
        'Direzione Vento'
    )

    # Formatta le colonne nelle rispettive larghezze
    tree.column('#0', width=0, stretch=NO)  # Hidden column for item IDs
    tree.column('ID', width=25, anchor=CENTER, stretch=NO)
    tree.column('Data', width=100, anchor=CENTER, stretch=NO)
    tree.column('Citta', width=80, anchor=CENTER, stretch=NO)
    tree.column('Descrizione Meteo', width=150, anchor=CENTER, stretch=NO)
    tree.column('Temperatura', width=100, anchor=CENTER, stretch=NO)
    tree.column('Minima', width=70, anchor=CENTER, stretch=NO)
    tree.column('Massima', width=80, anchor=CENTER, stretch=NO)
    tree.column('Umidita', width=70, anchor=CENTER, stretch=NO)
    tree.column('Vento', width=60, anchor=CENTER, stretch=NO)
    tree.column('Direzione Vento', width=180, anchor=CENTER, stretch=NO)

    # Imposta gli headings 
    tree.heading('ID', text='ID', anchor=CENTER)
    tree.heading('Data', text='Data', anchor=CENTER)
    tree.heading('Citta', text='Citta', anchor=CENTER)
    tree.heading('Descrizione Meteo', text='Descrizione Meteo', anchor=CENTER)
    tree.heading('Temperatura', text='Temperatura', anchor=CENTER)
    tree.heading('Minima', text='Minima', anchor=CENTER)
    tree.heading('Massima', text='Massima', anchor=CENTER)
    tree.heading('Umidita', text='Umidita', anchor=CENTER)
    tree.heading('Vento', text='Vento', anchor=CENTER)
    tree.heading('Direzione Vento', text='Direzione Vento', anchor=CENTER)

    # Inserisce i dati nel Treeview
    for row in all_rows:
        item_id = tree.insert('', 'end', values=row)

    # Aggiunge una barra di scorrimento verticale
    y_scrollbar = ttk.Scrollbar(tree, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=y_scrollbar.set)
    y_scrollbar.pack(side=RIGHT, fill=Y)

    # Aggiunge una barra di scorrimento orizzontale
    x_scrollbar = ttk.Scrollbar(tree, orient='horizontal', command=tree.xview)
    tree.configure(xscrollcommand=x_scrollbar.set)
    x_scrollbar.pack(side=BOTTOM, fill=X)

    # Posiziona il widget Treeview
    tree.place(x=360, y=109, width=360, height=180)
	
	  # Connette la funzione filter_by_keyword all'evento KeyRelease del the search box del database
    search_box_database.bind('<KeyRelease>', lambda event: filter_by_keyword(search_box_database, all_rows))

database()

finestra.mainloop()

# FINE DEL PROGRAMMA
