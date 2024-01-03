#####################################
#   APPLICAZIONE METEOLIVE DB       #
#                                   #   
# Studente:     Damian Dutka        #
# Matricola     2941875             #
# Esame:        BASI DI DATI 1      #
# Codice esame:                     #
#####################################

from tkinter import * 
from tkinter import ttk, messagebox
from datetime import datetime
import locale
import requests
import sqlite3
import io
import os  # Add this line to import the os module
from io import BytesIO
from urllib.request import urlopen
from PIL import Image, ImageTk


#Creo una finestra del programma di dimensioni 340x400 e fornisco un titolo al programma
finestra = Tk()
finestra.title("Applicazione MeteoLive DB")
finestra.geometry("340x400")

# Function to convert wind direction fetched from the API into cardinal points     
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

# Function to load the city image from the API and resize it accordingly
def load_city_image():
    city = city_search_box.get()
    #print("City:", city)  # Print the city for debugging
    # Unsplash access key
    access_key = 'Vxk_ofMGMVZibPzYhWdkXmMtNewaY0h4yq9UkB3p0NY'
    url = f'https://api.unsplash.com/photos/random?query={city}&order_by=popular&client_id={access_key}'

    # Fetch image data from the API
    response = requests.get(url)
    response.raise_for_status()
    image_data = response.json()
    image_url = image_data['urls']['regular']

    # Download the image
    image_response = requests.get(image_url)
    image_response.raise_for_status()

    # Open the image using PIL
    image = Image.open(BytesIO(image_response.content))

    # Calculate the corresponding height to maintain the original aspect ratio
    original_width, original_height = image.size
    target_width = 340
    target_height = int((target_width / original_width) * original_height)

    # Resize the image while maintaining the aspect ratio
    image = image.resize((target_width, target_height))

    # Convert PIL image to Tkinter PhotoImage
    pil_image = ImageTk.PhotoImage(image)

    # Update the label with the new image
    label_api_unsplash.config(image=pil_image)
    label_api_unsplash.image = pil_image  # Keep a reference to avoid garbage collection        
        
# Function to fetch data from API OpenWeather
def fetch_weather_data():
    # Take city input from the user and make sure the output has always the first letter uppercase
    city = city_search_box.get().capitalize()
    # Set date time to italian
    global today_date
    locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')
    today_date = datetime.now().strftime("%a, %d %B %Y").title()
    # Construct the API request URL and make the API request
    api_key = 'a0e78d3b449db7059df0a38abd3952f8'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}&lang=it'
    response = requests.get(url)
    # Check request successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract relevant data from json 
        weather = data['weather'][0]['description']
        weather_icon = data['weather'][0]['icon']
        icon_url = f'http://openweathermap.org/img/wn/{weather_icon}@2x.png'
        # Download the icon and display it directly
        icon_data = requests.get(icon_url).content
        # Convert the binary data to PhotoImage 
        global icon_image #rendo la variabile globale
        icon_image = ImageTk.PhotoImage(Image.open(BytesIO(icon_data)).resize((40, 40)))
        temperature = round(data['main']['temp'], 1)
        temp_min = round(data['main']['temp_min'], 1)
        temp_max = round(data['main']['temp_max'], 1)
        humidity = data['main']['humidity']
        wind_speed = round(data['wind']['speed'] * 3.6, 1)
        wind_direction = data['wind']['deg']
        direction_of_wind = get_wind_direction(wind_direction)

        # Format today's date as day-month-year to use into the database
        date_of_today = datetime.now().strftime("%d-%m-%Y")
        
        # Print the weather information FOR DEBUG
        print(f'Meteo di {city} del {date_of_today}')

    return date_of_today, city, weather, temperature, temp_min, temp_max, humidity, wind_speed, direction_of_wind

# Function to create and connect to a database table and store the data fetched from the API
def connect_and_store_in_database():
    date_of_today, city, weather, temperature, temp_min, temp_max, humidity, wind_speed, direction_of_wind = fetch_weather_data()

    # Print data before insertion for debugging
    print('Data before insertion into database:', date_of_today, city, weather, temperature, temp_min, temp_max,
          humidity, wind_speed, direction_of_wind)

    # Save data to SQLite database
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    try:
        sql_statement = '''
        INSERT INTO weather_data (date_of_today, city, weather, temperature, temp_min, temp_max, humidity, wind_speed, direction_of_wind)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        # Insert data into the table
        cursor.execute(sql_statement, (
        date_of_today, city, weather, temperature, temp_min, temp_max, humidity, wind_speed, direction_of_wind))

        # Commit changes
        conn.commit()
        update_labels()
    except Exception as e:
        print(f'Error during table creation/insertion: {e}')
    finally:
        # Close the connection in the 'finally' block to ensure it happens even if an exception occurs
        conn.close()
        database()


# Function to update the widget labels        
def update_labels():
    global today_date
    date_of_today, city, weather, temperature, temp_min, temp_max, humidity, wind_speed, direction_of_wind = fetch_weather_data()        
    # Update the label with the city name
    city_label.config(text=city)
    # Update the label with today date
    today_date_label.config(text=today_date)	
    # Update the label icon with weather icon       	
    icona_meteo_label.config(image=icon_image)	
    # Update the label with the weather description
    descrizione_meteo_label.config(text=weather)
    # Update the label with the temperature description
    temperatura_label.config(text=f"{temperature}°")
    # Update the label with the minimum temperature description
    temp_min_label.config(text=temp_min)
    # Update the label with the maximum temperature description
    temp_max_label.config(text=temp_max)
    # Update the label with the humidity description
    humidity_label.config(text=humidity)
    # Update the label with the wind speed description
    wind_speed_label.config(text=f"{wind_speed} KM / H")
    # Update the label with the wind direction description
    wind_direction_label.config(text=direction_of_wind)                    

# Function to search fetch data and load the city picture 
def search():
    connect_and_store_in_database()
    load_city_image()    
    
# Function to expand the window when pressed the button mostra_database 
def mostra_database():
    finestra.geometry('740x400')

# Function to resize the window at the original size
def indietro():
    finestra.geometry('340x400')    
    
# Function to place a placeholder text in the search_box that disappear on click
def placeholder(event):
    if city_search_box.get() == placeholder_text:
        city_search_box.delete(0, END)
        city_search_box.configure(show="")
        
# Define the delete_row function
def delete_row():
    selected_item = tree.selection()
    if selected_item:
        # Get the ID of the selected row
        selected_id = tree.item(selected_item, 'values')[0]

        # Connect to the SQLite database
        conn = sqlite3.connect('weather_data.db')
        cursor = conn.cursor()

        # Delete the record from the database based on the selected ID
        cursor.execute('DELETE FROM weather_data WHERE ID = ?', (selected_id,))
        conn.commit()

        # Close the connection
        conn.close()

        # Delete the selected item from the Treeview
        tree.delete(selected_item)

	    # Refresh the Treeview by calling the database function again
        database()            
        
		
##########-----WIDGET LABELS-----##########

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

##########-----POSIZIONE DEI LABELS-----##########

#Sfondo del programma
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


######-----TABELLA DEL DATABASE-----######

# Function who filter the rows where the typed keyword is present
def filter_by_keyword(entry, all_rows):
    keyword = entry.get().lower()

    if all_rows is not None:
        for item in tree.get_children():
            tree.delete(item)

        filtered_rows = [row for row in all_rows if any(keyword in str(value).lower() for value in row)]

        for row in filtered_rows:
            item_id = tree.insert('', 'end', values=row)

# Function to create a database and a table and order the row from the lastest by id
def database():
    global tree, all_rows  # Declare tree and all_rows as global variables

    # Connect to the SQLite database or create it if it doesn't exist
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    # Check if the 'weather_data' table exists, and create it if it doesn't
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

    # Fetch data from the table
    cursor.execute('SELECT * FROM weather_data ORDER BY ID DESC')
    all_rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Create a Treeview widget
    tree = ttk.Treeview(finestra)

    # Define columns
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

    # Format columns with individual widths
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

    # Set headings with individual text and anchor
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

    # Insert data into the Treeview
    for row in all_rows:
        item_id = tree.insert('', 'end', values=row)

    # Add vertical scrollbar
    y_scrollbar = ttk.Scrollbar(tree, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=y_scrollbar.set)
    y_scrollbar.pack(side=RIGHT, fill=Y)

    # Add horizontal scrollbar
    x_scrollbar = ttk.Scrollbar(tree, orient='horizontal', command=tree.xview)
    tree.configure(xscrollcommand=x_scrollbar.set)
    x_scrollbar.pack(side=BOTTOM, fill=X)

    # Pack the Treeview
    tree.place(x=360, y=109, width=360, height=180)
	
	# Connect the filter_by_keyword function to the KeyRelease event of the search box
    search_box_database.bind('<KeyRelease>', lambda event: filter_by_keyword(search_box_database, all_rows))

# Call the database function to initially populate the Treeview
database()

finestra.mainloop()




