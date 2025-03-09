#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from datetime import datetime

def validate_required(value):
    return value is not None and str(value).strip() != ""

def validate_cmnd(cmnd):
    if not validate_required(cmnd):
        return False
    
    cmnd_str = str(cmnd).strip()
    
    if not re.match(r'^\d{9}(\d{3})?$', cmnd_str):
        return False
    
    return True

def validate_phone(phone):
    if not validate_required(phone):
        return True
    
    phone_str = str(phone).strip()
    
    if not re.match(r'^(\+84|0)\d{9,10}$', phone_str):
        return False
    
    return True

def validate_date(date_str, format="%Y-%m-%d"):
    if not validate_required(date_str):
        return False
    
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False

def validate_time(time_str, format="%H:%M"):
    if not validate_required(time_str):
        return False
    
    try:
        datetime.strptime(time_str, format)
        return True
    except ValueError:
        return False

def validate_gender(gender):
    if not validate_required(gender):
        return False
    
    valid_genders = ["Nam", "Nữ"]
    return str(gender).strip() in valid_genders

def validate_name(name):
    if not validate_required(name):
        return False
    
    name_str = str(name).strip()
    if len(name_str) < 2 or len(name_str) > 50:
        return False
    
    if re.search(r'[0-9!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|~`]', name_str):
        return False
    
    return True

def validate_email(email):
    if not validate_required(email):
        return True
    
    email_str = str(email).strip()
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email_str):
        return False
    
    return True

def validate_password(password):
    if not validate_required(password):
        return False
    
    password_str = str(password)
    
    if len(password_str) < 6:
        return False
    
    return True

def validate_username(username):
    if not validate_required(username):
        return False
    
    username_str = str(username).strip()
    
    if len(username_str) < 4 or len(username_str) > 20:
        return False
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username_str):
        return False
    
    return True

def validate_height(height):
    if not validate_required(height):
        return True
    
    try:
        height_val = float(height)
        return 50 <= height_val <= 250  
    except ValueError:
        return False

def validate_weight(weight):
    if not validate_required(weight):
        return True
    
    try:
        weight_val = float(weight)
        return 1 <= weight_val <= 500  # Reasonable weight range in kg
    except ValueError:
        return False

def validate_blood_type(blood_type):
    if not validate_required(blood_type):
        return True
    
    valid_blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    return str(blood_type).strip() in valid_blood_types

def validate_patient_data(data):
    errors = {}
    
    required_fields = ["Ho", "Ten", "CMND", "Gioitinh", "Ngaysinh"]
    for field in required_fields:
        if field not in data or not validate_required(data[field]):
            errors[field] = "Thông tin bắt buộc"
    
    if "CMND" in data and validate_required(data["CMND"]):
        if not validate_cmnd(data["CMND"]):
            errors["CMND"] = "CMND/CCCD không hợp lệ"
    
    if "SDT" in data and data["SDT"]:
        if not validate_phone(data["SDT"]):
            errors["SDT"] = "Số điện thoại không hợp lệ"
    
    if "Gioitinh" in data and validate_required(data["Gioitinh"]):
        if not validate_gender(data["Gioitinh"]):
            errors["Gioitinh"] = "Giới tính không hợp lệ"
    
    if "Ngaysinh" in data and validate_required(data["Ngaysinh"]):
        if not validate_date(data["Ngaysinh"]):
            errors["Ngaysinh"] = "Ngày sinh không hợp lệ"
    
    if "Ho" in data and validate_required(data["Ho"]):
        if not validate_name(data["Ho"]):
            errors["Ho"] = "Họ không hợp lệ"
    
    if "Ten" in data and validate_required(data["Ten"]):
        if not validate_name(data["Ten"]):
            errors["Ten"] = "Tên không hợp lệ"
    
    if "Email" in data and data["Email"]:
        if not validate_email(data["Email"]):
            errors["Email"] = "Email không hợp lệ"
    
    if "ChieuCao" in data and data["ChieuCao"]:
        if not validate_height(data["ChieuCao"]):
            errors["ChieuCao"] = "Chiều cao không hợp lệ"
    
    if "CanNang" in data and data["CanNang"]:
        if not validate_weight(data["CanNang"]):
            errors["CanNang"] = "Cân nặng không hợp lệ"
    
    if "NhomMau" in data and data["NhomMau"]:
        if not validate_blood_type(data["NhomMau"]):
            errors["NhomMau"] = "Nhóm máu không hợp lệ"
    
    return errors

def validate_doctor_data(data):
    errors = {}
    
    required_fields = ["Ho", "Ten", "CMND", "Gioitinh", "Ngaysinh", "ChuyenKhoa"]
    for field in required_fields:
        if field not in data or not validate_required(data[field]):
            errors[field] = "Thông tin bắt buộc"
    
    if "CMND" in data and validate_required(data["CMND"]):
        if not validate_cmnd(data["CMND"]):
            errors["CMND"] = "CMND/CCCD không hợp lệ"
    
    if "SDT" in data and data["SDT"]:
        if not validate_phone(data["SDT"]):
            errors["SDT"] = "Số điện thoại không hợp lệ"
    
    if "Gioitinh" in data and validate_required(data["Gioitinh"]):
        if not validate_gender(data["Gioitinh"]):
            errors["Gioitinh"] = "Giới tính không hợp lệ"
    
    if "Ngaysinh" in data and validate_required(data["Ngaysinh"]):
        if not validate_date(data["Ngaysinh"]):
            errors["Ngaysinh"] = "Ngày sinh không hợp lệ"
    
    if "Ho" in data and validate_required(data["Ho"]):
        if not validate_name(data["Ho"]):
            errors["Ho"] = "Họ không hợp lệ"
    
    if "Ten" in data and validate_required(data["Ten"]):
        if not validate_name(data["Ten"]):
            errors["Ten"] = "Tên không hợp lệ"
    
    if "Email" in data and data["Email"]:
        if not validate_email(data["Email"]):
            errors["Email"] = "Email không hợp lệ"
    
    if "username" in data and data["username"]:
        if not validate_username(data["username"]):
            errors["username"] = "Tên đăng nhập không hợp lệ"
    
    return errors

def validate_appointment_data(data):
    errors = {}
    
    required_fields = ["MaBN", "MaBS", "NgayKham", "GioKham"]
    for field in required_fields:
        if field not in data or not validate_required(data[field]):
            errors[field] = "Thông tin bắt buộc"
    
    if "NgayKham" in data and validate_required(data["NgayKham"]):
        if not validate_date(data["NgayKham"]):
            errors["NgayKham"] = "Ngày khám không hợp lệ"
    
    if "GioKham" in data and validate_required(data["GioKham"]):
        if not validate_time(data["GioKham"]):
            errors["GioKham"] = "Giờ khám không hợp lệ"
    
    if "TrangThai" in data and data["TrangThai"]:
        valid_statuses = ["Chờ khám", "Đang khám", "Đã khám", "Hủy"]
        if data["TrangThai"] not in valid_statuses:
            errors["TrangThai"] = "Trạng thái không hợp lệ"
    
    return errors

def validate_user_data(data):
    errors = {}
    
    required_fields = ["username", "pass", "Hovaten", "Gioitinh", "Quyen"]
    for field in required_fields:
        if field not in data or not validate_required(data[field]):
            errors[field] = "Thông tin bắt buộc"
    
    if "username" in data and validate_required(data["username"]):
        if not validate_username(data["username"]):
            errors["username"] = "Tên đăng nhập không hợp lệ"
    
    if "pass" in data and validate_required(data["pass"]):
        if not validate_password(data["pass"]):
            errors["pass"] = "Mật khẩu không hợp lệ"
    
    if "Hovaten" in data and validate_required(data["Hovaten"]):
        if not validate_name(data["Hovaten"]):
            errors["Hovaten"] = "Họ và tên không hợp lệ"
    
    if "Gioitinh" in data and validate_required(data["Gioitinh"]):
        if not validate_gender(data["Gioitinh"]):
            errors["Gioitinh"] = "Giới tính không hợp lệ"
    
    if "Quyen" in data and validate_required(data["Quyen"]):
        valid_roles = ["admin", "doctor", "staff"]
        if data["Quyen"] not in valid_roles:
            errors["Quyen"] = "Quyền không hợp lệ"
    
    if "SDT" in data and data["SDT"]:
        if not validate_phone(data["SDT"]):
            errors["SDT"] = "Số điện thoại không hợp lệ"
    
    if "email" in data and data["email"]:
        if not validate_email(data["email"]):
            errors["email"] = "Email không hợp lệ"
    
    return errors

def validate_medical_record_data(data):
    errors = {}
    
    required_fields = ["MaBN", "MaBS", "NgayKham", "ChanDoan"]
    for field in required_fields:
        if field not in data or not validate_required(data[field]):
            errors[field] = "Thông tin bắt buộc"
    
    if "NgayKham" in data and validate_required(data["NgayKham"]):
        if not validate_date(data["NgayKham"]):
            errors["NgayKham"] = "Ngày khám không hợp lệ"
    
    return errors