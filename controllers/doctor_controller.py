from typing import List, Dict, Any, Optional
from database.models import Doctor
from database.db_manager import DatabaseManager, DatabaseError
from utils.validators import validate_doctor_data

class DoctorController:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()
    
    def get_all_doctors(self) -> List[Dict[str, Any]]:
        try:
            with self.db_manager as db:
                return db.fetch_all("SELECT * FROM BacSi")
        except DatabaseError as e:
            print(f"Error retrieving doctors: {e}")
            return []
    
    def get_doctor(self, doctor_id: int) -> Optional[Dict[str, Any]]:
        try:
            doctor = Doctor.find(doctor_id, self.db_manager)
            return {k: v for k, v in doctor.__dict__.items() if not k.startswith('_') and k != 'db_manager'} if doctor else None
        except DatabaseError as e:
            print(f"Error retrieving doctor: {e}")
            return None
    
    def get_doctor_by_cmnd(self, cmnd: str) -> Optional[Dict[str, Any]]:
        try:
            doctor = Doctor.find_by_cmnd(cmnd)
            return {k: v for k, v in doctor.__dict__.items() if not k.startswith('_') and k != 'db_manager'} if doctor else None
        except DatabaseError as e:
            print(f"Error retrieving doctor by CMND: {e}")
            return None
    
    def add_doctor(self, doctor_data: Dict[str, Any]) -> bool:
        try:
            errors = validate_doctor_data(doctor_data)
            if errors:
                raise ValueError(f"Invalid doctor data: {errors}")
            
            doctor = Doctor(db_manager=self.db_manager, **doctor_data)
            return doctor.save()
            
        except (DatabaseError, ValueError) as e:
            print(f"Error adding doctor: {e}")
            return False
    
    def update_doctor(self, doctor_id: int, doctor_data: Dict[str, Any]) -> bool:
        try:
            doctor = Doctor.find(doctor_id, self.db_manager)
            if not doctor:
                return False
            
            errors = validate_doctor_data(doctor_data)
            if errors:
                raise ValueError(f"Invalid doctor data: {errors}")
            
            for key, value in doctor_data.items():
                setattr(doctor, key, value)
            
            return doctor.save()
            
        except (DatabaseError, ValueError) as e:
            print(f"Error updating doctor: {e}")
            return False
    
    def delete_doctor(self, doctor_id: int) -> bool:
        try:
            doctor = Doctor.find(doctor_id, self.db_manager)
            if not doctor:
                return False
            
            return doctor.delete()
            
        except DatabaseError as e:
            print(f"Error deleting doctor: {e}")
            return False
    
    def search_doctors(self, search_term: str) -> List[Dict[str, Any]]:
        try:
            doctors = Doctor.search(search_term)
            return [{k: v for k, v in doc.__dict__.items() if not k.startswith('_') and k != 'db_manager'} for doc in doctors]
        except DatabaseError as e:
            print(f"Error searching doctors: {e}")
            return []
    
    def get_doctors_by_specialty(self, specialty: str) -> List[Dict[str, Any]]:
        try:
            doctors = Doctor.find_by_specialty(specialty)
            return [{k: v for k, v in doc.__dict__.items() if not k.startswith('_') and k != 'db_manager'} for doc in doctors]
        except DatabaseError as e:
            print(f"Error retrieving doctors by specialty: {e}")
            return []
    
    def get_doctor_appointments(self, doctor_id: int) -> List[Dict[str, Any]]:
        try:
            doctor = Doctor.find(doctor_id, self.db_manager)
            if not doctor:
                return []
            
            return doctor.get_upcoming_appointments()
        except DatabaseError as e:
            print(f"Error retrieving doctor appointments: {e}")
            return []