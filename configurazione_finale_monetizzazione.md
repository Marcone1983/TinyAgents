# Configurazione Finale della Monetizzazione (Stripe e Supabase)

Il codice del tuo progetto "Tiny Agents" è stato aggiornato per includere la gestione dei crediti tramite Supabase e il flusso di pagamento tramite Stripe.

**Questa fase richiede la tua azione per configurare i servizi esterni e le variabili d'ambiente su Vercel.**

## 1. Configurazione di Supabase (Database Crediti)

### 1.1. Creazione della Tabella `users`

Accedi alla tua dashboard di Supabase e crea una nuova tabella chiamata `users` con le seguenti colonne:

| Nome Colonna | Tipo di Dato | Proprietà | Descrizione |
| :--- | :--- | :--- | :--- |
| `id` | `bigint` | Primary Key, Non-Nullable | L'ID univoco dell'utente Telegram. |
| `credits` | `integer` | Default: 0, Non-Nullable | Il numero di esecuzioni rimanenti. |
| `created_at` | `timestamp with time zone` | Default: `now()`, Non-Nullable | Data di creazione del record. |

### 1.2. Variabili d'Ambiente Supabase

Dalla sezione "Settings" -> "API" di Supabase, recupera i seguenti valori e aggiungili come **Environment Variables** al tuo progetto Vercel:

| Nome Variabile | Valore | Descrizione |
| :--- | :--- | :--- |
| `SUPABASE_URL` | L'URL del tuo progetto Supabase (es. `https://xxxx.supabase.co`). |
| `SUPABASE_KEY` | La chiave **Anonima (Public Anon Key)** di Supabase. |

## 2. Configurazione di Stripe (Pagamenti)

### 2.1. Creazione del Prodotto e del Prezzo

1.  **Crea un Prodotto:** Nella dashboard di Stripe, crea un prodotto (es. "Pacchetto 100 Crediti").
2.  **Crea un Prezzo:** Associa un prezzo a questo prodotto (es. 9.99€).
3.  **Salva l'ID del Prezzo:** Stripe ti fornirà un ID del prezzo (inizia con `price_...`).

### 2.2. Configurazione del Webhook

1.  **Crea un Webhook Endpoint:** Nella sezione "Sviluppatori" -> "Webhook" di Stripe, aggiungi un nuovo endpoint.
2.  **URL del Webhook:** L'URL del tuo webhook su Vercel sarà: `https://<NOME_DEL_TUO_PROGETTO>.vercel.app/api/stripe-webhook`
3.  **Eventi da Ascoltare:** Seleziona solo l'evento `checkout.session.completed`.
4.  **Salva la Chiave Segreta:** Stripe ti fornirà la **Webhook Secret** (inizia con `whsec_...`).

### 2.3. Variabili d'Ambiente Stripe

Aggiungi le seguenti variabili al tuo progetto Vercel:

| Nome Variabile | Valore | Descrizione |
| :--- | :--- | :--- |
| `STRIPE_SECRET_KEY` | La tua chiave segreta di Stripe (inizia con `sk_live_...` o `sk_test_...`). |
| `STRIPE_PRODUCT_ID` | L'ID del **Prezzo** che hai creato (inizia con `price_...`). |
| `STRIPE_WEBHOOK_SECRET` | La chiave segreta del Webhook di Stripe (inizia con `whsec_...`). |

## 3. Deployment Finale

1.  **Carica il Codice Aggiornato su GitHub:**
    Assicurati di aver caricato su GitHub i file aggiornati:
    *   `requirements.txt`
    *   `vercel.json`
    *   `api/telegram.py`
    *   `api/stripe_webhook.py`

    ```bash
    git add .
    git commit -m "Feature: Added Stripe monetization and Supabase credit management"
    git push origin main
    ```

2.  **Deployment su Vercel:**
    Vercel rileverà i cambiamenti e avvierà un nuovo deployment. Assicurati che tutte le **Environment Variables** siano state aggiunte prima del deployment.

Una volta completato il deployment e configurati i servizi esterni, il tuo bot sarà completamente monetizzato!
