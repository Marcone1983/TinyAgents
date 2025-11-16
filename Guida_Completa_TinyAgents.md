# Guida Completa alla Creazione e al Deployment di "Tiny Agents"

**Autore:** Manus AI
**Data:** 16 Novembre 2025

## Introduzione al Progetto "Tiny Agents"

Il progetto "Tiny Agents" rappresenta un'applicazione moderna e scalabile che sfrutta l'integrazione tra l'ecosistema Telegram e le capacità dei Large Language Models (LLM) per offrire micro-servizi specializzati. L'obiettivo è creare un prodotto minimo funzionante (MVP) in grado di generare contenuti specifici e di alta qualità su richiesta.

Lo stack tecnologico selezionato è ottimizzato per l'efficienza, la scalabilità e la riduzione dei costi operativi, sfruttando l'architettura **Serverless** su Vercel.

| Componente | Tecnologia | Ruolo nel Progetto |
| :--- | :--- | :--- |
| **Frontend/Hosting** | Vercel | Hosting per le funzioni Serverless e per l'eventuale Landing Page. |
| **Backend** | Python (Serverless Functions) | Gestione del Webhook di Telegram e logica di routing dei comandi. |
| **LLM Engine** | Groq API (Llama 3) | Fornitura di risposte veloci e intelligenti per gli agenti. |
| **Interfaccia Utente** | Telegram Bot API | Piattaforma di interazione con l'utente. |
| **Controllo Versione** | GitHub | Gestione del codice sorgente e integrazione continua con Vercel. |

---

## Fase 1: Preparazione dell'Ambiente e degli Account

Prima di procedere con il codice, è fondamentale configurare gli account necessari e ottenere le chiavi API.

### 1.1. Configurazione del Bot Telegram

1.  **Crea il Bot:** Apri Telegram e cerca `BotFather`.
2.  Invia il comando `/newbot` e segui le istruzioni per scegliere un nome e un username (che deve terminare con `_bot`).
3.  **Salva il Token API:** BotFather ti fornirà un **Token API** (es. `8271278686:AAHhcDkTK38Xpz5srRUviniJuYk7kAeBgGk`). Questo è il tuo `TELEGRAM_TOKEN`.

### 1.2. Configurazione dei Servizi Esterni

| Servizio | Azione | Chiave da Salvare |
| :--- | :--- | :--- |
| **GitHub** | Crea un account e un nuovo repository vuoto (es. `TinyAgents`). | N/A |
| **Vercel** | Crea un account e collegalo a GitHub. | N/A |
| **Groq** | Crea un account, vai su "API Keys" e genera una nuova chiave. | `GROQ_API_KEY` |
| **Stripe** (Per Sviluppi Futuri) | Crea un account per la monetizzazione. | Chiave Pubblicabile e Chiave Segreta. |

---

## Fase 2: Struttura del Progetto e Configurazione Iniziale

Questa struttura è necessaria per il corretto funzionamento del deployment Serverless su Vercel.

### 2.1. Struttura delle Cartelle

La struttura finale del progetto sarà:

```
TinyAgents/
|-- api/
|   |-- telegram.py      # La nostra funzione serverless principale
|-- .gitignore           # File da ignorare per Git
|-- requirements.txt     # Dipendenze Python
|-- vercel.json          # Configurazione per Vercel
```

### 2.2. File di Configurazione

#### `requirements.txt`
Questo file elenca le librerie Python che Vercel deve installare per la funzione Serverless.

```
requests
python-telegram-bot
groq
```

#### `vercel.json`
Questo file istruisce Vercel su come costruire e instradare la richiesta HTTP alla nostra funzione Python.

```json
{
  "builds": [
    {
      "src": "api/telegram.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/telegram",
      "dest": "api/telegram.py"
    }
  ]
}
```

---

## Fase 3: Sviluppo del Backend - La Funzione Serverless

Il file `api/telegram.py` contiene la logica per ricevere gli aggiornamenti da Telegram (Webhook), instradare i comandi e interrogare l'API di Groq per generare le risposte.

### Codice Sorgente: `api/telegram.py`

```python
import os
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse
import telegram
from groq import Groq

# --- CONFIGURAZIONE INIZIALE ---
# Le chiavi API vengono lette dalle variabili d'ambiente di Vercel
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# Inizializza il client Groq
try:
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"Attenzione: Impossibile inizializzare Groq client. Errore: {e}")
    groq_client = None


# --- DEFINIZIONE DEI "TINY AGENTS" ---
# Ogni agent ha un prompt di sistema (istruzioni per l'AI) e una descrizione
AGENTS = {
    "meme_persona": {
        "description": "Trasforma una tua idea in una caption per un meme virale.",
        "system_prompt": "Sei un generatore di meme. Data un'idea, crea una caption breve, divertente e virale in stile meme. Aggiungi 3-5 hashtag pertinenti e di tendenza. Rispondi solo con la caption e gli hashtag."
    },
    "viral_pitch": {
        "description": "Scrivi un pitch freddo e conciso per LinkedIn.",
        "system_prompt": "Sei un esperto di copywriting per LinkedIn. Scrivi un messaggio di direct message (DM) di massimo 50 parole basato sull'idea dell'utente. Il tono deve essere professionale ma accattivante. L'obiettivo è ottenere una risposta."
    },
    "roast_generator": {
        "description": "Fornisci un argomento e io lo 'roasterò' simpaticamente.",
        "system_prompt": "Sei un comico specializzato in 'roast'. Data una parola o una frase, crea una battuta divertente e pungente, ma mai offensiva o volgare. Sii creativo e inaspettato."
    }
}

def get_llm_response(agent_name, user_input):
    """
    Funzione per interrogare l'LLM con il prompt specifico dell'agent.
    """
    if not groq_client:
        return "Servizio AI non disponibile. Controlla la configurazione della chiave API Groq."
        
    if agent_name not in AGENTS:
        return "Agente non valido."

    system_prompt = AGENTS[agent_name]["system_prompt"]
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            model="llama3-8b-8192", # Modello Groq veloce
            temperature=0.7,
            max_tokens=150,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Errore API Groq: {e}")
        return "Oops! Qualcosa è andato storto con l'intelligenza artificiale. Riprova tra poco."

# --- GESTORE DELLA RICHIESTA HTTP (SERVERLESS FUNCTION) ---
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Leggi il corpo della richiesta inviata da Telegram
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            update = telegram.Update.de_json(json.loads(post_data.decode('utf-8')), None)
            
            if not update.message or not update.message.text:
                self.send_response(200)
                self.end_headers()
                return

            chat_id = update.message.chat.id
            text = update.message.text

            if not TELEGRAM_TOKEN:
                bot = None
            else:
                bot = telegram.Bot(token=TELEGRAM_TOKEN)

            # Logica di routing dei comandi
            if text.startswith('/start'):
                welcome_message = "Benvenuto in Tiny Agents! 🤖\n\n"
                welcome_message += "Scegli un micro-agente per un compito specifico:\n\n"
                for agent_name, data in AGENTS.items():
                    welcome_message += f"🔹 `/{agent_name}` - {data['description']}\n"
                welcome_message += "\nUsa il comando seguito dalla tua richiesta. Esempio:\n`/meme_persona gatto che suona il pianoforte`"
                
                if bot:
                    bot.send_message(chat_id=chat_id, text=welcome_message, parse_mode=telegram.ParseMode.MARKDOWN)

            elif text.startswith('/'):
                parts = text.split(' ', 1)
                command = parts[0][1:] # Rimuove lo '/'
                
                if command in AGENTS:
                    if len(parts) > 1:
                        user_input = parts[1].strip()
                        
                        if bot:
                            bot.send_message(chat_id=chat_id, text="⏳ Sto elaborando la tua richiesta...")
                        
                        response = get_llm_response(command, user_input)
                        
                        if bot:
                            bot.send_message(chat_id=chat_id, text=response)
                    else:
                        if bot:
                            bot.send_message(chat_id=chat_id, text=f"Uso corretto: `/{command} [la tua richiesta]`", parse_mode=telegram.ParseMode.MARKDOWN)
                else:
                    if bot:
                        bot.send_message(chat_id=chat_id, text="Comando non riconosciuto. Usa /start per vedere la lista degli agenti disponibili.")
            
            else:
                pass # Gestione di messaggi non-comando

        except Exception as e:
            print(f"Errore nel gestore: {e}")
            try:
                if bot and chat_id:
                    bot.send_message(chat_id=chat_id, text="Si è verificato un errore interno. Riprova più tardi.")
            except:
                pass

        # Rispondi a Telegram che la richiesta è stata ricevuta correttamente
        self.send_response(200)
        self.end_headers()
        return
```

---

## Fase 4: Deployment su Vercel e Collegamento a Telegram

Questa fase è cruciale per rendere il tuo bot accessibile al mondo. Poiché non posso eseguire il deployment per te, ti fornirò le istruzioni esatte da seguire.

### 4.1. Caricamento del Codice su GitHub

1.  **Inizializza Git e aggiungi i file:**
    Assicurati di essere nella cartella `TinyAgents` nel tuo terminale.
    ```bash
    git init
    git add .
    git commit -m "Tiny Agents: Serverless function and Vercel config"
    ```

2.  **Collega e Carica i File:**
    Sostituisci `<TUO_USERNAME>` con il tuo username GitHub e `<NOME_DEL_REPOSITORY>` con il nome del repository che hai creato (es. `TinyAgents`).
    ```bash
    git remote add origin https://github.com/<TUO_USERNAME>/<NOME_DEL_REPOSITORY>.git
    git branch -M main
    git push -u origin main
    ```

### 4.2. Deployment su Vercel e Variabili d'Ambiente

1.  **Importa il Progetto su Vercel:**
    *   Vai alla tua dashboard di [Vercel](https://vercel.com).
    *   Clicca su **"Add New..."** -> **"Project"**.
    *   Seleziona il repository `TinyAgents` che hai appena caricato da GitHub.

2.  **Configura le Variabili d'Ambiente (CRITICO):**
    Prima di cliccare su "Deploy", vai nella sezione **"Environment Variables"** e aggiungi le seguenti chiavi:

    | Nome Variabile | Valore (La Tua Chiave Segreta) |
    | :--- | :--- |
    | `TELEGRAM_TOKEN` | Il token API ottenuto da BotFather. |
    | `GROQ_API_KEY` | La chiave API ottenuta da Groq. |

3.  **Avvia il Deployment:** Clicca su **"Deploy"**.

### 4.3. Configurazione del Webhook di Telegram

Una volta che il deployment è completato, Vercel ti fornirà un URL.

1.  **Ottieni il Webhook URL:**
    *   L'URL della tua funzione serverless sarà: `https://<NOME_DEL_TUO_PROGETTO>.vercel.app/api/telegram`
    *   **Esempio:** `https://tiny-agents-factory.vercel.app/api/telegram`.

2.  **Imposta il Webhook:**
    Visita il seguente indirizzo nel tuo browser, sostituendo i segnaposto:

    ```
    https://api.telegram.org/bot<IL_TUO_TOKEN_API>/setWebhook?url=<IL_TUO_WEBHOOK_URL>
    ```

    **Esempio di comando completo (usando il tuo token fornito):**
    ```
    https://api.telegram.org/bot8271278686:AAHhcDkTK38Xpz5srRUviniJuYk7kAeBgGk/setWebhook?url=https://tiny-agents-factory.vercel.app/api/telegram
    ```

Se l'operazione ha successo, riceverai una risposta JSON con `"ok": true`. Il tuo bot è ora attivo!

---

## Sviluppi Futuri e Monetizzazione

Il bot è ora funzionante. Per trasformarlo in un prodotto di successo, i prossimi passi dovrebbero concentrarsi sulla monetizzazione e sulla crescita.

### 1. Monetizzazione con Stripe

Per implementare la monetizzazione, dovrai:
1.  **Creare un Prodotto su Stripe:** Definisci un prodotto (es. "Pacchetto 100 Esecuzioni") e ottieni il suo ID.
2.  **Aggiungere un Comando `/buy` al Bot:** Modifica `api/telegram.py` per intercettare il comando `/buy`.
3.  **Generare una Sessione di Checkout:** Quando l'utente usa `/buy`, il bot chiama l'API di Stripe per creare una sessione di checkout e invia il link all'utente.
4.  **Gestire il Webhook di Stripe:** Creare una seconda funzione Serverless su Vercel (`api/stripe_webhook.py`) che ascolta l'evento `checkout.session.completed` di Stripe. Quando l'evento arriva, questa funzione aggiorna il database dell'utente (ad esempio, il suo ID Telegram) aggiungendo i crediti acquistati.

### 2. Landing Page e Branding

Creare una semplice Landing Page su Vercel (usando il preset `web-static`) per:
*   Descrivere il valore degli agenti.
*   Mostrare esempi di output.
*   Fornire un link diretto al bot Telegram.

### 3. Database per i Crediti

Per gestire i crediti degli utenti (necessari per la monetizzazione), è necessario un database. Si consiglia di integrare un servizio come **Supabase** o **PostgreSQL** (disponibile tramite Vercel) per associare l'ID Telegram di ogni utente al numero di esecuzioni rimanenti.

---
