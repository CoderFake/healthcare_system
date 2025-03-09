from typing import List, Dict, Any, Optional
from database.models import Patient
from database.db_manager import DatabaseManager, DatabaseError
from utils.validators import validate_patient_data

class PatientController:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()
    
    def get_all_patients(self) -> List[Dict[str, Any]]:
        try:
            with self.db_manager as db:
                return db.fetch_all("SELECT * FROM BenhNhan")
        except DatabaseError as e:
            print(f"Error retrieving patients: {e}")
            return []
    
    def get_patient(self, patient_id: int) -> Optional[Dict[str, Any]]:
        try:
            patient = Patient.find(patient_id, self.db_manager)
            return {k: v for k, v in patient.__dict__.items() if not k.startswith('_') and k != 'db_manager'} if patient else None
        except DatabaseError as e:
            print(f"Error retrieving patient: {e}")
            return None
    
    def get_patient_by_cmnd(self, cmnd: str) -> Optional[Dict[str, Any]]:
        try:
            patient = Patient.find_by_cmnd(cmnd)
            return {k: v for k, v in patient.__dict__.items() if not k.startswith('_') and k != 'db_manager'} if patient else None
        except DatabaseError as e:
            print(f"Error retrieving patient by CMND: {e}")
            return None
    
    def add_patient(self, patient_data: Dict[str, Any]) -> bool:
        try:
            errors = validate_patient_data(patient_data)
            if errors:
                raise ValueError(f"Invalid patient data: {errors}")
            
            patient = Patient(db_manager=self.db_manager, **patient_data)
            return patient.save()
            
        except (DatabaseError, ValueError) as e:
            print(f"Error adding patient: {e}")
            return False
    
    def update_patient(self, patient_id: int, patient_data: Dict[str, Any]) -> bool:
        try:
            patient = Patient.find(patient_id, self.db_manager)
            if not patient:
                return False
            
            errors = validate_patient_data(patient_data)
            if errors:
                raise ValueError(f"Invalid patient data: {errors}")
            
            for key, value in patient_data.items():
                setattr(patient, key, value)
            
            return patient.save()
            
        except (DatabaseError, ValueError) as e:
            print(f"Error updating patient: {e}")
            return False
    
    def delete_patient(self, patient_id: int) -> bool:
        try:
            patient = Patient.find(patient_id, self.db_manager)
            if not patient:
                return False
            
            return patient.delete()
            
        except DatabaseError as e:
            print(f"Error deleting patient: {e}")
            return False
    
    def search_patients(self, search_term: str) -> List[Dict[str, Any]]:
        try:
            patients = Patient.search(search_term)
            return [{k: v for k, v in pat.__dict__.items() if not k.startswith('_') and k != 'db_manager'} for pat in patients]
        except DatabaseError as e:
            print(f"Error searching patients: {e}")
            return []
    
    def get_patient_appointments(self, patient_id: int) -> List[Dict[str, Any]]:
        try:
            patient = Patient.find(patient_id, self.db_manager)
            if not patient:
                return []
            
            return patient.get_appointment_history()
        except DatabaseError as e:
            print(f"Error retrieving patient appointments: {e}")
            return []
    
    def get_patient_medical_records(self, patient_id: int) -> List[Dict[str, Any]]:
        try:
            patient = Patient.find(patient_id, self.db_manager)
            if not patient:
                return []
            
            return patient.get_medical_records()
        except DatabaseError as e:
            print(f"Error retrieving patient medical records: {e}")
            return []