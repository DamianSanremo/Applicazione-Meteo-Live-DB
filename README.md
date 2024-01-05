# Applicazione MeteoLive DB
## Esame di Basi di Dati 1 

#### Codice esame: 27667 

#### Matricola studente: 2941875

Progetto realizzato in Python

##### ---> [CLICCA QUI](https://github.com/DamianSanremo/Applicazione-Meteo-Live-DB/blob/main/Applicazione%20MeteoLive%20DB.zip) <--- PER SCARICARE il file .zip del progetto.

##### Versione alternativa: ---> [CLICCA QUI]() <--- Se scaricare la versione del progetto con gia' all'interno il file 'weather_data.db'  

---

### Demo video dell'applicazione

<video src='https://github.com/DamianSanremo/Media/blob/main/Demo_App_video.mp4' width=90/>

---

### Avvio dell' applicazione

Immagine dell'applicazione all'avvio.

![Come l'applicazione si presenta all'avvio](https://github.com/DamianSanremo/Media/blob/main/Screenshot_avvio.png)

### Ricerca meteo 

La ricerca del meteo avviene inserendo il nome della citta' cliccando sul riquadro "Inserisci citta'..."

![esempio ricerca meteo](https://github.com/DamianSanremo/Media/blob/main/Screenshot_particular_searchbox.png)

Una volta inserito il nome della città che si vuole cercare per la ricerca del meteo, basta cliccare sul pulsante con la lente d'ingrandimento, come indicato dalla freccia rossa.

![inserisci nome citta' e clicca sul pulsante](https://github.com/DamianSanremo/Media/blob/main/Screenshot_particular_searchbox2.png) 

L'applicazione mostrera' i dati metereologici in tempo reale forniti dall'API di OpenWeather. 

Aggiornera' rispetto ai dati di default: la data (di oggi), il nome della citta' cercata, temperatura, icona e descrizione meteo, massima e minina, umidita', vento e direzione.

Inoltre l'applicazione aggiornera' l'immagine di default (Porto di Genova) sostituendola con l'immagine fornita dall'API di Unsplash. 

Alcuni esempi delle ricerche effettuate:

![Parigi](https://github.com/DamianSanremo/Media/blob/main/Screenshot_4.png)
![Varsavia](https://github.com/DamianSanremo/Media/blob/main/Screenshot_5.png)
![Roma](https://github.com/DamianSanremo/Media/blob/main/Screenshot_7.png)
![Washington](https://github.com/DamianSanremo/Media/blob/main/Screenshot_8.png)

### Interazione con il Database 

Cliccando sull'icona, la finestra dell'applicazione si ingrandira'. 

![pulsante database](https://github.com/DamianSanremo/Media/blob/main/Screenshot_particular.png) 

L'applicazione permettera' di interagire con lo storico meteo, mostrandolo sotto forma di tabella in ordine decrescente per ID.

La tabella visualizza rispettivamente le colonne: ID, data, citta', descrizione meteo, temperatura, minima, massima, umidita', vento, direzione vento. 

![Deattaglio Tabella del Database weather_data.db](https://github.com/DamianSanremo/Media/blob/main/Screenshot_expanded_1.png)

Posso interagire con la tabella inserendo una keyword.

La tabella mostrera' tutte le righe della tabella in cui e' contente la keyword inserita.

Ecco alcuni esempi: 

![keyword cielo coperto](https://github.com/DamianSanremo/Media/blob/main/Screenshot_Keyword_cielo_coperto.png)
![keyword nord-est](https://github.com/DamianSanremo/Media/blob/main/Screenshot_Keyword_nord-est.png)
 
### Gestione degli errori

Se il nome della citta' e' stato inserito in modo errato, l'applicazione mostra un pop-up segnalando un errore.

N.B: L'applicazione impedisce che l'errore venga trascritto e memorizzato nel database.

![Errore nella ricerca](https://github.com/DamianSanremo/Media/blob/main/Screenshot_particular_error.png)

### Eliminare una riga (o record) presente nella tabella del database

L'applicazione permette di interagire con la tabella del database, permettendo di eliminare una o piu' righe.

Selezionando una riga della tabella e cliccando sul pulsante indicato dalla freccia rossa (seleziono la riga con ID 80).

![Seleziono la riga della tabella da eliminare](https://github.com/DamianSanremo/Media/blob/main/screenshot_particular_delete.png)

L'applicazione elimina la riga della tabella corrispondente all'ID 80, aggiorna la tabella e mostra che la riga con ID 80 e' stata eliminata dalla tabella del database.

![La riga della tabella e' stata eliminata](https://github.com/DamianSanremo/Media/blob/main/screenshot_particular_delete_id80.png)

La stessa operazione e' possibile farla aiutandosi con una keyword (nell'esempio la keyword Roma).

![Elimino la riga della tabella del database aiutandomi con la keyword](https://github.com/DamianSanremo/Media/blob/main/screenshot_particular_delete2.png)

### Nascondere la tabella del database e ridimensionamento

L'applicazione tramite il pulsante indietro indicato dalla freccia rossa, permette di nascondere la tabella del database, ridimensionando la finestra alla dimensione originaria.

Prima

![Pulsante indietro nasconde la tabella del database](https://github.com/DamianSanremo/Media/blob/main/screenshot_particular_indietro.png)

Dopo 

![Finestra dell'applicazione ridimensionata alla dimensione originaria](https://github.com/DamianSanremo/Media/blob/main/screenshot_particular_indietro2.png) 

---

### Dettagli sul codice: i comandi SQL

L'applicazione, come menzionato in precedenza, utilizza una libreria SQLite, in quanto gia' presente in Python (e quindi non richiede l'installazione di ulteriori librerie) 
al fine di creare un file "weather_data.db" e una table "weather_data" al suo interno.

#### Creazione della tabella e ordine delle righe in modo decrescente in base all'ID

![Comandi SQL creazione tabellla e ordine secondo ID decrescente](https://github.com/DamianSanremo/Media/blob/main/screenshot_sql1.png)

Viene eseguito un primo comando SQL per creare la tabella 'weather_data' nel database SQLite (se non presente).

La tabella contiene le seguenti colonne: 'ID', 'date_of_today', 'city', 'weather', 'temperature', 'temp_min', 'temp_max', 'humidity', 'wind_speed', 'direction_of_wind'. 

L'ID è una chiave primaria che si auto-incrementa.

Il secondo comando SQL esegue una query di selezione (SELECT) per recuperare tutte le colonne (*) dalla tabella 'weather_data'. 
"ORDER BY ID DESC" ordina i record in modo decrescente in base alla colonna 'ID'. 

I risultati della query, che includono tutti i dati delle colonne per ciascuna riga, vengono quindi recuperati utilizzando cursor.fetchall() e memorizzati nella variabile all_rows.

#### Inserimento dei dati nella tabella del database

![Comando SQL per inserimento dati](https://github.com/DamianSanremo/Media/blob/main/screenshot_sql2.png) 

Questo comando SQL viene utilizzato per inserire nuovi dati nella tabella 'weather_data'.

Python, attraverso il comando cursor.execute(), fornisce i valori come parametri al comando SQL per eseguire l'inserimento dei dati nella tabella.

#### Cancellazione della riga (o record) della tabella del database

![Comando SQL per cancellare una riga della tabella](https://github.com/DamianSanremo/Media/blob/main/screenshot_sql3.png)

Questo comando SQL viene eseguito per eliminare dalla tabella 'weather_data' la riga in cui il valore della colonna 'ID' corrisponde a selected_id.

Utilizzando "conn.commit()" e "conn.close()" della libreria SQLite di Python si confermano e applicano le modifiche effettuate al database e si chiude la connessione ad esso.

---

### Note aggiuntive e conclusive sull'applicazione

Il programma si basa sulle seguenti librerie: 

![Librerie utilizzate dall'applicazione](https://github.com/DamianSanremo/Media/blob/main/screenshot_libraries.png)

Per la libreria PIL (Pillow) non presente nell'installazione di Python, puo' essere installata digitando:

Linux / MacOS
```bash
pip --version
pip install Pillow

```
oppure su Windows nel prompt dei comandi o nel Powershell

```bash
python -m pip --version
python -m pip install Pillow
```

N.B: In questo modo verifico, per precauzione, anche se e' installata la libreria PIP e a quale versione.
