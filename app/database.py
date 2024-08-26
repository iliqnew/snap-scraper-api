import sqlite3


def setup_db(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS screenshots (id INTEGER PRIMARY KEY, scrape_id TEXT, path TEXT, url TEXT)"
    )
    conn.commit()
    return conn, cursor


def insert_screenshot(conn, cursor, screenshot):
    cursor.execute(
        "INSERT INTO screenshots (scrape_id, path, url) VALUES (?, ?, ?)",
        (screenshot.scrape_id, screenshot.screenshot_path, screenshot.url),
    )
    conn.commit()


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # for sqlite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
