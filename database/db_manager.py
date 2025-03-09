import sqlite3
import os
from typing import List, Dict, Any, Optional, Tuple, Union
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

class DatabaseManager:
    
    def __init__(self, db_file: str = None):
        load_dotenv()
        
        self.db_file = db_file or os.getenv('DB_FILE', 'qlchamsocsk.db')
        self._connection = None
        
    def __enter__(self):
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
    def connect(self):
        try:
            self._connection = sqlite3.connect(self.db_file)
            self._connection.row_factory = sqlite3.Row  

            self._connection.execute("PRAGMA foreign_keys = ON")
            
            return self._connection
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to connect to database: {e}")
            
    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            
    @property
    def connection(self):
        if not self._connection:
            self.connect()
        return self._connection
    
    def execute(self, query: str, params: tuple = None) -> sqlite3.Cursor:
        try:
            return self.connection.execute(query, params or ())
        except sqlite3.Error as e:
            self.connection.rollback()
            raise DatabaseError(f"Query execution failed: {e}")
            
    def executemany(self, query: str, params_list: List[tuple]) -> sqlite3.Cursor:
        try:
            return self.connection.executemany(query, params_list)
        except sqlite3.Error as e:
            self.connection.rollback()
            raise DatabaseError(f"Multiple query execution failed: {e}")
            
    def commit(self):
        try:
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            raise DatabaseError(f"Failed to commit transaction: {e}")
            
    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        cursor = self.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
        
    def fetch_all(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        cursor = self.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
        
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        has_timestamps = self._table_has_column(table, 'created_at') and self._table_has_column(table, 'updated_at')
        
        if has_timestamps:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data['created_at'] = now
            data['updated_at'] = now
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor = self.execute(query, tuple(data.values()))
        self.commit()
        return cursor.lastrowid
        
    def update(self, table: str, data: Dict[str, Any], condition: str, params: tuple) -> int:
        if self._table_has_column(table, 'updated_at'):
            data['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        set_clause = ', '.join([f"{column} = ?" for column in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        cursor = self.execute(query, tuple(data.values()) + params)
        self.commit()
        return cursor.rowcount
        
    def delete(self, table: str, condition: str, params: tuple) -> int:
        query = f"DELETE FROM {table} WHERE {condition}"
        cursor = self.execute(query, params)
        self.commit()
        return cursor.rowcount
    
    def _table_has_column(self, table: str, column: str) -> bool:
        try:
            cursor = self.execute(f"PRAGMA table_info({table})")
            columns = [row['name'] for row in cursor.fetchall()]
            return column in columns
        except sqlite3.Error:
            return False
    
    def backup(self, backup_file: str = None) -> str:
        if not backup_file:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            backup_file = f"backup_{timestamp}.db"
        
        try:
            backup_conn = sqlite3.connect(backup_file)
            with backup_conn:
                self.connection.backup(backup_conn)

            backup_conn.close()
            
            return backup_file
            
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to backup database: {e}")
    
    def restore(self, backup_file: str) -> bool:
        if not Path(backup_file).exists():
            raise DatabaseError(f"Backup file not found: {backup_file}")
        
        try:
            self.close()
            backup_conn = sqlite3.connect(backup_file)
            self.connect()
        
            with backup_conn:
                backup_conn.backup(self.connection)
        
            backup_conn.close()
            return True
            
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to restore database: {e}")
    
    def execute_script(self, script: str) -> bool:
        try:
            self.connection.executescript(script)
            self.commit()
            return True
        except sqlite3.Error as e:
            self.connection.rollback()
            raise DatabaseError(f"Failed to execute script: {e}")

class DatabaseError(Exception):
    pass