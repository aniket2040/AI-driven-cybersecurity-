"""
Database connection and utility functions for cybersecurity threat prediction system.
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, db_url=None):
        """
        Initialize database manager.
        
        Args:
            db_url: Database connection URL. If None, reads from environment.
        """
        if db_url is None:
            db_url = os.getenv(
                'DATABASE_URL',
                'postgresql://postgres:postgres@localhost:5432/cyber_threat_db'
            )
        
        self.engine = create_engine(
            db_url,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True
        )
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        
    @contextmanager
    def get_session(self):
        """Context manager for database sessions."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def create_tables(self, schema_file='database/schema.sql'):
        """
        Create database tables from SQL schema file.
        
        Args:
            schema_file: Path to SQL schema file
        """
        try:
            with open(schema_file, 'r') as f:
                schema_sql = f.read()
            
            with self.engine.connect() as conn:
                # Split by semicolon and execute each statement
                statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
                for statement in statements:
                    conn.execute(text(statement))
                conn.commit()
            
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    def execute_query(self, query, params=None):
        """
        Execute a SQL query and return results.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Query results
        """
        with self.get_session() as session:
            result = session.execute(text(query), params or {})
            return result.fetchall()
    
    def insert_data(self, table_name, data):
        """
        Insert data into a table.
        
        Args:
            table_name: Name of the table
            data: Dictionary or list of dictionaries containing data
        """
        if not isinstance(data, list):
            data = [data]
        
        with self.get_session() as session:
            for record in data:
                columns = ', '.join(record.keys())
                placeholders = ', '.join([f':{k}' for k in record.keys()])
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                session.execute(text(query), record)
    
    def close(self):
        """Close database connections."""
        self.engine.dispose()


# Global database manager instance
db_manager = DatabaseManager()


def get_db_session():
    """Get a database session for use in other modules."""
    return db_manager.get_session()
