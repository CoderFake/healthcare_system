import os
import hashlib
import re
from datetime import datetime, timedelta
import calendar
import uuid
import base64

def generate_password_hash(password):
    salt = uuid.uuid4().hex
    hashed = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(plain_password, hashed_password):
    import hashlib
    
    if not hashed_password or "$" not in hashed_password:
        return False
        
    salt, hash_value = hashed_password.split("$", 1)
    calculated_hash = hashlib.sha256(salt.encode() + plain_password.encode()).hexdigest()
    return calculated_hash == hash_value


def normalize_vietnamese_name(name):
    name = name.strip()
    
    def normalize_char(c):
        mapping = {
            'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
            'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
            'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
            'đ': 'd',
            'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
            'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
            'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
            'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
            'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
            'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
            'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
            'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
            'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y'
        }
        if c.lower() in mapping:
            return mapping[c.lower()]
        return c.lower()
    
    normalized = ''.join(normalize_char(c) for c in name)
    return normalized

def format_date(date_str, input_format="%Y-%m-%d", output_format="%d/%m/%Y"):
    try:
        date_obj = datetime.strptime(date_str, input_format)
        return date_obj.strftime(output_format)
    except ValueError:
        return date_str

def parse_date(date_str, formats=["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]):
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date '{date_str}' does not match any of the formats: {formats}")

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

def get_week_dates(date_str=None):
    if date_str:
        current_date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        current_date = datetime.now()
    
    start_of_week = current_date - timedelta(days=current_date.weekday())
    
    dates = []
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        dates.append(day.strftime("%Y-%m-%d"))
    
    return dates

def get_month_dates(year=None, month=None):
    if year is None or month is None:
        now = datetime.now()
        year = now.year
        month = now.month
    
    _, num_days = calendar.monthrange(year, month)
    
    dates = []
    for day in range(1, num_days + 1):
        date = datetime(year, month, day)
        dates.append(date.strftime("%Y-%m-%d"))
    
    return dates

def format_phone_number(phone):
    if not phone:
        return ""
    
    phone = re.sub(r'\D', '', phone) 
    
    if len(phone) == 10 and phone.startswith('0'):
        return f"{phone[0:4]}.{phone[4:7]}.{phone[7:10]}"
    elif len(phone) == 10 and not phone.startswith('0'):
        return f"{phone[0:4]}.{phone[4:7]}.{phone[7:10]}"
    elif len(phone) == 11 and phone.startswith('0'):
        return f"{phone[0:2]}.{phone[2:6]}.{phone[6:11]}"
    elif len(phone) > 11 and (phone.startswith('84') or phone.startswith('+84')):
        if phone.startswith('+'):
            cleaned = phone[3:] 
        else:
            cleaned = phone[2:] 
            
        if len(cleaned) == 9:
            return f"0{cleaned[0:3]}.{cleaned[3:6]}.{cleaned[6:9]}"
        elif len(cleaned) == 10:
            return f"0{cleaned[0:4]}.{cleaned[4:7]}.{cleaned[7:10]}"
    
    return phone  

def create_user_folders():
    folders = ["exports", "reports", "temp"]
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

def generate_appointment_times(start_hour=8, end_hour=17, interval_minutes=30):
    times = []
    
    current = datetime(2000, 1, 1, start_hour, 0)
    end = datetime(2000, 1, 1, end_hour, 0)
    
    while current <= end:
        times.append(current.strftime("%H:%M"))
        current += timedelta(minutes=interval_minutes)
    
    return times

def parse_id_from_combo_string(combo_string):
    if not combo_string or " - " not in combo_string:
        return None
    
    try:
        id_part = combo_string.split(" - ")[0]
        return int(id_part)
    except (ValueError, IndexError):
        return None

def format_full_name(ho, ten, include_title=False):
    if include_title:
        if ho.lower() in ["bác sĩ", "bs", "bs.", "bs "]:
            return f"{ho} {ten}"
        else:
            return f"BS. {ho} {ten}"
    else:
        return f"{ho} {ten}"

def get_weekday_name(date_str, format="%Y-%m-%d"):
    date_obj = datetime.strptime(date_str, format)
    weekday_names = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
    return weekday_names[date_obj.weekday()]

def truncate_text(text, max_length=50, ellipsis="..."):
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(ellipsis)] + ellipsis

def calculate_age(birth_date_str, format="%Y-%m-%d"):
    try:
        birth_date = datetime.strptime(birth_date_str, format)
        today = datetime.now()
        
        age = today.year - birth_date.year
        
        # Check if birthday has occurred this year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
            
        return age
    except ValueError:
        return None

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def lighter_color(hex_color, factor=0.2):
    r, g, b = hex_to_rgb(hex_color)
    
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    
    return rgb_to_hex(r, g, b)

def darker_color(hex_color, factor=0.2):
    r, g, b = hex_to_rgb(hex_color)
    
    r = max(0, int(r * (1 - factor)))
    g = max(0, int(g * (1 - factor)))
    b = max(0, int(b * (1 - factor)))
    
    return rgb_to_hex(r, g, b)