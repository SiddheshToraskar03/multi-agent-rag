--- schema.sql : PostgreSQL schema for RAG dataset


CREATE TABLE IF NOT EXISTS customers (
  customer_id SERIAL PRIMARY KEY,
  first_name VARCHAR(60),
  last_name VARCHAR(60),
  email VARCHAR(150) UNIQUE,
  city VARCHAR(100),
  country VARCHAR(100),
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS projects (
  project_id SERIAL PRIMARY KEY,
  project_name VARCHAR(150),
  start_date DATE,
  end_date DATE,
  status VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS employees (
  employee_id SERIAL PRIMARY KEY,
  first_name VARCHAR(60),
  last_name VARCHAR(60),
  email VARCHAR(150) UNIQUE,
  hire_date DATE,
  department VARCHAR(100),
  project_id INT REFERENCES projects(project_id)
);

CREATE TABLE IF NOT EXISTS sales (
  sale_id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE,
  employee_id INT REFERENCES employees(employee_id) ON DELETE SET NULL,
  project_id INT REFERENCES projects(project_id),
  amount NUMERIC(12,2),
  sale_date DATE,
  channel VARCHAR(50),
  notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_sales_sale_date ON sales(sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_employees_project ON employees(project_id);
