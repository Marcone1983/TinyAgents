# Configurazione della Mini App in BotFather

Questa guida ti aiuterà a configurare la Mini App di TinyAgents in BotFather.

## Passaggi

### 1. Apri BotFather

Invia il comando `/start` a [@BotFather](https://t.me/BotFather) su Telegram.

### 2. Seleziona il Tuo Bot

Invia il comando `/mybots` e seleziona **TinyAgents_bot** dalla lista.

### 3. Configura il Pulsante del Menu

1. Clicca su **"Bot Settings"**.
2. Clicca su **"Menu Button"**.
3. Clicca su **"Configure menu button"**.
4. Inserisci l'URL della Mini App:
   ```
   https://tiny-agents-ine6.vercel.app
   ```
   (Sostituisci `tiny-agents-ine6.vercel.app` con l'URL del tuo deployment Vercel)

### 4. Verifica la Configurazione

1. Vai su Telegram e apri il bot **TinyAgents_bot**.
2. Dovresti vedere un pulsante **"Apri app"** nel menu.
3. Clicca su **"Apri app"** per aprire la Mini App.

## Risoluzione dei Problemi

### Il pulsante "Apri app" non appare

1. Assicurati di aver configurato il pulsante del menu in BotFather.
2. Riavvia Telegram.
3. Prova a inviare `/start` al bot di nuovo.

### La Mini App mostra errore 404

1. Verifica che l'URL del deployment Vercel sia corretto.
2. Assicurati che il file `index.html` sia stato deployato su Vercel.
3. Visita l'URL nel browser per verificare che sia raggiungibile.

### La Mini App non funziona correttamente

1. Apri la console del browser (F12) e controlla gli errori.
2. Verifica che il file `main.js` sia stato caricato correttamente.
3. Assicurati che il Telegram Web App SDK sia caricato.

## Personalizzazione

Puoi personalizzare l'interfaccia della Mini App modificando i file:

- `index.html` - Struttura HTML e stili CSS
- `main.js` - Logica JavaScript e interazioni

## Supporto

Per problemi o domande, contatta il team di TinyAgents.
