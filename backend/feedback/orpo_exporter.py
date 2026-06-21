import sqlite3
import json
from config import DB_PATH
from loguru import logger
from pathlib import Path

def export_preference_pairs():
    """
    Exports preference pairs (ORPO format) based on feedback.
    High rating (>=4) vs Low rating (<=2) for the same query.
    """
    export_path = Path(DB_PATH).parent / "orpo_dataset.json"
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all queries that have both high and low ratings
    cursor.execute("""
        SELECT query, 
               MAX(CASE WHEN rating >= 4 THEN explanation END) as chosen,
               MAX(CASE WHEN rating <= 2 THEN explanation END) as rejected
        FROM feedback
        GROUP BY query
        HAVING chosen IS NOT NULL AND rejected IS NOT NULL
    """)
    
    rows = cursor.fetchall()
    dataset = []
    
    for row in rows:
        dataset.append({
            "prompt": row["query"],
            "chosen": row["chosen"],
            "rejected": row["rejected"]
        })
        
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
        
    logger.info(f"Exported {len(dataset)} preference pairs to {export_path}")
    conn.close()
    return dataset
