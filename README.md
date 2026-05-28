# 🚨 RoadSoS — AI Road Emergency Assistant

> Road Safety Hackathon 2026 | IIT Madras CoERS | Problem Statement: RoadSoS

**RoadSoS** is a conversational AI that triages road accidents and connects victims to the nearest emergency services in seconds — hospitals, ambulances, police, and towing — with offline fallback and global emergency number support.

---

## 🔴 Live Demo
🔗 [Live App on Hugging Face Spaces](#) *(link after deployment)*

---

## 🎯 Problem
53 people die every hour on Indian roads. The **golden hour** — first 60 minutes after an accident — determines survival. Bystanders lose 10–15 minutes searching for the right number or nearest hospital.

## ✅ Solution
RoadSoS eliminates that delay:
1. Describe the accident in plain text
2. AI classifies severity → decides which service to call FIRST
3. Nearest hospitals, police, ambulances shown on live map
4. First-aid instructions from RAG knowledge base
5. Works offline — SQLite cache stores last-known services

---

## 🏗️ Architecture

```
User (browser)
      │
      ▼
Flask REST API
      │
   ┌──┴─────────────────┐
   │                    │
AI Layer           Places Service
LangChain          Google Places API
Gemini 2.0 Flash   (hospitals, police,
FAISS + HuggingFace ambulance, towing)
(first-aid RAG)         │
   │                    │
   └────────┬───────────┘
            │
      SQLite offline cache
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Gemini 2.0 Flash |
| RAG Pipeline | LangChain + FAISS |
| Embeddings | HuggingFace (local, offline-capable) |
| Backend | Flask + REST API |
| Maps | Google Maps JS + Places API (New) |
| Offline | SQLite cache |
| Deploy | Hugging Face Spaces |

---

## 📊 Evaluation Criteria Coverage

| Criterion | Implementation |
|---|---|
| Reliability & data accuracy | Google Places API — live verified data |
| Number of contacts fetched | Places Details API — phone for every result |
| Offline functionality | SQLite cache + HuggingFace local embeddings |
| Innovation | Severity triage AI, RAG first-aid, priority routing |
| Global applicability | 20+ country emergency numbers, global Places API |

---

## 🚀 Setup

```bash
git clone https://github.com/Rsharan622244/roadsos
cd roadsos
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
python build_knowledge_base.py
python app.py
```

Open http://localhost:5000

---

## 📡 API Reference

### POST /nearby
```json
Request:  { "description": "Car crash, driver unconscious", "lat": 17.38, "lng": 78.48 }
Response: { "severity": "CRITICAL", "services": {...}, "first_aid_tip": "..." }
```

### POST /chat
```json
Request:  { "question": "How do I do CPR?" }
Response: { "answer": "...", "sources": ["first_aid.txt"] }
```

---

## 👤 Team
**Rachuri Sharan** — NIT Andhra Pradesh, ECE  
rachurisharan0@gmail.com | [GitHub](https://github.com/Rsharan622244)

---
*Road Safety Hackathon 2026 | IIT Madras Centre of Excellence for Road Safety*
