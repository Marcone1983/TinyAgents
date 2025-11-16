// Inizializzazione Telegram Web App
const tg = window.Telegram.WebApp;

// Configurazione iniziale
const AGENTS = {
    "meme_persona": {
        "description": "Trasforma una tua idea in una caption per un meme virale.",
        "emoji": "😂"
    },
    "viral_pitch": {
        "description": "Scrivi un pitch freddo e conciso per LinkedIn.",
        "emoji": "💼"
    },
    "roast_generator": {
        "description": "Fornisci un argomento e io lo 'roasterò' simpaticamente.",
        "emoji": "🔥"
    },
    "email_writer": {
        "description": "Scrivi email professionali e persuasive.",
        "emoji": "📧"
    },
    "tweet_generator": {
        "description": "Crea tweet virali e accattivanti.",
        "emoji": "🐦"
    },
    "product_description": {
        "description": "Scrivi descrizioni di prodotti per e-commerce.",
        "emoji": "🛍️"
    },
    "story_starter": {
        "description": "Genera l'inizio di una storia affascinante.",
        "emoji": "📖"
    },
    "code_explainer": {
        "description": "Spiega concetti di programmazione in modo semplice.",
        "emoji": "💻"
    },
    "motivational_quote": {
        "description": "Genera citazioni motivazionali personalizzate.",
        "emoji": "⭐"
    },
    "seo_optimizer": {
        "description": "Ottimizza il testo per i motori di ricerca.",
        "emoji": "🔍"
    }
};

let currentAgent = null;
let chatHistory = [];

// Inizializzazione
document.addEventListener('DOMContentLoaded', () => {
    tg.ready();
    tg.expand();
    
    // Imposta il colore di sfondo
    tg.setBackgroundColor("#667eea");
    
    // Carica i crediti
    loadCredits();
    
    // Renderizza gli agenti
    renderAgents();
});

// Funzione per caricare i crediti
async function loadCredits() {
    try {
        const userId = tg.initDataUnsafe?.user?.id;
        if (!userId) {
            document.getElementById('creditsAmount').textContent = '0';
            return;
        }
        
        // Simula il caricamento dei crediti (in produzione, chiamerebbe l'API)
        document.getElementById('creditsAmount').textContent = '0';
    } catch (error) {
        console.error('Errore nel caricamento dei crediti:', error);
        document.getElementById('creditsAmount').textContent = '0';
    }
}

// Funzione per renderizzare gli agenti
function renderAgents() {
    const grid = document.getElementById('agentsGrid');
    grid.innerHTML = '';
    
    Object.entries(AGENTS).forEach(([key, agent]) => {
        const card = document.createElement('div');
        card.className = 'agent-card';
        card.innerHTML = `
            <div style="font-size: 24px; margin-bottom: 8px;">${agent.emoji}</div>
            <div class="agent-name">${key.replace(/_/g, ' ').toUpperCase()}</div>
            <div class="agent-description">${agent.description}</div>
        `;
        card.onclick = () => selectAgent(key);
        grid.appendChild(card);
    });
}

// Funzione per selezionare un agente
function selectAgent(agentName) {
    currentAgent = agentName;
    chatHistory = [];
    
    document.getElementById('agentsView').style.display = 'none';
    document.getElementById('chatView').classList.add('active');
    document.getElementById('chatTitle').textContent = agentName.replace(/_/g, ' ').toUpperCase();
    document.getElementById('chatMessages').innerHTML = '';
    document.getElementById('userInput').value = '';
    document.getElementById('userInput').focus();
}

// Funzione per tornare agli agenti
function backToAgents() {
    currentAgent = null;
    chatHistory = [];
    
    document.getElementById('agentsView').style.display = 'block';
    document.getElementById('chatView').classList.remove('active');
    document.getElementById('chatMessages').innerHTML = '';
}

// Funzione per inviare un messaggio
async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Aggiungi il messaggio dell'utente alla chat
    addMessageToChat(message, 'user');
    input.value = '';
    
    // Mostra il caricamento
    showLoading();
    
    try {
        // Simula la risposta dell'agente (in produzione, chiamerebbe l'API)
        // Per ora, mostra un messaggio di placeholder
        const response = await simulateAgentResponse(currentAgent, message);
        removeLoading();
        addMessageToChat(response, 'bot');
    } catch (error) {
        removeLoading();
        addMessageToChat('Errore nella risposta. Riprova.', 'bot');
    }
}

// Funzione per aggiungere un messaggio alla chat
function addMessageToChat(text, sender) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageEl = document.createElement('div');
    messageEl.className = `message ${sender}`;
    messageEl.textContent = text;
    messagesDiv.appendChild(messageEl);
    
    // Scroll automatico
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    chatHistory.push({ text, sender });
}

// Funzione per mostrare il caricamento
function showLoading() {
    const messagesDiv = document.getElementById('chatMessages');
    const loadingEl = document.createElement('div');
    loadingEl.id = 'loading';
    loadingEl.className = 'loading';
    loadingEl.innerHTML = '<div class="spinner"></div> Elaborazione in corso...';
    messagesDiv.appendChild(loadingEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Funzione per rimuovere il caricamento
function removeLoading() {
    const loading = document.getElementById('loading');
    if (loading) loading.remove();
}

// Funzione per simulare la risposta dell'agente
async function simulateAgentResponse(agent, message) {
    // In produzione, questo chiamerebbe l'API del bot Telegram
    // Per ora, ritorna un messaggio di placeholder
    return `Risposta da ${agent}: "${message}" - Questa è una risposta simulata. In produzione, chiamerebbe l'API del bot.`;
}

// Funzione per acquistare crediti
function buyCredits() {
    // Apri il link di pagamento Stripe
    const userId = tg.initDataUnsafe?.user?.id;
    if (userId) {
        // In produzione, questo chiamerebbe l'API per ottenere il link di pagamento
        tg.openLink(`https://t.me/TinyAgents_bot?start=buy`);
    }
}

// Gestione della pressione di Enter nel campo di input
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('userInput');
    if (input) {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
});
