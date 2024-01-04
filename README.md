# Applicazione MeteoLive DB
## Esame di Basi di Dati 1 

##### Codice esame: 27667 

##### Matricola studente: 2941875

Progetto realizzato in Python

---

### Avvio dell' applicazione

Immagine dell'applicazione all'avvio.

![Come l'applicazione si presenta all'avvio](https://github.com/DamianSanremo/Media/blob/main/Screenshot_avvio.png)

### Ricerca meteo 

La ricerca del meteo avviene inserendo il nome della citta' cliccando sul riquadro "Inserisci citta'..."

![esempio ricerca meteo](https://github.com/DamianSanremo/Media/blob/main/Screenshot_particular_searchbox.png)

Una volta inserito il nome della città che si vuole cercare per la ricerca del meteo, basta cliccare sul pulsante con la lente d'ingrandimento.

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

Cliccando sull'icona 

![pulsante database](https://github.com/DamianSanremo/Media/blob/main/Screenshot_particular.png) 

L'applicazione permettera' di interagire con lo storico meteo, mostrandolo sotto forma di tabella in ordine decrescente per ID.

![Deattaglio Tabella del Database weather_data.db](https://github.com/DamianSanremo/Media/blob/main/Screenshot_expanded_1.png)

Posso interagire con la tabella inserendo una keyword.

La tabella mostrera' tutte le righe della tabella in cui e' contente la keyword inserita.

Ecco alcuni esempi: 

![keyword cielo coperto](https://github.com/DamianSanremo/Media/blob/main/Screenshot_Keyword_cielo_coperto.png)
![keyword nord-est](https://github.com/DamianSanremo/Media/blob/main/Screenshot_Keyword_nord-est.png)
 
### Gestione degli errori

Se il nome della citta' e' stato inserito in modo errato, l'applicazione mostra un pop-up segnalando un errore.

N.B: L'applicazione impedisce che l'errore venga trascritto e memorizzato nel database

![Errore nella ricerca](https://github.com/DamianSanremo/Media/blob/main/Screenshot_particular_error.png)

### Eliminare una riga (o record) presente nella tabella del database

L'applicazione permette di interagire con la tabella del database, permettendo di eliminare una o piu' righe.

 
