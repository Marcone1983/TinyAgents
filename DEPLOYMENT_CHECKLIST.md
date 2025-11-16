# Deployment Checklist - TinyAgents

Usa questa checklist per assicurarti che tutto sia configurato correttamente prima di lanciare il bot.

## ✅ Configurazione Telegram

- [ ] Bot creato su BotFather (@BotFather)
- [ ] Token del bot salvato (es. `8271278686:AAHhcDkTK38Xpz5srRUviniJuYk7kAeBgGk`)
- [ ] Comandi configurati in BotFather:
  - [ ] `/start` - Avvia il bot
  - [ ] `/credits` - Mostra i crediti
  - [ ] `/buy` - Acquista crediti
  - [ ] `/meme_persona` - Agente meme
  - [ ] `/viral_pitch` - Agente pitch
  - [ ] `/roast_generator` - Agente roast
  - [ ] `/email_writer` - Agente email
  - [ ] `/tweet_generator` - Agente tweet
  - [ ] `/product_description` - Agente prodotto
  - [ ] `/story_starter` - Agente storia
  - [ ] `/code_explainer` - Agente codice
  - [ ] `/motivational_quote` - Agente motivazione
  - [ ] `/seo_optimizer` - Agente SEO
- [ ] Logo impostato in BotFather
- [ ] Descrizione impostata in BotFather
- [ ] Pulsante del menu configurato (Mini App)

## ✅ Configurazione Groq

- [ ] Account Groq creato (https://console.groq.com)
- [ ] Chiave API Groq generata
- [ ] Chiave API salvata come `GROQ_API_KEY` in Vercel

## ✅ Configurazione Supabase

- [ ] Progetto Supabase creato (https://supabase.com)
- [ ] Tabella `users` creata con le colonne:
  - [ ] `id` (bigint, Primary Key)
  - [ ] `credits` (integer, Default: 0)
  - [ ] `created_at` (timestamp, Default: now())
- [ ] URL del progetto Supabase salvato come `SUPABASE_URL` in Vercel
- [ ] Chiave Anonima (Public Anon Key) salvata come `SUPABASE_KEY` in Vercel
- [ ] Row Level Security (RLS) configurato (opzionale, ma consigliato)

## ✅ Configurazione Stripe

- [ ] Account Stripe creato (https://stripe.com)
- [ ] Prodotto "Pacchetto 100 Crediti Tiny Agents" creato
- [ ] Prezzo 9,99 € (una tantum) creato
- [ ] ID del Prezzo (`price_...`) salvato come `STRIPE_PRODUCT_ID` in Vercel
- [ ] Chiave segreta di Stripe salvata come `STRIPE_SECRET_KEY` in Vercel
- [ ] Webhook di Stripe configurato:
  - [ ] URL: `https://tiny-agents-ine6.vercel.app/api/stripe-webhook`
  - [ ] Evento: `checkout.session.completed`
  - [ ] Chiave segreta del webhook salvata come `STRIPE_WEBHOOK_SECRET` in Vercel

## ✅ Configurazione Vercel

- [ ] Progetto Vercel creato (https://vercel.com)
- [ ] Repository GitHub collegato a Vercel
- [ ] Tutte le variabili d'ambiente impostate:
  - [ ] `TELEGRAM_TOKEN`
  - [ ] `GROQ_API_KEY`
  - [ ] `SUPABASE_URL`
  - [ ] `SUPABASE_KEY`
  - [ ] `STRIPE_SECRET_KEY`
  - [ ] `STRIPE_PRODUCT_ID`
  - [ ] `STRIPE_WEBHOOK_SECRET`
- [ ] Deployment completato con successo
- [ ] URL del deployment copiato (es. `https://tiny-agents-ine6.vercel.app`)

## ✅ Configurazione Webhook

- [ ] Webhook di Telegram impostato visitando:
  ```
  https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=<VERCEL_URL>/api/telegram
  ```
  - [ ] Risposta: `{"ok": true, "result": true}`
- [ ] Webhook di Stripe configurato in Stripe Dashboard

## ✅ Test Funzionali

### Test del Bot Telegram

1. [ ] Invia `/start` al bot
   - [ ] Il bot risponde con il messaggio di benvenuto
   - [ ] La lista degli agenti è visibile

2. [ ] Invia `/credits`
   - [ ] Il bot risponde con il saldo crediti (dovrebbe essere 0 per un nuovo utente)

3. [ ] Invia `/meme_persona gatto che suona il pianoforte`
   - [ ] Il bot risponde con una caption virale per un meme
   - [ ] I crediti vengono decrementati

4. [ ] Invia `/buy`
   - [ ] Il bot fornisce un link di pagamento Stripe
   - [ ] Il link è raggiungibile e funziona

### Test della Mini App

1. [ ] Apri il bot su Telegram
2. [ ] Clicca sul pulsante "Apri app"
   - [ ] La Mini App si apre senza errori 404
   - [ ] L'interfaccia è visibile e responsive
   - [ ] I crediti sono visualizzati correttamente

3. [ ] Seleziona un agente dalla Mini App
   - [ ] La chat si apre
   - [ ] Puoi scrivere un messaggio

### Test della Monetizzazione

1. [ ] Completa un pagamento su Stripe
   - [ ] Il pagamento va a buon fine
   - [ ] Ricevi un'email di conferma da Stripe

2. [ ] Verifica i crediti dopo il pagamento
   - [ ] Invia `/credits` al bot
   - [ ] I crediti dovrebbero essere aumentati (es. 100)

## ✅ Ottimizzazione e Sicurezza

- [ ] Tutti i secret sono salvati in variabili d'ambiente (non nel codice)
- [ ] Il file `.env.example` è stato creato (senza valori sensibili)
- [ ] Il file `.gitignore` esclude i file sensibili
- [ ] I log di errore sono configurati (opzionale)
- [ ] La documentazione è completa e aggiornata

## ✅ Lancio Finale

- [ ] Tutti i test sono passati
- [ ] Il bot è pronto per il pubblico
- [ ] Un messaggio di benvenuto è stato inviato ai primi utenti
- [ ] Il supporto è disponibile per gli utenti

## 🚀 Lancio!

Se hai completato tutti i passaggi della checklist, il tuo bot TinyAgents è pronto per il lancio!

---

**Nota**: Se riscontri problemi durante il deployment, consulta il file `README.md` per la risoluzione dei problemi.
