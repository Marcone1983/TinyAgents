# Istruzioni per la Configurazione Finale su BotFather

Queste istruzioni ti guidano su come utilizzare i comandi `/setdomain` e `/setmenubutton` in BotFather.

**Nota Importante:** Il tuo bot è attualmente un **Webhook Bot** e non una **Mini App** (che è ciò che userebbe `/setmenubutton`). Tuttavia, puoi usare `/setmenubutton` per reindirizzare gli utenti a una pagina web esterna (come una Landing Page).

### 1. Comando `/setdomain`

Questo comando è utilizzato principalmente per le Mini App o per collegare un dominio specifico al tuo bot.

*   **Azione:** Vai su BotFather e digita `/setdomain`.
*   **Risposta di BotFather:** Ti chiederà di selezionare il bot.
*   **La Tua Risposta:** Seleziona il tuo bot (`TinyAgents_bot`).
*   **Risposta di BotFather:** Ti chiederà di inserire il dominio.
*   **La Tua Risposta:** Inserisci il dominio principale del tuo deployment Vercel (senza `https://` e senza `/api/telegram`).

| Campo | Valore da Inserire | Esempio |
| :--- | :--- | :--- |
| **Dominio** | `tiny-agents-xxxx.vercel.app` | `tiny-agents-ine6.vercel.app` |

### 2. Comando `/setmenubutton` (Menu Web App)

Questo comando crea un pulsante permanente nel menu del tuo bot che apre una pagina web (Mini App o Landing Page).

*   **Azione:** Vai su BotFather e digita `/setmenubutton`.
*   **Risposta di BotFather:** Ti chiederà di selezionare il bot.
*   **La Tua Risposta:** Seleziona il tuo bot (`TinyAgents_bot`).
*   **Risposta di BotFather:** Ti chiederà di inserire il testo del pulsante.
*   **La Tua Risposta:** Inserisci un testo accattivante.
*   **Risposta di BotFather:** Ti chiederà l'URL della Web App.

| Campo | Valore da Inserire | Esempio |
| :--- | :--- | :--- |
| **Testo Pulsante** | `Acquista Crediti` o `Landing Page` | `TinyAgents Store` |
| **URL Web App** | L'URL della tua Landing Page (se ne hai una) o l'URL del tuo deployment Vercel. | `https://tiny-agents-ine6.vercel.app` |

**Consiglio:** Se non hai una Landing Page, puoi usare l'URL del tuo deployment Vercel per ora. In futuro, potresti creare una semplice Landing Page su Vercel e usare quell'URL.

### 3. Comando `/setdescription`

Questo comando imposta la descrizione che appare quando un utente apre per la prima volta la chat con il tuo bot.

*   **Azione:** Vai su BotFather e digita `/setdescription`.
*   **Risposta di BotFather:** Ti chiederà di selezionare il bot.
*   **La Tua Risposta:** Seleziona il tuo bot (`TinyAgents_bot`).
*   **Risposta di BotFather:** Ti chiederà di inserire la descrizione.
*   **La Tua Risposta:** Copia e incolla la descrizione che ti ho fornito nel file `tinyagents_description.txt`.
