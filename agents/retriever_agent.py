# agents/retriever_agent.py

from typing import Any, Dict, List, Tuple

from psycopg2.extras import RealDictCursor

from backend.db import get_conn


class RetrieverAgent:
    """Executes SQL and returns rows as list[dict]."""

    def run(self, sql: str, params: Dict[str, Any] | None = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        params = params or {}
        with get_conn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()
                cols = [desc.name for desc in cur.description]
        return [dict(r) for r in rows], cols



