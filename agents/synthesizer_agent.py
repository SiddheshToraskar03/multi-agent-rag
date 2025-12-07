# agents/synthesizer_agent.py
from typing import Any, Dict, List
import json

from backend.llm import call_llm


class SynthAgent:
    """Generates natural language answers from query results using Gemini API."""

    def answer(self, question: str, rows: List[Dict[str, Any]], sql: str = "") -> str:
        """
        Generate natural language answer from query results.
        
        Args:
            question: Original natural language question
            rows: Query result rows
            sql: Generated SQL query (optional, for context)
            
        Returns:
            Natural language answer
        """
        if not rows:
            system_prompt = (
                "You are a data analyst. "
                "Given a natural language question and an executed SQL query that returned no results, "
                "write a clear, helpful message explaining that no matching records were found. "
                "Suggest how the user might rephrase their question or what they might be looking for."
            )
            user_prompt = f"Question: {question}\n\nSQL: {sql}\n\nNo results were returned."
            return call_llm(system_prompt, user_prompt)
        
        system_prompt = (
            "You are a data analyst. "
            "Given a natural language question, an executed SQL query, and its result rows, "
            "write a clear, concise answer in plain English. "
            "Summarize the key findings and present the data in a user-friendly way. "
            "If there are many rows, provide a summary and mention the total count."
        )
        
        preview_rows = rows[:50]
        
        user_prompt = (
            f"Question: {question}\n\n"
            f"SQL Query: {sql}\n\n"
            f"Result rows (JSON format, {len(rows)} total rows):\n{json.dumps(preview_rows, indent=2, default=str)}"
        )
        
        if len(rows) > 50:
            user_prompt += f"\n\nNote: Showing first 50 of {len(rows)} total rows."
        
        try:
            return call_llm(system_prompt, user_prompt)
        except Exception as e:
            if len(rows) == 1:
                return f"Found 1 result: {rows[0]}"
            return f"Found {len(rows)} results for your question."
