### Fase 4: Deployment su Vercel e Collegamento a Telegram (Simulazione e Istruzioni per l'Utente)

Questa fase è cruciale per rendere il tuo bot accessibile al mondo. Poiché non posso eseguire il deployment per te, ti fornirò le istruzioni esatte da seguire.

#### 4.1. Caricamento del Codice su GitHub

Assicurati di essere nella cartella `TinyAgents` nel tuo terminale.

1.  **Inizializza Git e aggiungi i file:**
    ```bash
    git init
    git add .
    git commit -m "Tiny Agents: Serverless function and Vercel config"
    ```

2.  **Crea il Repository Remoto:**
    *   Vai su [GitHub](https://github.com) e crea un **nuovo repository vuoto** (es. `TinyAgents`).
    *   **NON** spuntare l'opzione per inizializzarlo con un `README` o `.gitignore`.

3.  **Collega e Carica i File:**
    Sostituisci `<TUO_USERNAME>` con il tuo username GitHub.
    ```bash
    git remote add origin https://github.com/<TUO_USERNAME>/TinyAgents.git
    git branch -M main
    git push -u origin main
    ```

#### 4.2. Deployment su Vercel e Configurazione delle Variabili d'Ambiente

1.  **Importa il Progetto su Vercel:**
    *   Vai alla tua dashboard di [Vercel](https://vercel.com).
    *   Clicca su **"Add New..."** -> **"Project"**.
    *   Seleziona il repository `TinyAgents` che hai appena caricato da GitHub.

2.  **Configura le Variabili d'Ambiente (CRITICO):**
    Prima di cliccare su "Deploy", vai nella sezione **"Environment Variables"** e aggiungi le seguenti chiavi, che sono essenziali per il funzionamento del bot:

    | Nome Variabile | Valore (La Tua Chiave Segreta) | Descrizione |
    | :--- | :--- | :--- |
    | `TELEGRAM_TOKEN` | Il token API ottenuto da BotFather. | Permette al tuo codice di comunicare con Telegram. |
    | `GROQ_API_KEY` | La chiave API ottenuta da Groq. | Permette al tuo codice di accedere ai modelli LLM veloci. |

3.  **Avvia il Deployment:**
    *   Clicca su **"Deploy"**. Vercel prenderà il codice da GitHub, installerà le dipendenze (`requirements.txt`) e pubblicherà la tua funzione serverless.

#### 4.3. Configurazione del Webhook di Telegram

Una volta che il deployment è completato, Vercel ti fornirà un URL.

1.  **Ottieni il Webhook URL:**
    *   L'URL della tua funzione serverless sarà: `https://<NOME_DEL_TUO_PROGETTO>.vercel.app/api/telegram`
    *   **Esempio:** Se il tuo progetto si chiama `tiny-agents-factory`, l'URL sarà `https://tiny-agents-factory.vercel.app/api/telegram`.

2.  **Imposta il Webhook:**
    Devi dire a Telegram di inviare tutti i messaggi a questo URL. Apri il tuo browser e visita il seguente indirizzo, sostituendo i segnaposto:

    ```
    https://api.telegram.org/bot<IL_TUO_TOKEN_API>/setWebhook?url=<IL_TUO_WEBHOOK_URL>
    ```

    **Esempio di comando completo:**
    ```
    https://api.telegram.org/bot8271278686:AAHhcDkTK38Xpz5srRUviniJuYk7kAeBgGk/setWebhook?url=https://tiny-agents-factory.vercel.app/api/telegram
    ```

    Se l'operazione ha successo, riceverai una risposta JSON con `"ok": true`.

#### 4.4. Test Finale

Il tuo bot è ora attivo!

1.  Apri Telegram e cerca il tuo bot.
2.  Invia il comando `/start`.
3.  Prova un agente: `/meme_persona il mio gatto è un programmatore pigro`
    
Se ricevi la risposta, il tuo **Tiny Agents** è operativo!
