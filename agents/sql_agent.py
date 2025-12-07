# agents/sql_agent.py
from typing import Any, Dict, Tuple
import re

from backend.llm import call_llm
from backend.schema_description import SCHEMA_DESCRIPTION


class SqlAgent:
    """Generates PostgreSQL SQL queries from natural language questions using Gemini API."""

    def build(self, question: str, schema_info: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Generate SQL query from question and schema info.
        
        Args:
            question: Natural language question
            schema_info: Schema information from SchemaAgent
            
        Returns:
            Tuple of (SQL query string, parameters dict)
        """
        system_prompt = (
            "You are a PostgreSQL SQL generator. "
            "Given a question and the database schema, generate a single safe SELECT query. "
            "Rules:\n"
            "- Use only SELECT (no INSERT/UPDATE/DELETE/DDL).\n"
            "- Use table names and columns exactly as in the schema.\n"
            "- Handle temporal phrases like 'last year', 'this year', 'Q1 2023' using CURRENT_DATE and date_trunc.\n"
            "- For 'last year', use: sale_date >= DATE_TRUNC('year', CURRENT_DATE - INTERVAL '1 year') AND sale_date < DATE_TRUNC('year', CURRENT_DATE)\n"
            "- For 'this year', use: sale_date >= DATE_TRUNC('year', CURRENT_DATE)\n"
            "- If aggregation is needed, use GROUP BY.\n"
            "- Use proper JOINs when accessing related tables.\n"
            "- Return ONLY the SQL query, no explanation, no markdown, no backticks."
        )
        
        schema_context = f"Relevant tables: {schema_info.get('tables', [])}\n"
        if schema_info.get('columns'):
            schema_context += f"Relevant columns: {schema_info['columns']}\n"
        
        user_prompt = (
            f"Schema:\n{SCHEMA_DESCRIPTION}\n\n"
            f"{schema_context}\n"
            f"Question: {question}\n\n"
            f"Generate the SQL query:"
        )
        
        try:
            sql = call_llm(system_prompt, user_prompt).strip()
            
            sql = re.sub(r'^```sql\s*', '', sql, flags=re.IGNORECASE)
            sql = re.sub(r'^```\s*', '', sql)
            sql = re.sub(r'\s*```$', '', sql)
            sql = sql.strip()
            
            sql = sql.rstrip(';').strip()
            
            if not sql.upper().startswith("SELECT"):
                raise ValueError("Generated SQL is not a SELECT query.")
            
            if sql.count(';') > 0:
                sql = sql.split(';')[0].strip()
            
            return sql, {}
            
        except Exception as e:
            raise ValueError(f"SQL Generation Fails: {str(e)}")
