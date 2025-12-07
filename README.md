# **Multi-Agent RAG System for Natural Language Querying of PostgreSQL**

This project implements a multi-agent Retrieval-Augmented Generation (RAG) system that converts natural‑language questions into SQL queries, executes them on PostgreSQL, and returns both answers and intermediate reasoning. The system uses Google Gemini API for intelligent query understanding and generation.

---

## Features
- Natural‑language question understanding using Google Gemini API
- Schema‑aware table/column selection  
- SQL query generation (aggregations, filters, joins, date ranges)  
- Safe SQL execution  
- Human‑readable synthesized answer  
- Debug output (SQL, rows, schema reasoning)  
- Simple web UI for querying  
- Error handling for missing schema, SQL errors, and empty results  

---

## Project Structure
```
multi-rag/
├── agents/
│   ├── __init__.py
│   ├── schema_agent.py
│   ├── sql_agent.py
│   ├── retriever_agent.py
│   └── synthesizer_agent.py
│
├── backend/
│   ├── __init__.py
│   ├── db.py
│   ├── llm.py
│   ├── schema_description.py
│   ├── pipeline.py
│   └── main.py
│
├── postgres_db/
│   ├── schema.sql
│   ├── customers.csv
│   ├── employees.csv
│   ├── projects.csv
│   └── sales.csv
│
├── web/
│   └── index.html
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Setup Instructions

## 1️ Install Python dependencies
```
pip install -r requirements.txt
```

## 1.5️ Set up Google Gemini API Key

Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

### Recommended: Using .env file

Create a `.env` file in the project root directory with:
```
GEMINI_API_KEY=your-api-key-here
```

The application will automatically load the API key from this file. **Important:** Make sure to add `.env` to `.gitignore` to keep your API key secure!

### Alternative: Environment Variable

You can also set it as an environment variable:

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

## 2️ Start PostgreSQL (Docker)
```
docker compose up -d
```

## 3️ Load database schema
```
docker exec -i multi-rag-db-1 psql -U raguser -d ragdb < postgres_db/schema.sql
```

## 4️ Load CSV data

You can load CSV data using one of these methods:

### Method 1: Using Docker exec
```bash
# Copy CSV files into the container
docker cp postgres_db/customers.csv multi-rag-db:/tmp/customers.csv
docker cp postgres_db/employees.csv multi-rag-db:/tmp/employees.csv
docker cp postgres_db/projects.csv multi-rag-db:/tmp/projects.csv
docker cp postgres_db/sales.csv multi-rag-db:/tmp/sales.csv

# Load data into database
docker exec -i multi-rag-db psql -U raguser -d ragdb -c "\copy customers(customer_id,first_name,last_name,email,city,country,created_at) FROM '/tmp/customers.csv' DELIMITER ',' CSV HEADER;"

docker exec -i multi-rag-db psql -U raguser -d ragdb -c "\copy projects(project_id,project_name,start_date,end_date,status) FROM '/tmp/projects.csv' DELIMITER ',' CSV HEADER;"

docker exec -i multi-rag-db psql -U raguser -d ragdb -c "\copy employees(employee_id,first_name,last_name,email,hire_date,department,project_id) FROM '/tmp/employees.csv' DELIMITER ',' CSV HEADER;"

docker exec -i multi-rag-db psql -U raguser -d ragdb -c "\copy sales(sale_id,customer_id,employee_id,project_id,amount,sale_date,channel,notes) FROM '/tmp/sales.csv' DELIMITER ',' CSV HEADER;"
```

### Method 2: Using psql directly
```bash
# Connect to the database
docker exec -it multi-rag-db psql -U raguser -d ragdb

# Then run these commands inside psql:
\copy customers(customer_id,first_name,last_name,email,city,country,created_at) FROM '/docker-entrypoint-initdb.d/customers.csv' DELIMITER ',' CSV HEADER;
\copy projects(project_id,project_name,start_date,end_date,status) FROM '/docker-entrypoint-initdb.d/projects.csv' DELIMITER ',' CSV HEADER;
\copy employees(employee_id,first_name,last_name,email,hire_date,department,project_id) FROM '/docker-entrypoint-initdb.d/employees.csv' DELIMITER ',' CSV HEADER;
\copy sales(sale_id,customer_id,employee_id,project_id,amount,sale_date,channel,notes) FROM '/docker-entrypoint-initdb.d/sales.csv' DELIMITER ',' CSV HEADER;
```

## 5️ Start Backend API

**Important:** Make sure you have created a `.env` file with your `GEMINI_API_KEY` or set it as an environment variable before starting the backend.

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

**Note:** If you see an error about `GEMINI_API_KEY` not being set, make sure you've exported the environment variable in your current terminal session.

## 6️ Open Web UI

Open the `web/index.html` file in your web browser, or serve it using a simple HTTP server:

```bash
# Using Python
python -m http.server 8080

# Then open http://localhost:8080/web/index.html in your browser
```

Or simply open `web/index.html` directly in your browser (file:// protocol).

**Note:** Make sure the backend API is running on `http://localhost:8000` before using the web UI.

---

## Agent Overview

### **SchemaAgent**
Identifies relevant tables/columns for a question using Google Gemini API.
- Uses Gemini to analyze the question against the database schema
- Returns JSON with relevant tables and columns
- Handles complex natural language understanding

### **SQLAgent (SQL Generator Agent)**
Generates PostgreSQL SQL queries using Google Gemini API.
- Converts natural language questions to SQL
- Handles aggregations (SUM, AVG, COUNT)
- Supports filters, joins, and temporal references ("last year", "this year", "Q1 2023")
- Ensures only SELECT queries are generated (safety check)

### **RetrieverAgent**
Executes SQL queries using psycopg2 and returns results.
- Safely executes generated SQL queries
- Returns rows as list of dictionaries
- Returns column names for reference

### **SynthesizerAgent**
Generates natural‑language answers from query results using Google Gemini API.
- Converts SQL results into human-readable responses
- Handles empty result sets with helpful messages
- Provides summaries for large result sets

### **RagPipeline**
Connects all agents:  

User question 
SchemaAgent 
SqlAgent 
RetrieverAgent 
SynthAgent 
Final answer + intermediate reasoning

---

## API Example

## POST `/ask`
Request:
```json
{ "question": "total sales last year" }
```

Response:
```json
{
  "question": "total sales by country last year",
  "answer": "Based on the query results, I found sales data for multiple countries from last year. The total sales amounts vary by country...",
  "intermediate": {
    "schema": {
      "tables": ["sales", "customers"],
      "columns": {
        "sales": ["amount", "sale_date"],
        "customers": ["country"]
      }
    },
    "sql": "SELECT c.country, SUM(s.amount) AS total_amount FROM sales s JOIN customers c ON s.customer_id = c.customer_id WHERE s.sale_date >= DATE_TRUNC('year', CURRENT_DATE - INTERVAL '1 year') AND s.sale_date < DATE_TRUNC('year', CURRENT_DATE) GROUP BY c.country ORDER BY total_amount DESC",
    "params": {},
    "columns": ["country", "total_amount"],
    "rows": [
      { "country": "Aruba", "total_amount": 2915.08 },
      { "country": "Azerbaijan", "total_amount": 1831.83 },
      { "country": "Barbados", "total_amount": 8882.60 }
    ],
    "error": null
  }
}
```

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey) | Yes |

### Setting Environment Variables

**Recommended: Using .env file (default)**
- Create a `.env` file in the project root
- Add: `GEMINI_API_KEY=your-key`
- The application automatically loads it using `python-dotenv`
- **Important:** Add `.env` to `.gitignore` to keep your API key secure!

**Alternative: Environment Variable**
- Windows PowerShell: `$env:GEMINI_API_KEY="your-key"`
- Windows CMD: `set GEMINI_API_KEY=your-key`
- Linux/Mac: `export GEMINI_API_KEY="your-key"`

---

## Troubleshooting

### Backend fails to start with "GEMINI_API_KEY not set"
- Make sure you've set the environment variable in the same terminal session where you're running uvicorn
- Verify the variable is set: `echo $GEMINI_API_KEY` (Linux/Mac) or `echo $env:GEMINI_API_KEY` (PowerShell)

### Database connection errors
- Ensure Docker container is running: `docker ps`
- Check if PostgreSQL is accessible: `docker exec -it multi-rag-db psql -U raguser -d ragdb -c "SELECT 1;"`
- Verify connection settings in `backend/db.py` match docker-compose.yml

### SQL generation errors
- Check that the database schema is loaded correctly
- Verify CSV data is loaded (run a test query manually)
- Check the intermediate output in the API response for SQL errors

### Gemini API errors
- Verify your API key is valid and has sufficient quota
- Check your internet connection
- Review the error message in the API response

---

## System Architecture

```
User Query
    ↓
Schema Agent
    ↓ 
SQL Agent
    ↓
Retriever Agent
    ↓
Synthesizer Agent
    ↓
Final Answer + Intermediate Debug Info
```

---

## Supported Query Types

The system supports various types of natural language queries:

- **Direct data lookup**: "Show me all customers"
- **Filtering**: "Find employees in the Engineering department"
- **Aggregations**: "What is the total sales amount?", "Average sales by country"
- **Table joins**: "Show sales with customer information"
- **Temporal references**: "Sales from last year", "Projects started in Q1 2023"
- **Complex queries**: "Total sales by country for last year"

---

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL 15
- **LLM**: Google Gemini Pro
- **Python Libraries**: 
  - `google-generativeai` - Gemini API integration
  - `psycopg2-binary` - PostgreSQL adapter
  - `fastapi` - Web framework
  - `uvicorn` - ASGI server

---

---

## Quick Test Sequence

Run these in order to quickly verify all features:

1. **Direct Lookup:** "Show me all customers"/"Display all projects"
2. **Filtering:** "Find customers from USA"/"List projects with status 'Active'"
3. **Count:** "How many customers are there?"/"Show me the sum of all sales"
4. **Sum:** "What is the total sales amount?"/What is the average sale amount?"
5. **Join:** "Show sales with customer information"/"Get sales with customer country information"
6. **Temporal:** "Total sales last year"/"Show customers created in 2023"
7. **Combined:** "Total sales by country last year"/"Average sale amount by channel"

---