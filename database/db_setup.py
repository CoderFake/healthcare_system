#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from dotenv import load_dotenv
import json
from datetime import datetime

from .db_manager import DatabaseManager
from utils.helpers import generate_password_hash

class DatabaseSetup:
    def __init__(self, db_manager=None):
        load_dotenv()
        
        self.db_manager = db_manager or DatabaseManager()
        self.migrations_dir = Path(__file__).parent / 'migrations'
        self.migrations_dir.mkdir(exist_ok=True)
        
    def setup(self):
        self.initialize_migrations_table()
        self.create_base_tables()  # Tạo bảng cơ sở trước
        self.run_migrations()      # Sau đó mới áp dụng migrations
        self.initialize_admin_account()
    
    def initialize_migrations_table(self):
        with self.db_manager as db:
            db.execute('''
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration_name TEXT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            db.commit()
    
    def get_applied_migrations(self):
        with self.db_manager as db:
            result = db.fetch_all('SELECT migration_name FROM migrations ORDER BY id')
            return [m['migration_name'] for m in result]
    
    def run_migrations(self):
        applied = self.get_applied_migrations()
        
        migration_files = sorted([f for f in os.listdir(self.migrations_dir) 
                                if f.endswith('.sql') and not f.startswith('.')])
        
        for migration_file in migration_files:
            if migration_file not in applied:
                print(f"Applying migration: {migration_file}")
                try:
                    self.apply_migration(migration_file)
                except Exception as e:
                    print(f"Error applying migration {migration_file}: {e}")
    
    def apply_migration(self, migration_file):
        migration_path = self.migrations_dir / migration_file
        
        with open(migration_path, 'r') as f:
            sql = f.read()
        
        with self.db_manager as db:
            try:
                db.execute(sql)
                
                db.execute('INSERT INTO migrations (migration_name) VALUES (?)', (migration_file,))
                db.commit()
            except Exception as e:
                db.connection.rollback()
                print(f"Error applying migration {migration_file}: {e}")
                raise
    
    def create_base_tables(self):
        with self.db_manager as db:
            db.execute('''
            CREATE TABLE IF NOT EXISTS TaiKhoan (
                username TEXT PRIMARY KEY,
                pass TEXT NOT NULL,
                Hovaten TEXT NOT NULL,
                Gioitinh TEXT NOT NULL,
                Quyen TEXT NOT NULL,
                SDT TEXT,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')

            db.execute('''
            CREATE TABLE IF NOT EXISTS BenhNhan (
                MaBN INTEGER PRIMARY KEY AUTOINCREMENT,
                Ho TEXT NOT NULL,
                Ten TEXT NOT NULL,
                CMND TEXT NOT NULL UNIQUE,
                Gioitinh TEXT NOT NULL,
                Ngaysinh TEXT NOT NULL,
                SDT TEXT,
                Quequan TEXT,
                Ngaykham TEXT,
                DiaChi TEXT,
                Email TEXT,
                GhiChu TEXT,
                NhomMau TEXT,
                ChieuCao REAL,
                CanNang REAL,
                TienSuBenhAn TEXT,
                DiUng TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')

            db.execute('''
            CREATE TABLE IF NOT EXISTS BacSi (
                MaBS INTEGER PRIMARY KEY AUTOINCREMENT,
                Ho TEXT NOT NULL,
                Ten TEXT NOT NULL,
                CMND TEXT NOT NULL UNIQUE,
                Gioitinh TEXT NOT NULL,
                Ngaysinh TEXT NOT NULL,
                SDT TEXT,
                ChuyenKhoa TEXT NOT NULL,
                Email TEXT,
                DiaChi TEXT,
                BangCap TEXT,
                GhiChu TEXT,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES TaiKhoan(username)
            )
            ''')

            db.execute('''
            CREATE TABLE IF NOT EXISTS LichKham (
                MaLichKham INTEGER PRIMARY KEY AUTOINCREMENT,
                MaBN INTEGER,
                MaBS INTEGER,
                NgayKham TEXT,
                GioKham TEXT,
                LydoKham TEXT,
                TrangThai TEXT DEFAULT 'Chờ khám',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (MaBN) REFERENCES BenhNhan(MaBN),
                FOREIGN KEY (MaBS) REFERENCES BacSi(MaBS)
            )
            ''')
            
            db.execute('''
            CREATE TABLE IF NOT EXISTS HoSoBenhAn (
                MaHoSo INTEGER PRIMARY KEY AUTOINCREMENT,
                MaBN INTEGER,
                MaBS INTEGER,
                NgayKham TEXT,
                ChanDoan TEXT,
                TrieuChung TEXT,
                HuongDieuTri TEXT,
                DonThuoc TEXT,
                KetLuan TEXT,
                GhiChu TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (MaBN) REFERENCES BenhNhan(MaBN),
                FOREIGN KEY (MaBS) REFERENCES BacSi(MaBS)
            )
            ''')
            
            db.execute('''
            CREATE TABLE IF NOT EXISTS AppSettings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT,
                setting_type TEXT,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            db.commit()
    
    def initialize_admin_account(self):
        with self.db_manager as db:
            admin = db.fetch_one("SELECT * FROM TaiKhoan WHERE username = ?", ("admin",))
            
            if not admin:
                admin_username = os.getenv('ADMIN_USERNAME', 'admin')
                admin_password = os.getenv('ADMIN_PASSWORD', '123456')
                admin_name = os.getenv('ADMIN_NAME', 'Quản trị viên')
                admin_gender = os.getenv('ADMIN_GENDER', 'Nam')
                admin_phone = os.getenv('ADMIN_PHONE', '0123456789')
                admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
                
                hashed_password = generate_password_hash(admin_password)
                
                db.execute('''
                INSERT INTO TaiKhoan (username, pass, Hovaten, Gioitinh, Quyen, SDT, email)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (admin_username, hashed_password, admin_name, admin_gender, "admin", admin_phone, admin_email))
                db.commit()
                print("Admin account created successfully!")
    
    def create_migration(self, name):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{name}.sql"
        
        migration_path = self.migrations_dir / filename
        
        with open(migration_path, 'w') as f:
            f.write(f"-- Migration: {name}\n")
            f.write(f"-- Created at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("-- Write your SQL migration here\n\n")
        
        print(f"Created migration: {filename}")
        return migration_path
    
    def export_schema(self, output_file=None):
        if output_file is None:
            output_file = Path('schema_export.json')
        
        schema = {}
        
        with self.db_manager as db:
            tables = db.fetch_all("SELECT name FROM sqlite_master WHERE type='table'")
            
            for table in tables:
                table_name = table['name']
                
                if table_name.startswith('sqlite_'):
                    continue
                
                create_table = db.fetch_one(f"SELECT sql FROM sqlite_master WHERE name=?", (table_name,))
                
                table_info = db.fetch_all(f"PRAGMA table_info({table_name})")
                
                schema[table_name] = {
                    'creation_sql': create_table['sql'],
                    'columns': [{'name': col['name'], 'type': col['type'], 'notnull': col['notnull']} for col in table_info]
                }
        
        with open(output_file, 'w') as f:
            json.dump(schema, f, indent=4)
        
        print(f"Schema exported to {output_file}")