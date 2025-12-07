# backend/schema_description.py
"""
Database schema description for the RAG system.
This is used by agents to understand the database structure.
"""

SCHEMA_DESCRIPTION = """
PostgreSQL Database Schema:

Table: customers
- customer_id (SERIAL PRIMARY KEY): Unique customer identifier
- first_name (VARCHAR(60)): Customer's first name
- last_name (VARCHAR(60)): Customer's last name
- email (VARCHAR(150) UNIQUE): Customer's email address
- city (VARCHAR(100)): Customer's city
- country (VARCHAR(100)): Customer's country
- created_at (TIMESTAMP): Customer registration timestamp

Table: projects
- project_id (SERIAL PRIMARY KEY): Unique project identifier
- project_name (VARCHAR(150)): Name of the project
- start_date (DATE): Project start date
- end_date (DATE): Project end date
- status (VARCHAR(50)): Project status

Table: employees
- employee_id (SERIAL PRIMARY KEY): Unique employee identifier
- first_name (VARCHAR(60)): Employee's first name
- last_name (VARCHAR(60)): Employee's last name
- email (VARCHAR(150) UNIQUE): Employee's email address
- hire_date (DATE): Employee hire date
- department (VARCHAR(100)): Employee department
- project_id (INT): Foreign key referencing projects(project_id)

Table: sales
- sale_id (SERIAL PRIMARY KEY): Unique sale identifier
- customer_id (INT): Foreign key referencing customers(customer_id)
- employee_id (INT): Foreign key referencing employees(employee_id)
- project_id (INT): Foreign key referencing projects(project_id)
- amount (NUMERIC(12,2)): Sale amount
- sale_date (DATE): Date of the sale
- channel (VARCHAR(50)): Sales channel
- notes (TEXT): Additional notes

Relationships:
- sales.customer_id -> customers.customer_id
- sales.employee_id -> employees.employee_id
- sales.project_id -> projects.project_id
- employees.project_id -> projects.project_id
"""

