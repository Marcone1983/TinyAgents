import os
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse
import telegram
from telegram import ParseMode
from groq import Groq
from supabase.client import create_client, Client
import stripe

# --- CONFIGURAZIONE INIZIALE ---
# Le chiavi API vengono lette dalle variabili d'ambiente di Vercel
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PRODUCT_ID = os.environ.get('STRIPE_PRODUCT_ID')

# --- FUNZIONI DI GESTIONE CREDITI (SUPABASE) ---

def get_supabase_client() -> Client | None:
    """Inizializza e restituisce il client Supabase."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Errore durante l'inizializzazione del client Supabase: {e}")
        return None

def get_user_credits(user_id: int) -> int:
    """Recupera i crediti dell'utente da Supabase. Crea un record se non esiste."""
    supabase_client = get_supabase_client()
    if not supabase_client:
        return 0
        
    try:
        response = supabase_client.table('users').select('credits').eq('id', user_id).execute()
        
        if response.data:
            return response.data[0]['credits']
        else:
            # Inizializza l'utente con 0 crediti
            supabase_client.table('users').insert({"id": user_id, "credits": 0}).execute()
            return 0
    except Exception as e:
        print(f"Errore Supabase (get_user_credits): {e}")
        return 0

def decrement_user_credits(user_id: int) -> bool:
    """Decrementa i crediti dell'utente di 1."""
    supabase_client = get_supabase_client()
    if not supabase_client:
        return False
        
    try:
        # Nota: get_user_credits è ricorsivo e crea l'utente se non esiste
        current_credits = get_user_credits(user_id)
        if current_credits > 0:
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
    if not STRIPE_SECRET_KEY or not STRIPE_PRODUCT_ID:
        return "Errore di configurazione Stripe. Controlla STRIPE_PRODUCT_ID e STRIPE_SECRET_KEY."
    
    try:
        # Inizializzazione di Stripe all'interno della funzione
        stripe.api_key = STRIPE_SECRET_KEY
    except Exception as e:
        print(f"Errore durante l'inizializzazione di Stripe: {e}")
        return "Errore interno durante l'inizializzazione di Stripe."

    success_url = f"https://t.me/TinyAgents_bot?start=success_{user_id}"
    cancel_url = f"https://t.me/TinyAgents_bot?start=cancel_{user_id}"
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': STRIPE_PRODUCT_ID,
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            client_reference_id=str(user_id),
            metadata={
                'telegram_user_id': str(user_id),
            }
        )
        return session.url
    except Exception as e:
        print(f"Errore Stripe: {e}")
        return "Errore durante la creazione della sessione di pagamento."


# --- DEFINIZIONE DEI "TINY AGENTS" (10 AGENTI) ---
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
    },
    "email_writer": {
        "description": "Scrivi email professionali e persuasive.",
        "system_prompt": "Sei un esperto di email marketing. Scrivi un'email professionale e persuasiva basata sul tema fornito dall'utente. L'email deve essere breve (max 100 parole), con un oggetto accattivante e una call-to-action chiara."
    },
    "tweet_generator": {
        "description": "Crea tweet virali e accattivanti.",
        "system_prompt": "Sei un esperto di social media. Crea un tweet breve (max 280 caratteri), virale e accattivante basato sull'idea dell'utente. Aggiungi emoji pertinenti e hashtag di tendenza."
    },
    "product_description": {
        "description": "Scrivi descrizioni di prodotti per e-commerce.",
        "system_prompt": "Sei un copywriter di e-commerce. Scrivi una descrizione di prodotto breve e persuasiva (max 150 parole) basata sul prodotto descritto dall'utente. Evidenzia i benefici principali e crea urgenza d'acquisto."
    },
    "story_starter": {
        "description": "Genera l'inizio di una storia affascinante.",
        "system_prompt": "Sei uno scrittore creativo. Genera l'inizio di una storia affascinante (max 100 parole) basato sul tema fornito dall'utente. L'inizio deve catturare l'attenzione e creare suspense."
    },
    "code_explainer": {
        "description": "Spiega concetti di programmazione in modo semplice.",
        "system_prompt": "Sei un insegnante di programmazione. Spiega il concetto di programmazione fornito dall'utente in modo semplice e comprensibile (max 150 parole). Usa esempi pratici e evita il gergo tecnico complesso."
    },
    "motivational_quote": {
        "description": "Genera citazioni motivazionali personalizzate.",
        "system_prompt": "Sei un coach motivazionale. Genera una citazione motivazionale personalizzata (max 50 parole) basata sulla situazione o il tema fornito dall'utente. La citazione deve essere ispiratrice e pratica."
    },
    "seo_optimizer": {
        "description": "Ottimizza il testo per i motori di ricerca.",
        "system_prompt": "Sei un esperto SEO. Ottimizza il testo fornito dall'utente per i motori di ricerca (max 150 parole). Aggiungi parole chiave pertinenti, migliora la struttura e rendi il testo più accattivante per i lettori."
    }
}

def get_llm_response(agent_name, user_input):
    """
    Funzione per interrogare l'LLM con il prompt specifico dell'agent.
    """
    if not GROQ_API_KEY:
        return "Servizio AI non disponibile. Chiave API Groq mancante."
        
    if agent_name not in AGENTS:
        return "Agente non valido."

    system_prompt = AGENTS[agent_name]["system_prompt"]
    
    try:
        # Inizializzazione del client Groq all'interno della funzione
        groq_client = Groq(api_key=GROQ_API_KEY)
        
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            model="llama3-8b-8192",
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
        # 1. CONTROLLO CRITICO DELLE VARIABILI D'AMBIENTE
        # Se le chiavi essenziali non sono presenti, invia un messaggio di errore all'utente
        if not all([TELEGRAM_TOKEN, GROQ_API_KEY, SUPABASE_URL, SUPABASE_KEY, STRIPE_SECRET_KEY, STRIPE_PRODUCT_ID]):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Tenta di inviare un messaggio di errore se il token è presente
            if TELEGRAM_TOKEN and self.headers.get('X-Forwarded-Host'):
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    update = telegram.Update.from_dict(json.loads(post_data.decode('utf-8')))
                    if update.message:
                        bot = telegram.Bot(token=TELEGRAM_TOKEN)
                        missing_keys = [k for k, v in {'GROQ_API_KEY': GROQ_API_KEY, 'SUPABASE_URL': SUPABASE_URL, 'STRIPE_SECRET_KEY': STRIPE_SECRET_KEY}.items() if not v]
                        bot.send_message(chat_id=update.message.chat.id, text=f"⚠️ **ERRORE CRITICO DI CONFIGURAZIONE!** ⚠️\n\nIl bot non è configurato correttamente. Le seguenti chiavi sono mancanti o vuote in Vercel: {', '.join(missing_keys)}\n\n**SOLUZIONE:** Vai alla dashboard di Vercel e inserisci le chiavi mancanti.", parse_mode=ParseMode.MARKDOWN)
                except Exception as e:
                    print(f"Errore durante l'invio del messaggio di errore: {e}")
            
            return
        # Controllo delle chiavi API essenziali
        if not TELEGRAM_TOKEN or not GROQ_API_KEY or not SUPABASE_URL or not SUPABASE_KEY:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_msg = {
                "error": "Configurazione incompleta",
                "missing": {
                    "TELEGRAM_TOKEN": not TELEGRAM_TOKEN,
                    "GROQ_API_KEY": not GROQ_API_KEY,
                    "SUPABASE_URL": not SUPABASE_URL,
                    "SUPABASE_KEY": not SUPABASE_KEY
                }
            }
            self.wfile.write(json.dumps(error_msg).encode())
            return
        
        # Leggi il corpo della richiesta inviata da Telegram
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            update = telegram.Update.from_dict(json.loads(post_data.decode('utf-8')))
            
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
            
            # Inizio del blocco di gestione dei comandi con try/except per debug
            try:
                # Logica di routing dei comandi
                if text.startswith('/start'):
                    if "success" in text:
                        bot.send_message(chat_id=chat_id, text="🎉 Pagamento completato con successo! I tuoi crediti saranno aggiunti a breve. Usa /credits per controllare il saldo.")
                    elif "cancel" in text:
                        bot.send_message(chat_id=chat_id, text="❌ Pagamento annullato. Puoi riprovare in qualsiasi momento con /buy.")
                    else:
                        welcome_message = "Benvenuto in Tiny Agents! 🤖\n\n"
                        welcome_message += "Scegli un micro-agente per un compito specifico:\n\n"
                        for agent_name, data in AGENTS.items():
                            welcome_message += f"🔹 `/{agent_name}` - {data['description']}\n"
                        welcome_message += "\nUsa il comando seguito dalla tua richiesta. Esempio:\n`/meme_persona gatto che suona il pianoforte`\n\n"
                        welcome_message += "💳 **Monetizzazione:** Usa `/credits` per vedere il tuo saldo e `/buy` per acquistare nuovi utilizzi."
                        
                        if bot:
                            bot.send_message(chat_id=chat_id, text=welcome_message, parse_mode=ParseMode.MARKDOWN)

                elif text.startswith('/credits'):
                    credits = get_user_credits(user_id)
                    if bot:
                        bot.send_message(chat_id=chat_id, text=f"Il tuo saldo attuale è di **{credits}** crediti. Usa `/buy` per ricaricare.", parse_mode=ParseMode.MARKDOWN)

                elif text.startswith('/buy'):
                    bot_url = self.headers.get('X-Forwarded-Host', 'https://t.me/TinyAgents_bot')
                    checkout_url = create_stripe_checkout_session(user_id, bot_url)
                    
                    if "Errore" in checkout_url:
                        bot.send_message(chat_id=chat_id, text=checkout_url)
                    else:
                        bot.send_message(chat_id=chat_id, text=f"Clicca qui per acquistare crediti: [Acquista Crediti]({checkout_url})", parse_mode=ParseMode.MARKDOWN)

                elif text.startswith('/'):
                    parts = text.split(' ', 1)
                    command = parts[0][1:]
                    
                    if command in AGENTS:
                        if len(parts) > 1:
                            user_input = parts[1].strip()
                            
                            credits = get_user_credits(user_id)
                            if credits <= 0:
                                bot.send_message(chat_id=chat_id, text="🚫 **Crediti esauriti!** Per continuare a usare gli agenti, acquista nuovi crediti con il comando `/buy`.")
                                self.send_response(200)
                                self.end_headers()
                                return

                            if not decrement_user_credits(user_id):
                                bot.send_message(chat_id=chat_id, text="⚠️ Errore nel decremento dei crediti. Riprova o contatta l'assistenza.")
                                self.send_response(200)
                                self.end_headers()
                                return
                            
                            bot.send_message(chat_id=chat_id, text=f"✅ Credito utilizzato. Saldo rimanente: **{credits - 1}**.\n⏳ Sto elaborando la tua richiesta...", parse_mode=ParseMode.MARKDOWN)
                            
                            response = get_llm_response(command, user_input)
                            
                            bot.send_message(chat_id=chat_id, text=response)
                        else:
                            if bot:
                                bot.send_message(chat_id=chat_id, text=f"Uso corretto: `/{command} [la tua richiesta]`", parse_mode=ParseMode.MARKDOWN)
                    else:
                        if bot:
                            bot.send_message(chat_id=chat_id, text="Comando non riconosciuto. Usa /start per vedere la lista degli agenti disponibili.")
                
                else:
                    pass
            
            except Exception as e:
                # Logga l'errore specifico del gestore comandi
                print(f"ERRORE GESTORE COMANDI: {e}")
                if bot and chat_id:
                    bot.send_message(chat_id=chat_id, text=f"Si è verificato un errore interno durante l'elaborazione del comando. Dettagli: {e}")

        except Exception as e:
            # Logga l'errore di parsing o di inizializzazione
            print(f"ERRORE PARSING/INIZIALIZZAZIONE: {e}")
            # Non possiamo inviare un messaggio all'utente qui perché chat_id potrebbe non essere disponibile

        self.send_response(200)
        self.end_headers()
        return
