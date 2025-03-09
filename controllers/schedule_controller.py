from typing import List, Dict, Any, Optional
from database.models import Appointment, MedicalRecord
from database.db_manager import DatabaseManager, DatabaseError
from utils.validators import validate_appointment_data

class ScheduleController:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()
    
    def get_all_appointments(self) -> List[Dict[str, Any]]:
        try:
            return Appointment.get_appointments_with_details(self.db_manager)
        except DatabaseError as e:
            print(f"Error retrieving appointments: {e}")
            return []
    
    def get_appointment(self, appointment_id: int) -> Optional[Dict[str, Any]]:
        try:
            appointment = Appointment.find(appointment_id, self.db_manager)
            if not appointment:
                return None
            
            with self.db_manager as db:
                query = """
                SELECT LK.*, BS.Ho || ' ' || BS.Ten AS TenBacSi, 
                            BN.Ho || ' ' || BN.Ten AS TenBenhNhan
                FROM LichKham LK
                LEFT JOIN BacSi BS ON LK.MaBS = BS.MaBS
                LEFT JOIN BenhNhan BN ON LK.MaBN = BN.MaBN
                WHERE LK.MaLichKham = ?
                """
                return db.fetch_one(query, (appointment_id,))
        except DatabaseError as e:
            print(f"Error retrieving appointment: {e}")
            return None
    
    def add_appointment(self, appointment_data: Dict[str, Any]) -> bool:
        try:
            errors = validate_appointment_data(appointment_data)
            if errors:
                raise ValueError(f"Invalid appointment data: {errors}")
            
            if not self._check_time_available(
                appointment_data.get('MaBS'), 
                appointment_data.get('NgayKham'), 
                appointment_data.get('GioKham')
            ):
                raise ValueError("The selected time is not available for this doctor")

            if 'TrangThai' not in appointment_data:
                appointment_data['TrangThai'] = 'Chờ khám'
            
            appointment = Appointment(db_manager=self.db_manager, **appointment_data)
            return appointment.save()
            
        except (DatabaseError, ValueError) as e:
            print(f"Error adding appointment: {e}")
            return False
    
    def update_appointment(self, appointment_id: int, appointment_data: Dict[str, Any]) -> bool:
        try:
            appointment = Appointment.find(appointment_id, self.db_manager)
            if not appointment:
                return False
            
            errors = validate_appointment_data(appointment_data)
            if errors:
                raise ValueError(f"Invalid appointment data: {errors}")
            if ('NgayKham' in appointment_data or 'GioKham' in appointment_data) and \
               (appointment_data.get('NgayKham') != getattr(appointment, 'NgayKham', None) or 
                appointment_data.get('GioKham') != getattr(appointment, 'GioKham', None)):
                
                doctor_id = appointment_data.get('MaBS', getattr(appointment, 'MaBS', None))
                date = appointment_data.get('NgayKham', getattr(appointment, 'NgayKham', None))
                time = appointment_data.get('GioKham', getattr(appointment, 'GioKham', None))
                
                if not self._check_time_available(doctor_id, date, time, exclude_id=appointment_id):
                    raise ValueError("The selected time is not available for this doctor")
            
            for key, value in appointment_data.items():
                setattr(appointment, key, value)
            
            return appointment.save()
            
        except (DatabaseError, ValueError) as e:
            print(f"Error updating appointment: {e}")
            return False
    
    def delete_appointment(self, appointment_id: int) -> bool:
        try:
            appointment = Appointment.find(appointment_id, self.db_manager)
            if not appointment:
                return False
            
            return appointment.delete()
            
        except DatabaseError as e:
            print(f"Error deleting appointment: {e}")
            return False
    
    def get_appointments_by_date(self, date: str) -> List[Dict[str, Any]]:
        try:
            return Appointment.get_appointments_by_date(date, self.db_manager)
        except DatabaseError as e:
            print(f"Error retrieving appointments by date: {e}")
            return []
    
    def get_doctor_appointments(self, doctor_id: int) -> List[Dict[str, Any]]:
        try:
            return Appointment.get_appointments_by_doctor(doctor_id, self.db_manager)
        except DatabaseError as e:
            print(f"Error retrieving doctor appointments: {e}")
            return []
    
    def get_patient_appointments(self, patient_id: int) -> List[Dict[str, Any]]:
        try:
            return Appointment.get_appointments_by_patient(patient_id, self.db_manager)
        except DatabaseError as e:
            print(f"Error retrieving patient appointments: {e}")
            return []
    
    def _check_time_available(self, doctor_id: int, date: str, time: str, exclude_id: int = None) -> bool:
        try:
            if exclude_id:
                with self.db_manager as db:
                    query = """
                    SELECT COUNT(*) as count
                    FROM LichKham
                    WHERE MaBS = ? AND NgayKham = ? AND GioKham = ? AND MaLichKham != ?
                    """
                    result = db.fetch_one(query, (doctor_id, date, time, exclude_id))
                    return result['count'] == 0
            else:
                return Appointment.check_time_available(doctor_id, date, time, self.db_manager)
        except DatabaseError:
            return False
    
    def create_medical_record(self, appointment_id: int, diagnosis: str) -> bool:
        try:
            record = MedicalRecord.create_from_appointment(appointment_id, diagnosis, self.db_manager)
            return record is not None
        except DatabaseError as e:
            print(f"Error creating medical record: {e}")
            return False