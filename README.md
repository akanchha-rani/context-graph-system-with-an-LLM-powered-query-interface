# 🚀 Context Graph System with LLM-Powered Query Interface

A full-stack AI application that integrates graph-based data modeling with a Large Language Model (LLM) to enable natural language querying over structured enterprise data.


## 📌 Overview

This project demonstrates how context graphs + LLMs can be combined to build intelligent systems that understand and respond to user queries in natural language.

Modern AI systems increasingly combine LLMs with graph-based structures to improve reasoning and contextual understanding .


## ✨ Features

💬 ChatGPT-like interface using Flask

🧠 LLM-powered query interpretation (Groq API)

🔗 Graph-based data modeling using NetworkX

🌐 Interactive graph visualization using Pyvis

🔴 Dynamic node highlighting based on user queries

⚡ Real-time query execution and visualization updates


## 🏗️ Architecture

User Query (UI)
      ↓

LLM (Groq - Query Understanding)
      ↓

Graph Engine (NetworkX)
      ↓

Response + Highlighted Graph (Pyvis)


## 🛠️ Tech Stack

| Category           | Technology            | Purpose                                    |
| ------------------ | --------------------- | ------------------------------------------ |
| Backend            | Flask                 | Web framework for handling routes and APIs |
| LLM API            | Groq (LLaMA 3.1)      | Natural language query understanding       |
| Graph Processing   | NetworkX              | Graph creation and relationship modeling   |
| Visualization      | Pyvis                 | Interactive graph visualization            |
| Frontend           | HTML, CSS, JavaScript | User interface (chat + graph panel)        |
| Environment Config | python-dotenv         | Managing API keys securely                 |
| Server             | Gunicorn              | Production WSGI server for deployment      |
| Deployment         | Render                | Cloud hosting platform                     |


## 📂 Project Structure

.

├── app.py                  # Flask app + LLM integration

├── fde_graph.py            # Graph creation logic

├── templates/

│   └── index.html          # UI (chat + graph panel)

├── static/

│   └── sap_graph.html      # Generated graph visualization

├── requirements.txt

├── Procfile

└── .env


## 🎯 Key Highlights

Converts natural language → structured graph queries

Enables non-technical users to interact with graph data

Demonstrates Graph + LLM integration (GraphRAG concept)

Provides visual + interactive insights


## 📸 Screenshots

<img width="1440" height="814" alt="Screenshot 2026-03-26 at 6 55 47 PM" src="https://github.com/user-attachments/assets/b201cefa-6bdd-4b88-81c2-2551dd29d08f" />
