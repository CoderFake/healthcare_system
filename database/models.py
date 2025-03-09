from typing import Dict, List, Any, Optional
from datetime import datetime
from .db_manager import DatabaseManager
from utils.helpers import generate_password_hash, verify_password

class Model:
    table_name = None
    primary_key = None
    
    def __init__(self, db_manager=None, **kwargs):
        self.db_manager = db_manager or DatabaseManager()
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def find(cls, id_value, db_manager=None) -> Optional['Model']:
        db = db_manager or DatabaseManager()
        with db:
            data = db.fetch_one(
                f"SELECT * FROM {cls.table_name} WHERE {cls.primary_key} = ?", 
                (id_value,)
            )
            return cls(db_manager=db, **data) if data else None
    
    @classmethod
    def find_all(cls, db_manager=None) -> List['Model']:
        db = db_manager or DatabaseManager()
        with db:
            records = db.fetch_all(f"SELECT * FROM {cls.table_name}")
            return [cls(db_manager=db, **record) for record in records]
    
    @classmethod
    def where(cls, condition: str, params: tuple, db_manager=None) -> List['Model']:
        db = db_manager or DatabaseManager()
        with db:
            query = f"SELECT * FROM {cls.table_name} WHERE {condition}"
            records = db.fetch_all(query, params)
            return [cls(db_manager=db, **record) for record in records]
    
    def save(self) -> bool:
        with self.db_manager:
            data = {k: v for k, v in self.__dict__.items() 
                    if k not in ('db_manager', self.primary_key) and not k.startswith('_')}
            
            if hasattr(self, self.primary_key) and getattr(self, self.primary_key):
                pk_value = getattr(self, self.primary_key)
                self.db_manager.update(
                    self.table_name, 
                    data, 
                    f"{self.primary_key} = ?", 
                    (pk_value,)
                )
                return True
            else:
                new_id = self.db_manager.insert(self.table_name, data)
                setattr(self, self.primary_key, new_id)
                return True
        return False
    
    def delete(self) -> bool:
        with self.db_manager:
            if hasattr(self, self.primary_key) and getattr(self, self.primary_key):
                pk_value = getattr(self, self.primary_key)
                result = self.db_manager.delete(
                    self.table_name, 
                    f"{self.primary_key} = ?", 
                    (pk_value,)
                )
                return result > 0
        return False
    
    def refresh(self) -> bool:
        if hasattr(self, self.primary_key) and getattr(self, self.primary_key):
            pk_value = getattr(self, self.primary_key)
            with self.db_manager:
                data = self.db_manager.fetch_one(
                    f"SELECT * FROM {self.table_name} WHERE {self.primary_key} = ?",
                    (pk_value,)
                )
                if data:
                    for key, value in data.items():
                        setattr(self, key, value)
                    return True
        return False


class User(Model):
    table_name = "TaiKhoan"
    primary_key = "username"
    
    @classmethod
    def find_by_username(cls, username: str) -> Optional['User']:
        db = DatabaseManager()
        with db:
            data = db.fetch_one(
                f"SELECT * FROM {cls.table_name} WHERE username = ?", 
                (username,)
            )
            return cls(db_manager=db, **data) if data else None
    
    @classmethod
    def authenticate(cls, username: str, password: str) -> Optional['User']:
        user = cls.find_by_username(username)
        
        if user and verify_password(password, user.pass_):
            return user
        
        return None
    
    def update_password(self, new_password: str) -> bool:
        if not hasattr(self, 'username'):
            return False
        
        hashed_password = generate_password_hash(new_password)
        
        with self.db_manager:
            result = self.db_manager.update(
                self.table_name,
                {'pass': hashed_password},
                f"{self.primary_key} = ?",
                (self.username,)
            )
            
            if result > 0:
                self.pass_ = hashed_password
                return True
            
        return False
    
    @property
    def pass_(self):
        return getattr(self, 'pass', None)
    
    @pass_.setter
    def pass_(self, value):
        setattr(self, 'pass', value)


class Doctor(Model):
    table_name = "BacSi"
    primary_key = "MaBS"
    
    @classmethod
    def find_by_cmnd(cls, cmnd: str) -> Optional['Doctor']:
        db = DatabaseManager()
        with db:
            data = db.fetch_one(
                f"SELECT * FROM {cls.table_name} WHERE CMND = ?", 
                (cmnd,)
            )
            return cls(db_manager=db, **data) if data else None
    
    @classmethod
    def find_by_specialty(cls, specialty: str) -> List['Doctor']:
        return cls.where("ChuyenKhoa = ?", (specialty,))
    
    @classmethod
    def search(cls, term: str) -> List['Doctor']:
        search_term = f"%{term}%"
        db = DatabaseManager()
        with db:
            query = f"""
            SELECT * FROM {cls.table_name} 
            WHERE Ho LIKE ? OR Ten LIKE ? OR CMND LIKE ? OR ChuyenKhoa LIKE ?
            """
            records = db.fetch_all(query, (search_term, search_term, search_term, search_term))
            return [cls(db_manager=db, **record) for record in records]
    
    def get_full_name(self) -> str:
        ho = getattr(self, 'Ho', '')
        ten = getattr(self, 'Ten', '')
        return f"{ho} {ten}".strip()
    
    def get_upcoming_appointments(self, limit=10) -> List[Dict[str, Any]]:
        if not hasattr(self, 'MaBS'):
            return []
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        with self.db_manager:
            query = """
            SELECT LK.*, BN.Ho || ' ' || BN.Ten AS TenBenhNhan 
            FROM LichKham LK
            JOIN BenhNhan BN ON LK.MaBN = BN.MaBN
            WHERE LK.MaBS = ? AND LK.NgayKham >= ?
            ORDER BY LK.NgayKham, LK.GioKham
            LIMIT ?
            """
            return self.db_manager.fetch_all(query, (self.MaBS, today, limit))


class Patient(Model):
    table_name = "BenhNhan"
    primary_key = "MaBN"
    
    @classmethod
    def find_by_cmnd(cls, cmnd: str) -> Optional['Patient']:
        db = DatabaseManager()
        with db:
            data = db.fetch_one(
                f"SELECT * FROM {cls.table_name} WHERE CMND = ?", 
                (cmnd,)
            )
            return cls(db_manager=db, **data) if data else None
    
    @classmethod
    def search(cls, term: str) -> List['Patient']:
        search_term = f"%{term}%"
        db = DatabaseManager()
        with db:
            query = f"""
            SELECT * FROM {cls.table_name} 
            WHERE Ho LIKE ? OR Ten LIKE ? OR CMND LIKE ? OR Quequan LIKE ?
            """
            records = db.fetch_all(query, (search_term, search_term, search_term, search_term))
            return [cls(db_manager=db, **record) for record in records]
    
    def get_full_name(self) -> str:
        ho = getattr(self, 'Ho', '')
        ten = getattr(self, 'Ten', '')
        return f"{ho} {ten}".strip()
    
    def get_appointment_history(self) -> List[Dict[str, Any]]:
        if not hasattr(self, 'MaBN'):
            return []
        
        with self.db_manager:
            query = """
            SELECT LK.*, BS.Ho || ' ' || BS.Ten AS TenBacSi, BS.ChuyenKhoa 
            FROM LichKham LK
            JOIN BacSi BS ON LK.MaBS = BS.MaBS
            WHERE LK.MaBN = ?
            ORDER BY LK.NgayKham DESC, LK.GioKham DESC
            """
            return self.db_manager.fetch_all(query, (self.MaBN,))
    
    def get_medical_records(self) -> List[Dict[str, Any]]:
        if not hasattr(self, 'MaBN'):
            return []
        
        with self.db_manager:
            query = """
            SELECT HS.*, BS.Ho || ' ' || BS.Ten AS TenBacSi, BS.ChuyenKhoa 
            FROM HoSoBenhAn HS
            JOIN BacSi BS ON HS.MaBS = BS.MaBS
            WHERE HS.MaBN = ?
            ORDER BY HS.NgayKham DESC
            """
            return self.db_manager.fetch_all(query, (self.MaBN,))
    
    def calculate_age(self) -> Optional[int]:
        if not hasattr(self, 'Ngaysinh'):
            return None
            
        try:
            birth_date = datetime.strptime(self.Ngaysinh, "%Y-%m-%d")
            today = datetime.now()
            
            age = today.year - birth_date.year
            
            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1
                
            return age
        except ValueError:
            return None


class Appointment(Model):
    table_name = "LichKham"
    primary_key = "MaLichKham"
    
    @classmethod
    def get_appointments_with_details(cls, db_manager=None) -> List[Dict[str, Any]]:
        db = db_manager or DatabaseManager()
        with db:
            query = """
            SELECT LK.*, BS.Ho || ' ' || BS.Ten AS TenBacSi, 
                          BN.Ho || ' ' || BN.Ten AS TenBenhNhan
            FROM LichKham LK
            LEFT JOIN BacSi BS ON LK.MaBS = BS.MaBS
            LEFT JOIN BenhNhan BN ON LK.MaBN = BN.MaBN
            """
            return db.fetch_all(query)
    
    @classmethod
    def get_appointments_by_date(cls, date: str, db_manager=None) -> List[Dict[str, Any]]:
        db = db_manager or DatabaseManager()
        with db:
            query = """
            SELECT LK.*, BS.Ho || ' ' || BS.Ten AS TenBacSi, BS.ChuyenKhoa,
                          BN.Ho || ' ' || BN.Ten AS TenBenhNhan
            FROM LichKham LK
            LEFT JOIN BacSi BS ON LK.MaBS = BS.MaBS
            LEFT JOIN BenhNhan BN ON LK.MaBN = BN.MaBN
            WHERE LK.NgayKham = ?
            ORDER BY LK.GioKham
            """
            return db.fetch_all(query, (date,))
    
    @classmethod
    def get_appointments_by_doctor(cls, doctor_id: int, db_manager=None) -> List[Dict[str, Any]]:
        db = db_manager or DatabaseManager()
        with db:
            query = """
            SELECT LK.*, BN.Ho || ' ' || BN.Ten AS TenBenhNhan
            FROM LichKham LK
            LEFT JOIN BenhNhan BN ON LK.MaBN = BN.MaBN
            WHERE LK.MaBS = ?
            ORDER BY LK.NgayKham, LK.GioKham
            """
            return db.fetch_all(query, (doctor_id,))
    
    @classmethod
    def get_appointments_by_patient(cls, patient_id: int, db_manager=None) -> List[Dict[str, Any]]:
        db = db_manager or DatabaseManager()
        with db:
            query = """
            SELECT LK.*, BS.Ho || ' ' || BS.Ten AS TenBacSi, BS.ChuyenKhoa
            FROM LichKham LK
            LEFT JOIN BacSi BS ON LK.MaBS = BS.MaBS
            WHERE LK.MaBN = ?
            ORDER BY LK.NgayKham, LK.GioKham
            """
            return db.fetch_all(query, (patient_id,))
    
    @classmethod
    def check_time_available(cls, doctor_id: int, date: str, time: str, db_manager=None) -> bool:
        db = db_manager or DatabaseManager()
        with db:
            query = """
            SELECT COUNT(*) as count
            FROM LichKham
            WHERE MaBS = ? AND NgayKham = ? AND GioKham = ?
            """
            result = db.fetch_one(query, (doctor_id, date, time))
            return result['count'] == 0


class MedicalRecord(Model):
    table_name = "HoSoBenhAn"
    primary_key = "MaHoSo"
    
    @classmethod
    def get_records_by_patient(cls, patient_id: int, db_manager=None) -> List[Dict[str, Any]]:
        db = db_manager or DatabaseManager()
        with db:
            query = """
            SELECT HS.*, BS.Ho || ' ' || BS.Ten AS TenBacSi, BS.ChuyenKhoa
            FROM HoSoBenhAn HS
            LEFT JOIN BacSi BS ON HS.MaBS = BS.MaBS
            WHERE HS.MaBN = ?
            ORDER BY HS.NgayKham DESC
            """
            return db.fetch_all(query, (patient_id,))
    
    @classmethod
    def get_records_by_doctor(cls, doctor_id: int, db_manager=None) -> List[Dict[str, Any]]:
        db = db_manager or DatabaseManager()
        with db:
            query = """
            SELECT HS.*, BN.Ho || ' ' || BN.Ten AS TenBenhNhan
            FROM HoSoBenhAn HS
            LEFT JOIN BenhNhan BN ON HS.MaBN = BN.MaBN
            WHERE HS.MaBS = ?
            ORDER BY HS.NgayKham DESC
            """
            return db.fetch_all(query, (doctor_id,))
    
    @classmethod
    def create_from_appointment(cls, appointment_id: int, diagnosis: str, db_manager=None) -> Optional['MedicalRecord']:
        db = db_manager or DatabaseManager()
        with db:
            appointment = db.fetch_one(
                "SELECT * FROM LichKham WHERE MaLichKham = ?", 
                (appointment_id,)
            )
            
            if not appointment:
                return None
            
            record_data = {
                'MaBN': appointment['MaBN'],
                'MaBS': appointment['MaBS'],
                'NgayKham': appointment['NgayKham'],
                'ChanDoan': diagnosis,
                'TrieuChung': '',
                'HuongDieuTri': '',
                'DonThuoc': '',
                'KetLuan': '',
                'GhiChu': f"Created from appointment #{appointment_id}"
            }
            
            record_id = db.insert(cls.table_name, record_data)
            
            db.update(
                'LichKham',
                {'TrangThai': 'Đã khám'},
                'MaLichKham = ?',
                (appointment_id,)
            )
            
            return cls.find(record_id, db)


class AppSetting(Model):
    table_name = "AppSettings"
    primary_key = "setting_key"
    
    @classmethod
    def get(cls, key: str, default=None, db_manager=None) -> Any:
        setting = cls.find(key, db_manager)
        
        if not setting:
            return default
            
        if not hasattr(setting, 'setting_value'):
            return default
            
        if hasattr(setting, 'setting_type'):
            value_type = getattr(setting, 'setting_type', 'string')
            
            if value_type == 'int':
                return int(setting.setting_value)
            elif value_type == 'float':
                return float(setting.setting_value)
            elif value_type == 'bool':
                return setting.setting_value.lower() in ('true', 'yes', '1', 'on')
                
        return setting.setting_value
    
    @classmethod
    def set(cls, key: str, value: Any, value_type: str = None, description: str = None, db_manager=None) -> bool:
        db = db_manager or DatabaseManager()
        
        value_str = str(value)
        
        if value_type is None:
            if isinstance(value, int):
                value_type = 'int'
            elif isinstance(value, float):
                value_type = 'float'
            elif isinstance(value, bool):
                value_type = 'bool'
            else:
                value_type = 'string'
        
        setting = cls.find(key, db)
        
        if setting:
            update_data = {'setting_value': value_str, 'setting_type': value_type}
            if description:
                update_data['description'] = description
                
            with db:
                db.update(
                    cls.table_name,
                    update_data,
                    f"{cls.primary_key} = ?",
                    (key,)
                )
        else:
            setting_data = {
                'setting_key': key,
                'setting_value': value_str,
                'setting_type': value_type
            }
            if description:
                setting_data['description'] = description
                
            with db:
                db.insert(cls.table_name, setting_data)
                
        return True