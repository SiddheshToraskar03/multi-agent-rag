# agents/schema_agent.py
from typing import Dict, Any, List
import json
import re

from backend.llm import call_llm
from backend.schema_description import SCHEMA_DESCRIPTION


class SchemaAgent:
    """Identifies relevant tables and columns for a question using Gemini API."""

    def run(self, question: str) -> Dict[str, Any]:
        """
        Analyze question and identify relevant tables and columns.
        
        Args:
            question: Natural language question
            
        Returns:
            Dictionary with tables and columns information
        """
        system_prompt = (
            "You are a schema reasoning agent. "
            "Given a database schema and a natural language question, "
            "select the relevant tables and columns needed to answer the question. "
            "Return a concise JSON with keys: tables (list of table names), "
            "columns (dict of table -> list of columns). "
            "Example format: {\"tables\": [\"customers\", \"sales\"], \"columns\": {\"customers\": [\"customer_id\", \"country\"], \"sales\": [\"amount\", \"sale_date\"]}}"
        )
        
        user_prompt = f"Schema:\n{SCHEMA_DESCRIPTION}\n\nQuestion:\n{question}\n\nReturn ONLY valid JSON, no additional text."
        
        try:
            text = call_llm(system_prompt, user_prompt)
            text = text.strip()
            text = re.sub(r'^```json\s*', '', text)
            text = re.sub(r'^```\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            text = text.strip()
            
            result = json.loads(text)
        
            if "tables" not in result:
                result["tables"] = []
            if "columns" not in result:
                result["columns"] = {}
                
            return result
        except Exception as e:
            return {
                "tables": ["customers", "employees", "projects", "sales"],
                "columns": {}
            }
