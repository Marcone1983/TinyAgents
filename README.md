# TinyAgents - Micro-AI Powerhouse 🤖

Un bot Telegram rivoluzionario che fornisce accesso istantaneo a 10 agenti AI specializzati, con monetizzazione integrata tramite Stripe e gestione dei crediti su Supabase.

## 🚀 Caratteristiche Principali

### 10 Agenti AI Specializzati

1. **Meme Persona** - Trasforma idee in caption virali per meme
2. **Viral Pitch** - Scrivi pitch freddi per LinkedIn
3. **Roast Generator** - Genera battute divertenti
4. **Email Writer** - Scrivi email professionali
5. **Tweet Generator** - Crea tweet virali
6. **Product Description** - Descrizioni di prodotti per e-commerce
7. **Story Starter** - Genera inizi di storie affascinanti
8. **Code Explainer** - Spiega concetti di programmazione
9. **Motivational Quote** - Citazioni motivazionali personalizzate
10. **SEO Optimizer** - Ottimizza testi per i motori di ricerca

### Monetizzazione

- **Sistema di Crediti**: Ogni utilizzo costa 1 credito
- **Pagamenti Stripe**: Acquista crediti tramite Stripe
- **Database Supabase**: Gestione persistente dei crediti

### Mini App

- **Interfaccia Moderna**: Mini App con TMA SDK
- **Chat Interattiva**: Interfaccia grafica per chattare con gli agenti
- **Responsive Design**: Funziona perfettamente su mobile

## 📋 Configurazione Iniziale

### 1. Variabili d'Ambiente (Vercel)

Assicurati di aver impostato tutte le seguenti variabili d'ambiente nella dashboard di Vercel:

```
TELEGRAM_TOKEN=8271278686:AAHhcDkTK38Xpz5srRUviniJuYk7kAeBgGk
GROQ_API_KEY=<la_tua_chiave_groq>
SUPABASE_URL=<l_url_del_tuo_progetto_supabase>
SUPABASE_KEY=<la_tua_chiave_anonima_supabase>
STRIPE_SECRET_KEY=<la_tua_chiave_segreta_stripe>
STRIPE_PRODUCT_ID=<l_id_del_tuo_prodotto_stripe>
STRIPE_WEBHOOK_SECRET=<la_chiave_segreta_del_webhook_stripe>
```

### 2. Configurazione Supabase

1. Crea una tabella `users` con le seguenti colonne:
   - `id` (bigint, Primary Key): L'ID dell'utente Telegram
   - `credits` (integer, Default: 0): Il numero di crediti disponibili
   - `created_at` (timestamp, Default: now()): Data di creazione

### 3. Configurazione Stripe

1. Crea un Prodotto: "Pacchetto 100 Crediti Tiny Agents"
2. Crea un Prezzo: 9,99 € (una tantum)
3. Copia l'ID del Prezzo (`price_...`) e inseriscilo in `STRIPE_PRODUCT_ID`
4. Configura il Webhook di Stripe:
   - URL: `https://tiny-agents-ine6.vercel.app/api/stripe-webhook`
   - Evento: `checkout.session.completed`
   - Copia la chiave segreta e inseriscila in `STRIPE_WEBHOOK_SECRET`

### 4. Attivazione del Webhook di Telegram

Visita questo URL nel tuo browser (sostituisci l'URL con il tuo deployment Vercel):

```
https://api.telegram.org/bot8271278686:AAHhcDkTK38Xpz5srRUviniJuYk7kAeBgGk/setWebhook?url=https://tiny-agents-ine6.vercel.app/api/telegram
```

Se la risposta è `{"ok": true, "result": true}`, il webhook è stato impostato correttamente.

## 🎮 Come Usare il Bot

### Comandi Disponibili

- `/start` - Mostra il messaggio di benvenuto e la lista degli agenti
- `/credits` - Mostra il tuo saldo crediti attuale
- `/buy` - Acquista nuovi crediti tramite Stripe
- `/<agent_name> <prompt>` - Usa un agente specifico

### Esempio di Utilizzo

```
/meme_persona gatto che suona il pianoforte
```

Il bot risponderà con una caption virale per un meme.

## 📱 Mini App

Clicca sul pulsante "Apri app" nel menu del bot per accedere alla Mini App con un'interfaccia grafica moderna.

## 🔧 Struttura del Progetto

```
TinyAgents/
├── api/
│   ├── telegram.py          # Webhook del bot Telegram
│   └── stripe_webhook.py    # Webhook di Stripe
├── index.html               # Mini App (interfaccia grafica)
├── main.js                  # Logica della Mini App
├── vercel.json              # Configurazione di Vercel
├── requirements.txt         # Dipendenze Python
└── README.md                # Questo file
```

## 🚨 Troubleshooting

### Il bot non risponde ai comandi

1. Verifica che tutte le variabili d'ambiente siano impostate correttamente in Vercel.
2. Controlla che il Webhook di Telegram sia stato impostato correttamente.
3. Verifica che Supabase sia raggiungibile e che la tabella `users` esista.

### Errore 404 sul pulsante del menu

Questo errore è stato risolto. Se persiste, assicurati che il file `index.html` sia stato deployato correttamente su Vercel.

### I pagamenti non funzionano

1. Verifica che `STRIPE_SECRET_KEY` e `STRIPE_PRODUCT_ID` siano corretti.
2. Verifica che il Webhook di Stripe sia stato configurato correttamente.
3. Controlla i log di Stripe per eventuali errori.

## 📈 Monetizzazione

- **Prezzo**: 9,99 € per 100 crediti
- **Costo per Utilizzo**: 1 credito per agente
- **Margine**: Dipende dalla tua configurazione di Stripe

## 🎨 Personalizzazione

Puoi aggiungere nuovi agenti modificando il dizionario `AGENTS` nel file `api/telegram.py`:

```python
"my_agent": {
    "description": "Descrizione dell'agente",
    "system_prompt": "Prompt di sistema per l'LLM"
}
```

## 📞 Supporto

Per problemi o domande, contatta il team di TinyAgents.

---

**Versione**: 1.0.0  
**Ultimo Aggiornamento**: Novembre 2025
