# Come Aggiungere Nuovi Agenti

Questa guida spiega come aggiungere nuovi agenti AI al sistema TinyAgents.

## Passaggi

### 1. Modifica il File `api/telegram.py`

Apri il file `api/telegram.py` e trova la sezione **"DEFINIZIONE DEI TINY AGENTS"**:

```python
AGENTS = {
    "meme_persona": {
        "description": "Trasforma una tua idea in una caption per un meme virale.",
        "system_prompt": "Sei un generatore di meme..."
    },
    # ... altri agenti ...
}
```

### 2. Aggiungi il Nuovo Agente

Aggiungi un nuovo agente al dizionario `AGENTS`:

```python
"my_new_agent": {
    "description": "Descrizione breve del tuo agente",
    "system_prompt": "Prompt di sistema per l'LLM. Questo definisce il comportamento dell'agente."
}
```

### 3. Aggiorna la Mini App (Opzionale)

Se desideri che il nuovo agente appaia nella Mini App, aggiungi anche il nuovo agente al file `main.js`:

```javascript
const AGENTS = {
    // ... altri agenti ...
    "my_new_agent": {
        "description": "Descrizione breve del tuo agente",
        "emoji": "🎯"  // Scegli un emoji appropriato
    }
};
```

### 4. Commit e Push

Esegui il commit e il push dei cambiamenti:

```bash
git add api/telegram.py main.js
git commit -m "FEAT: Aggiunto nuovo agente 'my_new_agent'"
git push origin main
```

Vercel attiverà automaticamente un nuovo deployment.

### 5. Test

1. Vai su Telegram e invia il comando:
   ```
   /my_new_agent il tuo prompt qui
   ```
2. Il bot dovrebbe rispondere con la risposta dell'agente.

## Esempi di Agenti

### Agente per Generare Titoli SEO

```python
"seo_title_generator": {
    "description": "Genera titoli ottimizzati per i motori di ricerca.",
    "system_prompt": "Sei un esperto SEO. Genera 5 titoli brevi (max 60 caratteri) e accattivanti per un articolo basato sul tema fornito dall'utente. Ogni titolo deve contenere parole chiave pertinenti e essere clickable."
}
```

### Agente per Scrivere Descrizioni di Prodotti

```python
"product_reviewer": {
    "description": "Scrivi recensioni di prodotti professionali.",
    "system_prompt": "Sei un critico di prodotti. Scrivi una breve recensione (max 150 parole) basata sulla descrizione del prodotto fornita dall'utente. Includi pro, contro e una valutazione finale."
}
```

### Agente per Generare Hashtag

```python
"hashtag_generator": {
    "description": "Genera hashtag virali per i social media.",
    "system_prompt": "Sei un esperto di social media. Genera 10-15 hashtag virali e pertinenti basati sul tema fornito dall'utente. Includi hashtag di tendenza e hashtag di nicchia."
}
```

## Best Practices

1. **Descrizione Chiara**: La descrizione deve essere breve e chiara, in modo che gli utenti capiscano cosa fa l'agente.
2. **Prompt Specifico**: Il prompt di sistema deve essere dettagliato e specifico per ottenere i migliori risultati.
3. **Test Approfondito**: Testa il nuovo agente con vari input per assicurarti che funzioni correttamente.
4. **Nomi Coerenti**: Usa nomi di agenti coerenti e facili da ricordare (es. `snake_case`).

## Limitazioni

- **Lunghezza del Prompt**: Il prompt di sistema non deve essere troppo lungo (max 500 caratteri consigliati).
- **Token Limit**: Groq ha un limite di token. Assicurati che il prompt e la risposta non superino il limite.
- **Costo**: Ogni utilizzo di un agente costa 1 credito all'utente.

## Supporto

Per problemi o domande, contatta il team di TinyAgents.
