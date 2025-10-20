# 🤖 QueryCraft: The Text-to-SQL BI Tool

**QueryCraft** is a self-service Business Intelligence (BI) tool that allows non-technical users to query a database using plain English. It leverages a Generative AI model to translate natural language into executable SQL queries, democratizing data access for everyone.

This project is built as a full-stack Python application, featuring a **FastAPI** backend for the AI and database logic, and a **Streamlit** frontend for a clean, interactive user experience.

![QueryCraft Demo](https://i.imgur.com/your-demo-gif.gif) 
*(You should record a GIF of your app working and place it here)*

---

### 🚀 The Problem & Opportunity

In most companies, data is locked behind a "technical wall." Business users in sales, marketing, or finance need insights but don't know SQL. They must file a ticket with a data analyst, creating a slow and expensive bottleneck.

**QueryCraft** solves this by providing a simple chat interface that acts as an AI data analyst, translating questions like "What were our top 5 best-selling albums last year?" directly into SQL.

---

### 🛠️ Tech Stack & Architecture

* **Frontend (UI):** [Streamlit](https://streamlit.io/)
* **Backend (API):** [FastAPI](https://fastapi.tiangolo.com/)
* **Gen AI (Text-to-SQL):** [ctransformers](https://github.com/marella/ctransformers) (running `sql-coder-7b-GGUF`)
* **Database (Source):** [SQLite](https://www.sqlite.org/index.html) (using the classic "Chinook" music store database)
* **Validation:** [Pydantic](https://docs.pydantic.dev/)

**Architecture:**
`Streamlit (UI)` ➔ `FastAPI (Backend)` ➔ `Gen AI Model (Translate)` ➔ `SQLite (Execute Query)`

---

### 🏁 Getting Started

Follow these steps to set up and run the project locally.

#### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/querycraft-text-to-sql.git](https://github.com/your-username/querycraft-text-to-sql.git)
cd querycraft-text-to-sql
