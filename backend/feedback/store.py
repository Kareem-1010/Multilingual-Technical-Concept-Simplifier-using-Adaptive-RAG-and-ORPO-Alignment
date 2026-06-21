import aiosqlite
from config import DB_PATH
from loguru import logger

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_id INTEGER,
                query TEXT NOT NULL,
                domain TEXT,
                language TEXT,
                explanation TEXT,
                rating INTEGER CHECK(rating IN (1, 2, 3, 4, 5)),
                comment TEXT,
                faithfulness_score REAL,
                readability_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        await db.commit()
    logger.info("Database initialized with users and feedback tables.")

async def get_user_by_username(username: str):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE username = ?", (username,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def create_user(username: str, hashed_password: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (username, hashed_password))
        await db.commit()

async def insert_feedback(data: dict):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO feedback (
                session_id, user_id, query, domain, language, explanation, 
                rating, comment, faithfulness_score, readability_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('session_id'),
            data.get('user_id'),
            data.get('query'),
            data.get('domain'),
            data.get('language'),
            data.get('explanation'),
            data.get('rating'),
            data.get('comment'),
            data.get('faithfulness_score'),
            data.get('readability_score')
        ))
        await db.commit()

async def get_history(user_id: int, limit: int = 50):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM feedback WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?", (user_id, limit)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def get_stats():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT AVG(rating) as avg_rating, COUNT(*) as total FROM feedback") as cursor:
            row = await cursor.fetchone()
            return {"avg_rating": row[0], "total_feedback": row[1]}
