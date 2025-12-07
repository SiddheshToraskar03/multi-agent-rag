# backend/pipeline.py

from typing import Any, Dict

from agents.schema_agent import SchemaAgent
from agents.sql_agent import SqlAgent
from agents.retriever_agent import RetrieverAgent
from agents.synthesizer_agent import SynthAgent


class RagPipeline:
    def __init__(self) -> None:
        self.schema_agent = SchemaAgent()
        self.sql_agent = SqlAgent()
        self.retriever = RetrieverAgent()
        self.synth = SynthAgent()

    def ask(self, question: str) -> Dict[str, Any]:
        """
        Process a natural language question through the multi-agent pipeline.
        
        Args:
            question: Natural language question
            
        Returns:
            Dictionary with answer and intermediate steps
        """
        try:
            # Step 1: Schema Agent - Identify relevant tables and columns
            schema_info = self.schema_agent.run(question)
            
            # Step 2: SQL Agent - Generate SQL query
            sql, params = self.sql_agent.build(question, schema_info)
            
            # Step 3: Retriever Agent - Execute SQL and get results
            rows, columns = self.retriever.run(sql, params)
            
            # Step 4: Synthesizer Agent - Generate natural language answer
            answer = self.synth.answer(question, rows, sql)
            
            error = None
            
        except Exception as e:
            rows, columns = [], []
            answer = f"Sorry, I encountered an error: {str(e)}"
            error = str(e)
            sql = ""
            params = {}
            schema_info = {}

        return {
            "question": question,
            "answer": answer,
            "intermediate": {
                "schema": schema_info,
                "sql": sql,
                "params": params,
                "columns": columns,
                "rows": rows,
                "error": error,
            },
        }
