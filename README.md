# MDS Lab 1 - Weather & TODO Apps

Aplicații demonstrative pentru laboratorul MDS.

## Aplicația Meteo

Folosește API-ul [Open-Meteo](https://open-meteo.com/) (fără autentificare) pentru a afișa vremea curentă pentru un oraș.

```bash
python main.py "București"
```

## Aplicația TODO

Aplicație TODO list interactivă cu comenzi în REPL.

```bash
python todo.py
```

Comenzi disponibile: `add`, `list [pending|done]`, `done <id>`, `delete <id>`, `clear`, `help`, `exit`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS/WSL
pip install -r requirements.txt
```
