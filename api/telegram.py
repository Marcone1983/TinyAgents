import os
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse
import telegram
from groq import Groq
from supabase import create_client, Client
import stripe

# --- CONFIGURAZIONE INIZIALE ---
# Le chiavi API vengono lette dalle variabili d'ambiente di Vercel
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PRODUCT_ID = os.environ.get('STRIPE_PRODUCT_ID') # ID del prodotto Stripe per 100 crediti

# Inizializza i client
try:
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"Attenzione: Impossibile inizializzare Groq client. Errore: {e}")
    groq_client = None

try:
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Attenzione: Impossibile inizializzare Supabase client. Errore: {e}")
    supabase_client = None

try:
    stripe.api_key = STRIPE_SECRET_KEY
except Exception as e:
    print(f"Attenzione: Impossibile inizializzare Stripe. Errore: {e}")

# --- FUNZIONI DI GESTIONE CREDITI (SUPABASE) ---

def get_user_credits(user_id: int) -> int:
    """Recupera i crediti dell'utente da Supabase. Crea un record se non esiste."""
    if not supabase_client:
        return 0 # Fallback in caso di errore di connessione
        
    try:
        response = supabase_client.table('users').select('credits').eq('id', user_id).execute()
        
        if response.data:
            return response.data[0]['credits']
        else:
            # Utente non trovato, lo creiamo con 0 crediti
            supabase_client.table('users').insert({"id": user_id, "credits": 0}).execute()
            return 0
    except Exception as e:
        print(f"Errore Supabase (get_user_credits): {e}")
        return 0

def decrement_user_credits(user_id: int) -> bool:
    """Decrementa i crediti dell'utente di 1."""
    if not supabase_client:
        return False
        
    try:
        # Recupera i crediti attuali
        current_credits = get_user_credits(user_id)
        if current_credits > 0:
            # Decrementa e aggiorna
            new_credits = current_credits - 1
            supabase_client.table('users').update({"credits": new_credits}).eq('id', user_id).execute()
            return True
        return False
    except Exception as e:
        print(f"Errore Supabase (decrement_user_credits): {e}")
        return False

# --- FUNZIONE DI ACQUISTO (STRIPE) ---

def create_stripe_checkout_session(user_id: int, bot_url: str) -> str:
    """Crea una sessione di checkout Stripe e restituisce l'URL."""
    if not STRIPE_PRODUCT_ID or not stripe.api_key:
        return "Errore di configurazione Stripe. Controlla STRIPE_PRODUCT_ID e STRIPE_SECRET_KEY."

    # URL di successo e cancellazione (devono essere configurati su Vercel)
    # Usiamo l'URL del bot come base per reindirizzare l'utente a Telegram
    success_url = f"https://t.me/TinyAgents_bot?start=success_{user_id}"
    cancel_url = f"https://t.me/TinyAgents_bot?start=cancel_{user_id}"
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': STRIPE_PRODUCT_ID, # Questo dovrebbe essere l'ID del prezzo, non del prodotto
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            client_reference_id=str(user_id), # Usiamo l'ID Telegram come riferimento
            metadata={
                'telegram_user_id': str(user_id),
            }
        )
        return session.url
    except Exception as e:
        print(f"Errore Stripe: {e}")
        return "Errore durante la creazione della sessione di pagamento."


# --- DEFINIZIONE DEI "TINY AGENTS" ---
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
            model="llama3-8b-8192", # Un modello veloce ed efficace
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
            user_id = update.message.from_user.id
            text = update.message.text

            if not TELEGRAM_TOKEN:
                bot = None
            else:
                bot = telegram.Bot(token=TELEGRAM_TOKEN)

            # Logica di routing dei comandi
            if text.startswith('/start'):
                # Gestione dei messaggi di ritorno da Stripe
                if "success" in text:
                    bot.send_message(chat_id=chat_id, text="🎉 Pagamento completato con successo! I tuoi crediti saranno aggiunti a breve. Usa /credits per controllare il saldo.")
                elif "cancel" in text:
                    bot.send_message(chat_id=chat_id, text="❌ Pagamento annullato. Puoi riprovare in qualsiasi momento con /buy.")
                else:
                    # Messaggio di benvenuto standard
                    welcome_message = "Benvenuto in Tiny Agents! 🤖\n\n"
                    welcome_message += "Scegli un micro-agente per un compito specifico:\n\n"
                    for agent_name, data in AGENTS.items():
                        welcome_message += f"🔹 `/{agent_name}` - {data['description']}\n"
                    welcome_message += "\nUsa il comando seguito dalla tua richiesta. Esempio:\n`/meme_persona gatto che suona il pianoforte`\n\n"
                    welcome_message += "💳 **Monetizzazione:** Usa `/credits` per vedere il tuo saldo e `/buy` per acquistare nuovi utilizzi."
                    
                    if bot:
                        bot.send_message(chat_id=chat_id, text=welcome_message, parse_mode=telegram.ParseMode.MARKDOWN)

            elif text.startswith('/credits'):
                credits = get_user_credits(user_id)
                if bot:
                    bot.send_message(chat_id=chat_id, text=f"Il tuo saldo attuale è di **{credits}** crediti. Usa `/buy` per ricaricare.", parse_mode=telegram.ParseMode.MARKDOWN)

            elif text.startswith('/buy'):
                # Otteniamo l'URL base del bot da Vercel (necessario per il reindirizzamento di Stripe)
                bot_url = self.headers.get('X-Forwarded-Host', 'https://t.me/TinyAgents_bot')
                checkout_url = create_stripe_checkout_session(user_id, bot_url)
                
                if "Errore" in checkout_url:
                    bot.send_message(chat_id=chat_id, text=checkout_url)
                else:
                    bot.send_message(chat_id=chat_id, text=f"Clicca qui per acquistare crediti: [Acquista Crediti]({checkout_url})", parse_mode=telegram.ParseMode.MARKDOWN)

            elif text.startswith('/'):
                parts = text.split(' ', 1)
                command = parts[0][1:] # Rimuove lo '/'
                
                # Controlla se il comando è un agent valido
                if command in AGENTS:
                    if len(parts) > 1:
                        user_input = parts[1].strip()
                        
                        # --- LOGICA DI CONTROLLO CREDITI ---
                        credits = get_user_credits(user_id)
                        if credits <= 0:
                            bot.send_message(chat_id=chat_id, text="🚫 **Crediti esauriti!** Per continuare a usare gli agenti, acquista nuovi crediti con il comando `/buy`.")
                            self.send_response(200)
                            self.end_headers()
                            return

                        # Decrementa i crediti prima di procedere
                        if not decrement_user_credits(user_id):
                            bot.send_message(chat_id=chat_id, text="⚠️ Errore nel decremento dei crediti. Riprova o contatta l'assistenza.")
                            self.send_response(200)
                            self.end_headers()
                            return
                        
                        # Notifica l'utente del saldo rimanente
                        bot.send_message(chat_id=chat_id, text=f"✅ Credito utilizzato. Saldo rimanente: **{credits - 1}**.\n⏳ Sto elaborando la tua richiesta...", parse_mode=telegram.ParseMode.MARKDOWN)
                        
                        # Ottieni la risposta dall'LLM
                        response = get_llm_response(command, user_input)
                        
                        # Invia la risposta all'utente
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
