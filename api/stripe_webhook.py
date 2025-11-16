import os
import json
from http.server import BaseHTTPRequestHandler
from supabase import create_client, Client
import stripe

# --- CONFIGURAZIONE INIZIALE ---
# Le chiavi API vengono lette dalle variabili d'ambiente di Vercel
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET') # Chiave segreta del webhook di Stripe

# Inizializza i client
try:
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Attenzione: Impossibile inizializzare Supabase client. Errore: {e}")
    supabase_client = None

try:
    stripe.api_key = STRIPE_SECRET_KEY
except Exception as e:
    print(f"Attenzione: Impossibile inizializzare Stripe. Errore: {e}")

# --- FUNZIONE DI AGGIORNAMENTO CREDITI (SUPABASE) ---

def add_credits_to_user(user_id: int, amount: int):
    """Aggiunge crediti all'utente in Supabase."""
    if not supabase_client:
        return False
        
    try:
        # Recupera il record dell'utente
        response = supabase_client.table('users').select('credits').eq('id', user_id).execute()
        
        if response.data:
            current_credits = response.data[0]['credits']
            new_credits = current_credits + amount
            
            # Aggiorna i crediti
            supabase_client.table('users').update({"credits": new_credits}).eq('id', user_id).execute()
            print(f"Crediti aggiornati per utente {user_id}: {current_credits} -> {new_credits}")
            return True
        else:
            # Utente non trovato, lo creiamo con i crediti acquistati
            supabase_client.table('users').insert({"id": user_id, "credits": amount}).execute()
            print(f"Nuovo utente creato con {amount} crediti: {user_id}")
            return True
            
    except Exception as e:
        print(f"Errore Supabase (add_credits_to_user): {e}")
        return False

# --- GESTORE DELLA RICHIESTA HTTP (WEBHOOK STRIPE) ---
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Leggi il corpo della richiesta
        content_length = int(self.headers['Content-Length'])
        payload = self.rfile.read(content_length)
        sig_header = self.headers.get('stripe-signature')
        
        event = None
        
        # Verifica la firma del webhook per sicurezza
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            # Invalid payload
            self.send_response(400)
            self.end_headers()
            return
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            self.send_response(400)
            self.end_headers()
            return

        # Gestisci l'evento
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            
            # Recupera l'ID utente Telegram dal metadata
            telegram_user_id = session.get('client_reference_id')
            
            if telegram_user_id:
                try:
                    # Recupera i dettagli del prodotto acquistato per determinare i crediti
                    # In un'implementazione reale, si dovrebbe recuperare il prezzo e mappare i crediti
                    # Per semplicità, assumiamo che l'acquisto dia 100 crediti
                    CREDITS_TO_ADD = 100 
                    
                    if add_credits_to_user(int(telegram_user_id), CREDITS_TO_ADD):
                        self.send_response(200)
                        self.end_headers()
                        return
                    else:
                        # Errore nell'aggiornamento del database
                        self.send_response(500)
                        self.end_headers()
                        return
                except Exception as e:
                    print(f"Errore durante l'elaborazione della sessione: {e}")
                    self.send_response(500)
                    self.end_headers()
                    return
            else:
                print("ID utente Telegram non trovato nel client_reference_id.")
                self.send_response(400)
                self.end_headers()
                return

        # Risposta per tutti gli altri eventi
        self.send_response(200)
        self.end_headers()
        return
