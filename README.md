# Python Internship Tasks

This repository contains the completed tasks for the Python Internship. The project is divided into two main tasks: an OOP-based Algo Trader and a condition-based RAG Agent System using PostgreSQL.

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites & Installation](#prerequisites--installation)
    - [Virtual Environment Setup](#virtual-environment-setup)
    - [Environment Variables](#environment-variables)
    - [Installing Packages](#installing-packages)
- [Task 1: OOP Algo Trader](#task-1-oop-algo-trader)
- [Task 2: RAG Agent System](#task-2-rag-agent-system)

## Project Overview

### Task 1: Algo Trader
An Object-Oriented Programming (OOP) class-based implementation of an algorithmic trading system.
- **Main Script**: `Task_1/task1.py`
- **Initial Testing**: `Task_1/Intern_Python_Task_1.ipynb`

### Task 2: RAG Agent System
A condition-based Retrieval-Augmented Generation (RAG) agent system that answers questions about mobile phone specifications.
- **Data Source**: Scraped from GSMArena using Selenium.
- **Processing**: Data preprocessed with Excel and Pandas.
- **Storage**: Stored in a PostgreSQL database using SQLAlchemy.
- **Architecture**: Modular design with separate components for database (`db.py`), helpers (`helpers.py`), agents (`agents.py`), and RAG logic (`rag.py`).
- **Interface**: FastAPI backend (`main.py`) and Streamlit frontend (`streamlit_app.py`).

---

## Prerequisites & Installation

### Virtual Environment Setup

It is recommended to use a virtual environment to manage dependencies.

**For macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Environment Variables

1. Create a file named `.env` in the root directory.
2. Add your PostgreSQL database connection string:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
```
*Replace `username`, `password`, and `your_database_name` with your actual credentials.*

### Installing Packages

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

**Key Packages Used:**
- `fastapi`, `uvicorn` (Backend API)
- `streamlit` (Frontend UI)
- `sqlalchemy`, `psycopg2` (Database)
- `pandas`, `numpy` (Data Processing)
- `selenium`, `undetected-chromedriver` (Web Scraping)
- `yfinance` (Financial Data for Task 1)

---

## Task 1: OOP Algo Trader

This module implements an algorithmic trading strategy using OOP principles.

**How to run:**
Execute the main Python script from the root directory:

```bash
python3 Task_1/task1.py
```

---

## Task 2: RAG Agent System

This system uses a RAG approach to answer user queries based on the stored mobile phone data.

### 1. Run the Backend (FastAPI)
Start the FastAPI server to handle requests and run the agents.

```bash
uvicorn main:app --reload
```
*The API will be available at `http://127.0.0.1:8000`.*

### 2. Run the User Interface (Streamlit)
Launch the Streamlit app to interact with the project via a web interface.

```bash
streamlit run streamlit_app.py
```

### 3. Testing with Postman (Optional)
You can also test the API directly using Postman by sending `POST` requests to `http://127.0.0.1:8000/ask` with a JSON body:
```json
{
  "question": "What are the specs of Samsung Galaxy S25 FE?"
}
```