# Troubleshooting - TinyAgents

Questa guida fornisce soluzioni ai problemi comuni che potresti incontrare durante l'uso di TinyAgents.

## Il Bot Non Risponde ai Comandi

### Sintomi
- Invii `/start` ma il bot non risponde
- Invii un comando di agente ma il bot rimane silenzioso

### Possibili Cause e Soluzioni

**Causa 1: Webhook di Telegram non impostato correttamente**

1. Verifica che il webhook sia stato impostato visitando:
   ```
   https://api.telegram.org/bot<TELEGRAM_TOKEN>/getWebhookInfo
   ```
2. Se la risposta contiene `"url": ""` o un errore, il webhook non è impostato.
3. Imposta il webhook nuovamente visitando:
   ```
   https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=https://tiny-agents-ine6.vercel.app/api/telegram
   ```

**Causa 2: Variabili d'ambiente non configurate**

1. Vai alla dashboard di Vercel
2. Verifica che tutte le variabili d'ambiente siano impostate:
   - `TELEGRAM_TOKEN`
   - `GROQ_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `STRIPE_SECRET_KEY`
   - `STRIPE_PRODUCT_ID`
   - `STRIPE_WEBHOOK_SECRET`
3. Se una variabile è vuota, il bot non funzionerà
4. Dopo aver aggiunto le variabili, esegui un "Redeploy" in Vercel

**Causa 3: Errore nel codice Python**

1. Controlla i log di Vercel:
   - Vai a Vercel Dashboard → Deployments → Seleziona l'ultimo deployment → Logs
2. Se vedi errori di Python, potrebbero essere dovuti a:
   - Importazioni mancanti (installa le dipendenze con `pip install -r requirements.txt`)
   - Errori di sintassi nel codice
   - Chiavi API non valide

**Soluzione Rapida:**

Prova a inviare un messaggio di testo generico al bot (non un comando). Se il bot non risponde nemmeno a questo, il webhook potrebbe non essere impostato correttamente.

---

## Errore 404 sulla Mini App

### Sintomi
- Clicchi sul pulsante "Apri app" e vedi un errore 404
- La Mini App non si carica

### Possibili Cause e Soluzioni

**Causa 1: URL della Mini App non configurato in BotFather**

1. Vai a BotFather (@BotFather)
2. Invia `/mybots` e seleziona **TinyAgents_bot**
3. Clicca su **"Bot Settings"** → **"Menu Button"** → **"Configure menu button"**
4. Verifica che l'URL sia impostato correttamente:
   ```
   https://tiny-agents-ine6.vercel.app
   ```
5. Se non è impostato, aggiungilo ora

**Causa 2: File index.html non deployato su Vercel**

1. Verifica che il file `index.html` sia nel repository GitHub
2. Controlla che il file sia stato incluso nell'ultimo commit
3. Vai a Vercel e verifica che il deployment sia completato con successo
4. Se il deployment è fallito, controlla i log per gli errori

**Causa 3: URL di Vercel errato**

1. Vai a Vercel Dashboard → Seleziona il progetto TinyAgents
2. Copia l'URL corretto del deployment (es. `https://tiny-agents-ine6.vercel.app`)
3. Assicurati che l'URL non contenga path aggiuntivi (es. `/api/telegram`)
4. Aggiorna l'URL in BotFather

**Soluzione Rapida:**

Visita direttamente l'URL nel browser (es. `https://tiny-agents-ine6.vercel.app`). Se vedi la Mini App, il problema è nella configurazione di BotFather. Se vedi un errore 404, il problema è nel deployment di Vercel.

---

## I Crediti Non Vengono Decrementati

### Sintomi
- Usi un agente ma i crediti rimangono uguali
- Vedi il messaggio "Credito utilizzato" ma i crediti non cambiano

### Possibili Cause e Soluzioni

**Causa 1: Supabase non configurato correttamente**

1. Vai a Supabase Dashboard
2. Verifica che la tabella `users` esista
3. Verifica che le colonne siano corrette:
   - `id` (bigint, Primary Key)
   - `credits` (integer, Default: 0)
   - `created_at` (timestamp, Default: now())
4. Se la tabella non esiste, creala manualmente

**Causa 2: Chiavi Supabase non valide**

1. Vai a Supabase Dashboard → Settings → API
2. Copia l'URL del progetto e la chiave Anonima (Public Anon Key)
3. Verifica che siano uguali a quelle in Vercel
4. Se sono diverse, aggiorna le variabili d'ambiente in Vercel e esegui un Redeploy

**Causa 3: Errore nel codice di decremento**

1. Controlla i log di Vercel per eventuali errori
2. Se vedi un errore di Supabase, potrebbe essere dovuto a:
   - Chiavi non valide
   - Tabella non trovata
   - Row Level Security (RLS) troppo restrittivo

**Soluzione Rapida:**

Invia il comando `/credits` al bot. Se vedi il tuo saldo crediti, Supabase è configurato correttamente. Se vedi un errore, il problema è nella configurazione di Supabase.

---

## I Pagamenti Non Funzionano

### Sintomi
- Clicchi su `/buy` ma il link di pagamento non funziona
- Il link di pagamento è raggiungibile ma il pagamento fallisce
- Dopo il pagamento, i crediti non vengono aggiunti

### Possibili Cause e Soluzioni

**Causa 1: Stripe non configurato correttamente**

1. Vai a Stripe Dashboard → Developers → API Keys
2. Copia la chiave segreta (Secret Key) - inizia con `sk_`
3. Verifica che sia uguale a `STRIPE_SECRET_KEY` in Vercel
4. Se è diversa, aggiorna la variabile d'ambiente e esegui un Redeploy

**Causa 2: Prodotto/Prezzo di Stripe non valido**

1. Vai a Stripe Dashboard → Products
2. Verifica che il prodotto "Pacchetto 100 Crediti Tiny Agents" esista
3. Verifica che abbia un prezzo di 9,99 € (una tantum)
4. Copia l'ID del Prezzo (inizia con `price_`)
5. Verifica che sia uguale a `STRIPE_PRODUCT_ID` in Vercel
6. Se è diverso, aggiorna la variabile d'ambiente e esegui un Redeploy

**Causa 3: Webhook di Stripe non configurato**

1. Vai a Stripe Dashboard → Developers → Webhooks
2. Verifica che esista un webhook con l'URL:
   ```
   https://tiny-agents-ine6.vercel.app/api/stripe-webhook
   ```
3. Verifica che l'evento `checkout.session.completed` sia selezionato
4. Se il webhook non esiste, crealo manualmente
5. Copia la chiave segreta del webhook (inizia con `whsec_`)
6. Verifica che sia uguale a `STRIPE_WEBHOOK_SECRET` in Vercel
7. Se è diversa, aggiorna la variabile d'ambiente e esegui un Redeploy

**Causa 4: Errore nel codice di pagamento**

1. Controlla i log di Vercel per eventuali errori
2. Se vedi un errore di Stripe, potrebbe essere dovuto a:
   - Chiavi non valide
   - Prodotto/Prezzo non trovato
   - Webhook non configurato

**Soluzione Rapida:**

Prova a completare un pagamento di test su Stripe. Se il pagamento va a buon fine ma i crediti non vengono aggiunti, il problema è nel webhook di Stripe. Controlla i log di Stripe per eventuali errori.

---

## La Mini App Non Carica i Crediti

### Sintomi
- La Mini App mostra "Crediti Disponibili: 0" anche se hai crediti
- I crediti non si aggiornano dopo un pagamento

### Possibili Cause e Soluzioni

**Causa 1: API non implementata nella Mini App**

La Mini App attuale è una versione di base che non chiama l'API per caricare i crediti. Questa è una limitazione intenzionale per semplicità.

**Soluzione:**

Per implementare il caricamento dei crediti nella Mini App:

1. Modifica il file `main.js`
2. Aggiungi una funzione per chiamare l'API del bot:
   ```javascript
   async function loadCredits() {
       const userId = tg.initDataUnsafe?.user?.id;
       // Chiama l'API per ottenere i crediti
       // Aggiorna il DOM con i crediti
   }
   ```
3. Chiama questa funzione al caricamento della Mini App

---

## Errore: "Configurazione incompleta"

### Sintomi
- Il bot risponde con un errore JSON che dice "Configurazione incompleta"
- L'errore specifica quali variabili d'ambiente mancano

### Soluzione

Questo errore significa che una o più variabili d'ambiente non sono configurate in Vercel.

1. Vai a Vercel Dashboard → Seleziona il progetto TinyAgents
2. Vai a Settings → Environment Variables
3. Aggiungi le variabili mancanti (come indicato nell'errore)
4. Esegui un Redeploy

---

## Errore: "Impossibile inizializzare Groq client"

### Sintomi
- Il bot risponde con un errore che dice "Servizio AI non disponibile"
- I comandi degli agenti non funzionano

### Soluzione

Questo errore significa che la chiave API di Groq non è valida o non è configurata.

1. Vai a Groq Console (https://console.groq.com)
2. Verifica che la chiave API sia valida
3. Copia la chiave API
4. Vai a Vercel e aggiorna la variabile `GROQ_API_KEY`
5. Esegui un Redeploy

---

## Errore: "Impossibile inizializzare Supabase client"

### Sintomi
- Il bot risponde con un errore che dice "Errore nel caricamento dei crediti"
- I comandi `/credits` e `/buy` non funzionano

### Soluzione

Questo errore significa che le chiavi di Supabase non sono valide o non sono configurate.

1. Vai a Supabase Dashboard → Settings → API
2. Verifica che l'URL del progetto e la chiave Anonima siano validi
3. Copia l'URL e la chiave
4. Vai a Vercel e aggiorna le variabili `SUPABASE_URL` e `SUPABASE_KEY`
5. Esegui un Redeploy

---

## Contatti e Supporto

Se il tuo problema non è elencato qui, contatta il team di TinyAgents per assistenza.

**Email**: support@tinyagents.com  
**Telegram**: @TinyAgents_Support

---

**Versione**: 1.0.0  
**Ultimo Aggiornamento**: Novembre 2025
