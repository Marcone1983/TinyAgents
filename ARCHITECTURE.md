# Architettura di TinyAgents

Questo documento descrive l'architettura tecnica di TinyAgents e come i diversi componenti interagiscono tra loro.

## Panoramica dell'Architettura

```
┌─────────────────────────────────────────────────────────────────┐
│                        TELEGRAM USERS                            │
│                    (Client Telegram App)                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    Webhook (HTTP POST)
                           │
        ┌──────────────────▼──────────────────┐
        │     VERCEL SERVERLESS FUNCTIONS     │
        │                                      │
        │  ┌────────────────────────────────┐ │
        │  │   /api/telegram.py             │ │
        │  │   (Webhook Handler)            │ │
        │  │   - Processa messaggi Telegram │ │
        │  │   - Gestisce comandi           │ │
        │  │   - Chiama Groq API            │ │
        │  │   - Gestisce crediti           │ │
        │  │   - Crea sessioni Stripe       │ │
        │  └────────────────────────────────┘ │
        │                                      │
        │  ┌────────────────────────────────┐ │
        │  │   /api/stripe_webhook.py       │ │
        │  │   (Stripe Webhook Handler)     │ │
        │  │   - Riceve notifiche pagamento │ │
        │  │   - Aggiorna crediti           │ │
        │  └────────────────────────────────┘ │
        │                                      │
        │  ┌────────────────────────────────┐ │
        │  │   index.html + main.js         │ │
        │  │   (Mini App - TMA SDK)         │ │
        │  │   - Interfaccia grafica        │ │
        │  │   - Chat con agenti            │ │
        │  └────────────────────────────────┘ │
        └──────────────────┬──────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
    Groq API         Supabase API      Stripe API
        │                  │                  │
    ┌───▼────┐      ┌──────▼──────┐    ┌─────▼────┐
    │  Groq  │      │  Supabase   │    │  Stripe  │
    │  (LLM) │      │  (Database) │    │(Payments)│
    └────────┘      └─────────────┘    └──────────┘
```

## Componenti Principali

### 1. Webhook di Telegram (`/api/telegram.py`)

**Responsabilità:**
- Ricevere i messaggi da Telegram
- Parsare i comandi dell'utente
- Gestire la logica di routing dei comandi
- Chiamare gli agenti AI tramite Groq
- Gestire i crediti tramite Supabase
- Creare sessioni di pagamento tramite Stripe

**Flusso di Elaborazione:**

```
1. Ricevi messaggio da Telegram
   ↓
2. Estrai comando e parametri
   ↓
3. Verifica se è un comando noto
   ├─ /start → Mostra benvenuto
   ├─ /credits → Mostra saldo crediti
   ├─ /buy → Crea sessione Stripe
   └─ /<agent> → Esegui agente
   ↓
4. Se è un agente:
   ├─ Verifica crediti disponibili
   ├─ Decrementa crediti
   ├─ Chiama Groq API
   └─ Invia risposta a Telegram
   ↓
5. Invia risposta HTTP 200 a Telegram
```

### 2. Webhook di Stripe (`/api/stripe_webhook.py`)

**Responsabilità:**
- Ricevere le notifiche di pagamento da Stripe
- Verificare l'autenticità della notifica
- Aggiornare i crediti dell'utente su Supabase
- Notificare l'utente del pagamento completato

**Flusso di Elaborazione:**

```
1. Ricevi notifica da Stripe
   ↓
2. Verifica la firma della notifica
   ↓
3. Se è un evento checkout.session.completed:
   ├─ Estrai l'ID dell'utente Telegram
   ├─ Aggiungi 100 crediti all'utente
   └─ Invia notifica a Telegram
   ↓
4. Invia risposta HTTP 200 a Stripe
```

### 3. Mini App (TMA SDK)

**Responsabilità:**
- Fornire un'interfaccia grafica moderna
- Permettere agli utenti di selezionare gli agenti
- Gestire la chat con gli agenti
- Visualizzare i crediti disponibili

**Tecnologie:**
- HTML5 per la struttura
- CSS3 per lo styling
- JavaScript per la logica
- Telegram Web App SDK per l'integrazione

### 4. Database Supabase

**Tabella: `users`**

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,           -- ID dell'utente Telegram
    credits INTEGER DEFAULT 0,       -- Numero di crediti disponibili
    created_at TIMESTAMP DEFAULT NOW() -- Data di creazione
);
```

**Operazioni:**
- `get_user_credits(user_id)` - Recupera i crediti dell'utente
- `decrement_user_credits(user_id)` - Decrementa i crediti di 1
- `add_user_credits(user_id, amount)` - Aggiunge crediti all'utente

### 5. Agenti AI (Groq)

**Architettura degli Agenti:**

Ogni agente è definito da:
- **Nome**: Identificatore univoco (es. `meme_persona`)
- **Descrizione**: Descrizione breve per l'utente
- **System Prompt**: Istruzioni per l'LLM

**Esempio di Agente:**

```python
"meme_persona": {
    "description": "Trasforma una tua idea in una caption per un meme virale.",
    "system_prompt": "Sei un generatore di meme. Data un'idea, crea una caption breve, divertente e virale in stile meme..."
}
```

**Flusso di Esecuzione:**

```
1. Ricevi richiesta dell'utente
   ↓
2. Seleziona il system prompt dell'agente
   ↓
3. Chiama Groq API con:
   - System prompt
   - Messaggio dell'utente
   - Modello: llama3-8b-8192
   - Temperatura: 0.7
   - Max tokens: 150
   ↓
4. Ricevi risposta da Groq
   ↓
5. Invia risposta all'utente
```

### 6. Pagamenti Stripe

**Flusso di Pagamento:**

```
1. Utente invia /buy
   ↓
2. Bot crea sessione di checkout Stripe
   ├─ Prodotto: Pacchetto 100 Crediti
   ├─ Prezzo: 9,99 €
   ├─ Success URL: Link al bot
   └─ Cancel URL: Link al bot
   ↓
3. Utente viene reindirizzato a Stripe
   ↓
4. Utente completa il pagamento
   ↓
5. Stripe invia notifica al webhook
   ↓
6. Webhook aggiorna i crediti su Supabase
   ↓
7. Bot notifica l'utente del pagamento completato
```

## Flusso di Dati

### Flusso 1: Utilizzo di un Agente

```
Utente Telegram
    ↓
/meme_persona gatto che suona il pianoforte
    ↓
Vercel: /api/telegram.py
    ├─ Verifica crediti su Supabase
    ├─ Decrementa crediti su Supabase
    ├─ Chiama Groq API
    └─ Invia risposta a Telegram
    ↓
Utente Telegram riceve risposta
```

### Flusso 2: Acquisto di Crediti

```
Utente Telegram
    ↓
/buy
    ↓
Vercel: /api/telegram.py
    ├─ Crea sessione Stripe
    └─ Invia link di pagamento
    ↓
Utente clicca sul link
    ↓
Stripe Checkout
    ├─ Utente inserisce dati di pagamento
    └─ Pagamento completato
    ↓
Stripe invia notifica
    ↓
Vercel: /api/stripe_webhook.py
    ├─ Verifica notifica
    ├─ Aggiunge 100 crediti a Supabase
    └─ Notifica Telegram
    ↓
Utente Telegram riceve notifica di pagamento completato
```

## Sicurezza

### 1. Autenticazione Telegram

Tutti i webhook di Telegram includono un token nel header `Authorization`. Questo token viene verificato per assicurare che la richiesta proviene da Telegram.

### 2. Verifica della Firma di Stripe

Tutti i webhook di Stripe includono una firma nel header `Stripe-Signature`. Questa firma viene verificata per assicurare che la richiesta proviene da Stripe.

### 3. Variabili d'Ambiente

Tutte le chiavi API sensibili sono memorizzate in variabili d'ambiente su Vercel, non nel codice.

### 4. Row Level Security (RLS) di Supabase

È consigliato abilitare RLS su Supabase per limitare l'accesso ai dati dell'utente.

## Scalabilità

### Considerazioni di Scalabilità

1. **Vercel Serverless**: Scalabile automaticamente in base al carico
2. **Supabase**: Scalabile con il piano di pricing
3. **Stripe**: Gestisce milioni di transazioni
4. **Groq API**: Limite di rate (verificare la documentazione)

### Ottimizzazioni Consigliate

1. **Caching**: Implementare caching per le risposte degli agenti
2. **Rate Limiting**: Limitare il numero di richieste per utente
3. **Batch Processing**: Elaborare i pagamenti in batch
4. **Monitoring**: Implementare monitoraggio e logging

## Estensioni Future

1. **Database Persistente**: Aggiungere cronologia delle conversazioni
2. **Analytics**: Tracciare l'utilizzo degli agenti
3. **Referral Program**: Sistema di referral per gli utenti
4. **Admin Dashboard**: Dashboard per la gestione dei dati
5. **Multi-Lingua**: Supporto per più lingue
6. **Agenti Personalizzati**: Permettere agli utenti di creare agenti personalizzati

---

**Versione**: 1.0.0  
**Ultimo Aggiornamento**: Novembre 2025
