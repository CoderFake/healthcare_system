import os
from pathlib import Path

APP_NAME = "Hệ Thống Quản Lý Dịch Vụ Chăm Sóc Sức Khỏe"
APP_VERSION = "1.0.0"
APP_AUTHOR = "HoangDieuIT"

ROOT_DIR = Path(__file__).parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
DATABASE_FILE = "qlchamsocsk.db"

THEME = "classic"
STYLES = {
    "background": "#f0f0f0",
    "accent": "#4a7abc",
    "accent_light": "#6a9ade",
    "accent_dark": "#2a5a9c",
    "error": "#c0392b",
    "success": "#27ae60",
    "warning": "#f39c12",
    "info": "#3498db",
    "text": "#333333",
    "text_light": "#666666",
    "border": "#d0d0d0"
}

FONTS = {
    "default": ("Arial", 10),
    "title": ("Arial", 16, "bold"),
    "heading": ("Arial", 14, "bold"),
    "subheading": ("Arial", 12, "bold"),
    "small": ("Arial", 9),
    "button": ("Arial", 10),
    "monospace": ("Courier New", 10)
}

TIME_SLOTS = [f"{h:02d}:{m:02d}" for h in range(8, 18) for m in (0, 30)]

EXPORT_FORMATS = ["CSV", "Excel", "PDF"]

MAX_APPOINTMENTS_PER_DAY = 20
MAX_APPOINTMENTS_PER_DOCTOR = 10

USER_ROLES = ["admin", "doctor", "staff"]

TIME_FORMAT = "%H:%M"
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"

DISPLAY_DATE_FORMAT = "%d/%m/%Y"
DISPLAY_TIME_FORMAT = "%H:%M"
DISPLAY_DATETIME_FORMAT = f"{DISPLAY_DATE_FORMAT} {DISPLAY_TIME_FORMAT}"

DEFAULT_SPECIALTIES = [
    "Nội khoa",
    "Ngoại khoa", 
    "Sản phụ khoa", 
    "Nhi khoa", 
    "Răng hàm mặt", 
    "Mắt", 
    "Tai mũi họng", 
    "Da liễu", 
    "Thần kinh", 
    "Tim mạch", 
    "Tiêu hóa",
    "Hô hấp", 
    "Tiết niệu", 
    "Chấn thương chỉnh hình", 
    "Ung thư", 
    "Dinh dưỡng", 
    "Tâm thần"
]

LOGGING = {
    "enabled": True,
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "app.log",
    "max_size": 10 * 1024 * 1024,  
    "backup_count": 5
}

EMAIL = {
    "enabled": False,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "",
    "password": "",
    "use_tls": True,
}

REMINDERS = {
    "enabled": False,
    "days_before": 1,
    "send_time": "08:00"
}

def get_asset_path(filename):
    return ASSETS_DIR / filename

def get_icon_path(icon_name):
    return ASSETS_DIR / "icons" / icon_name

def get_image_path(image_name):
    return ASSETS_DIR / "images" / image_name