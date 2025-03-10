import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import calendar

from .base_view import BaseView
from controllers.schedule_controller import ScheduleController
from controllers.doctor_controller import DoctorController
from controllers.patient_controller import PatientController
from database.models import Appointment
from .custom_date_entry import CustomDateEntry


class ScheduleView(BaseView):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.controller = ScheduleController()
        self.doctor_controller = DoctorController()
        self.patient_controller = PatientController()

        self._create_content()
        self._load_appointments()
    
    def _create_content(self):
        self.clear()

        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        title_label = ttk.Label(top_frame, text="Quản lý lịch khám", style="Title.TLabel")
        title_label.pack(side=tk.LEFT, pady=10)

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._create_list_view()
        self._create_calendar_view()
        self._create_form_view()
    
    def show(self):
        super().show()
        
    def hide(self):
        super().hide()

    def _create_list_view(self):
        list_frame = ttk.Frame(self.notebook)
        self.notebook.add(list_frame, text="Danh sách lịch khám")

        controls_frame = ttk.Frame(list_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(controls_frame, text="Ngày khám:").pack(side=tk.LEFT, padx=5)

        self.date_entry = CustomDateEntry(controls_frame, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(side=tk.LEFT, padx=5)

        today = datetime.now()
        self.date_entry.set_date(today)
        
        search_date_button = ttk.Button(
            controls_frame, 
            text="Tìm", 
            command=self._search_by_date,
            width=8
        )
        search_date_button.pack(side=tk.LEFT, padx=5)

        ttk.Label(controls_frame, text="Bác sĩ:").pack(side=tk.LEFT, padx=5)
        self.doctor_combo = ttk.Combobox(controls_frame, width=25)
        self.doctor_combo.pack(side=tk.LEFT, padx=5)

        self._load_doctors_combo()
        
        search_doctor_button = ttk.Button(
            controls_frame, 
            text="Tìm", 
            command=self._search_by_doctor,
            width=8
        )
        search_doctor_button.pack(side=tk.LEFT, padx=5)

        columns = [
            ("MaLichKham", "Mã LK", 60),
            ("MaBN", "Mã BN", 60),
            ("TenBenhNhan", "Tên bệnh nhân", 150),
            ("MaBS", "Mã BS", 60),
            ("TenBacSi", "Tên bác sĩ", 150),
            ("NgayKham", "Ngày khám", 100),
            ("GioKham", "Giờ khám", 80),
            ("LydoKham", "Lý do khám", 200)
        ]
        
        self.schedule_tree, tree_frame = self.create_data_table(list_frame, columns)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        add_button = ttk.Button(
            button_frame, 
            text="Thêm", 
            command=self._show_add_form,
            width=12
        )
        add_button.pack(side=tk.LEFT, padx=5)
        
        edit_button = ttk.Button(
            button_frame, 
            text="Sửa", 
            command=self._show_edit_form,
            width=12
        )
        edit_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = ttk.Button(
            button_frame, 
            text="Xóa", 
            command=self._delete_appointment,
            width=12
        )
        delete_button.pack(side=tk.LEFT, padx=5)
        
        refresh_button = ttk.Button(
            button_frame, 
            text="Làm mới", 
            command=self._load_appointments,
            width=12
        )
        refresh_button.pack(side=tk.RIGHT, padx=5)

        self.schedule_tree.bind("<Double-1>", lambda event: self._show_edit_form())

    def _create_list_view(self):
        list_frame = ttk.Frame(self.notebook)
        self.notebook.add(list_frame, text="Danh sách lịch khám")

        controls_frame = ttk.Frame(list_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(controls_frame, text="Ngày khám:").pack(side=tk.LEFT, padx=5)

        self.date_entry = CustomDateEntry(controls_frame, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(side=tk.LEFT, padx=5)

        today = datetime.now()
        self.date_entry.set_date(today)

        search_date_button = ttk.Button(
            controls_frame,
            text="Tìm",
            command=self._search_by_date,
            width=8
        )
        search_date_button.pack(side=tk.LEFT, padx=5)

        ttk.Label(controls_frame, text="Bác sĩ:").pack(side=tk.LEFT, padx=5)
        self.doctor_combo = ttk.Combobox(controls_frame, width=25)
        self.doctor_combo.pack(side=tk.LEFT, padx=5)

        self._load_doctors_combo()

        search_doctor_button = ttk.Button(
            controls_frame,
            text="Tìm",
            command=self._search_by_doctor,
            width=8
        )
        search_doctor_button.pack(side=tk.LEFT, padx=5)

        columns = [
            ("MaLichKham", "Mã LK", 60),
            ("MaBN", "Mã BN", 60),
            ("TenBenhNhan", "Tên bệnh nhân", 150),
            ("MaBS", "Mã BS", 60),
            ("TenBacSi", "Tên bác sĩ", 150),
            ("NgayKham", "Ngày khám", 100),
            ("GioKham", "Giờ khám", 80),
            ("LydoKham", "Lý do khám", 200)
        ]

        self.schedule_tree, tree_frame = self.create_data_table(list_frame, columns)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        add_button = ttk.Button(
            button_frame,
            text="Thêm",
            command=self._show_add_form,
            width=12
        )
        add_button.pack(side=tk.LEFT, padx=5)

        edit_button = ttk.Button(
            button_frame,
            text="Sửa",
            command=self._show_edit_form,
            width=12
        )
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(
            button_frame,
            text="Xóa",
            command=self._delete_appointment,
            width=12
        )
        delete_button.pack(side=tk.LEFT, padx=5)

        refresh_button = ttk.Button(
            button_frame,
            text="Làm mới",
            command=self._load_appointments,
            width=12
        )
        refresh_button.pack(side=tk.RIGHT, padx=5)

        self.schedule_tree.bind("<Double-1>", lambda event: self._show_edit_form())

    def _create_calendar_view(self):
        calendar_frame = ttk.Frame(self.notebook)
        self.notebook.add(calendar_frame, text="Lịch theo ngày")

        nav_frame = ttk.Frame(calendar_frame)
        nav_frame.pack(fill=tk.X, padx=5, pady=5)

        prev_day_button = ttk.Button(
            nav_frame,
            text="<< Ngày trước",
            command=self._previous_day,
            width=15
        )
        prev_day_button.pack(side=tk.LEFT, padx=5)

        self.current_date = self._get_today()
        self.date_label = ttk.Label(nav_frame, text=self._format_date(self.current_date), font=("Arial", 12, "bold"))
        self.date_label.pack(side=tk.LEFT, padx=20)

        next_day_button = ttk.Button(
            nav_frame,
            text="Ngày sau >>",
            command=self._next_day,
            width=15
        )
        next_day_button.pack(side=tk.LEFT, padx=5)

        today_button = ttk.Button(
            nav_frame,
            text="Hôm nay",
            command=self._go_to_today,
            width=10
        )
        today_button.pack(side=tk.RIGHT, padx=5)

        self.time_slots_frame = ttk.Frame(calendar_frame)
        self.time_slots_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._load_calendar_view()

    def _create_form_view(self):
        self.form_frame = ttk.Frame(self.notebook, style="Form.TFrame")
        self.notebook.add(self.form_frame, text="Thêm/Cập nhật lịch khám")

        container = ttk.Frame(self.form_frame, style="Form.TFrame")
        container.pack(padx=20, pady=20)

        self.form_fields = {}

        form_title = ttk.Label(container, text="THÔNG TIN LỊCH KHÁM", style="Title.TLabel")
        form_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        fields = [
            {"name": "MaLichKham", "label": "Mã lịch khám:", "row": 1, "disabled": True},
            {"name": "MaBN", "label": "Mã bệnh nhân:", "row": 2, "required": True, "type": "combobox"},
            {"name": "TenBenhNhan", "label": "Tên bệnh nhân:", "row": 3, "disabled": True},
            {"name": "MaBS", "label": "Mã bác sĩ:", "row": 4, "required": True, "type": "combobox"},
            {"name": "TenBacSi", "label": "Tên bác sĩ:", "row": 5, "disabled": True},
            {"name": "NgayKham", "label": "Ngày khám:", "row": 6, "required": True, "type": "date"},
            {"name": "GioKham", "label": "Giờ khám:", "row": 7, "required": True, "default": "08:00"},
            {"name": "LydoKham", "label": "Lý do khám:", "row": 8, "type": "text"}
        ]

        for field in fields:
            ttk.Label(container, text=field["label"]).grid(
                row=field["row"], column=0, sticky="e", padx=5, pady=5)

            if field.get("type") == "combobox":
                widget = ttk.Combobox(container, width=30)
                widget.grid(row=field["row"], column=1, sticky="w", padx=5, pady=5)

                if field["name"] == "MaBN":
                    widget.bind("<<ComboboxSelected>>", self._on_patient_selected)
                elif field["name"] == "MaBS":
                    widget.bind("<<ComboboxSelected>>", self._on_doctor_selected)
            elif field.get("type") == "text":
                widget = tk.Text(container, width=30, height=4)
                widget.grid(row=field["row"], column=1, sticky="w", padx=5, pady=5)
            elif field.get("type") == "date":
                widget = CustomDateEntry(container, date_pattern='yyyy-mm-dd')
                widget.grid(row=field["row"], column=1, sticky="w", padx=5, pady=5)
            else:
                widget = ttk.Entry(container, width=30)
                widget.grid(row=field["row"], column=1, sticky="w", padx=5, pady=5)

                if "default" in field:
                    widget.insert(0, field["default"])

            if field.get("disabled"):
                widget.configure(state="disabled")

            self.form_fields[field["name"]] = widget

        button_frame = ttk.Frame(container)
        button_frame.grid(row=9, column=0, columnspan=2, pady=20)

        self.save_button = ttk.Button(
            button_frame,
            text="Lưu",
            command=self._save_appointment,
            style="Primary.TButton",
            width=15
        )
        self.save_button.pack(side=tk.LEFT, padx=10)

        cancel_button = ttk.Button(
            button_frame,
            text="Hủy",
            command=self._cancel_form,
            width=15
        )
        cancel_button.pack(side=tk.LEFT, padx=10)
        self._load_form_combos()

        self.form_mode = "add"
        self.current_appointment_id = None

    def _load_form_combos(self):
        patients = self.patient_controller.get_all_patients()
        patient_values = [f"{p['MaBN']} - {p['Ho']} {p['Ten']}" for p in patients]
        if "MaBN" in self.form_fields:
            self.form_fields["MaBN"].configure(values=patient_values)

        self.patients_data = {p['MaBN']: p for p in patients}

        doctors = self.doctor_controller.get_all_doctors()
        doctor_values = [f"{d['MaBS']} - {d['Ho']} {d['Ten']} ({d['ChuyenKhoa']})" for d in doctors]
        if "MaBS" in self.form_fields:
            self.form_fields["MaBS"].configure(values=doctor_values)

        self.doctors_data = {d['MaBS']: d for d in doctors}

    def _on_patient_selected(self, event):
        if "MaBN" not in self.form_fields or "TenBenhNhan" not in self.form_fields:
            return

        selected = self.form_fields["MaBN"].get()
        if not selected:
            return

        try:
            patient_id = int(selected.split(' - ')[0])

            if patient_id in self.patients_data:
                patient = self.patients_data[patient_id]

                name_field = self.form_fields["TenBenhNhan"]
                name_field.configure(state="normal")
                name_field.delete(0, tk.END)
                name_field.insert(0, f"{patient['Ho']} {patient['Ten']}")
                name_field.configure(state="disabled")
        except (ValueError, IndexError):
            pass

    def _on_doctor_selected(self, event):
        if "MaBS" not in self.form_fields or "TenBacSi" not in self.form_fields:
            return

        selected = self.form_fields["MaBS"].get()
        if not selected:
            return

        try:
            doctor_id = int(selected.split(' - ')[0])

            if doctor_id in self.doctors_data:
                doctor = self.doctors_data[doctor_id]
                name_field = self.form_fields["TenBacSi"]
                name_field.configure(state="normal")
                name_field.delete(0, tk.END)
                name_field.insert(0, f"{doctor['Ho']} {doctor['Ten']} - {doctor['ChuyenKhoa']}")
                name_field.configure(state="disabled")
        except (ValueError, IndexError):
            pass

    def _get_today(self):
        return datetime.now().strftime("%Y-%m-%d")

    def _format_date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%d/%m/%Y - %A")
        except ValueError:
            return date_str

    def _format_date_for_db(self, date_str):
        if not date_str:
            return None
        try:
            day, month, year = date_str.split('/')
            return f"{year}-{month}-{day}"
        except ValueError:
            return date_str

    def _load_doctors_combo(self):
        doctors = self.doctor_controller.get_all_doctors()
        doctor_values = [""] + [f"{d['MaBS']} - {d['Ho']} {d['Ten']}" for d in doctors]
        self.doctor_combo.configure(values=doctor_values)

    def _load_appointments(self):
        self.schedule_tree.delete(*self.schedule_tree.get_children())
        appointments = self.controller.get_all_appointments()
        self._populate_appointments_tree(appointments)
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 1:  # Calendar view tab
            self._load_calendar_view()

    def _populate_appointments_tree(self, appointments):
        for appt in appointments:
            values = (
                appt.get("MaLichKham", ""),
                appt.get("MaBN", ""),
                appt.get("TenBenhNhan", ""),
                appt.get("MaBS", ""),
                appt.get("TenBacSi", ""),
                appt.get("NgayKham", ""),
                appt.get("GioKham", ""),
                appt.get("LydoKham", "")
            )
            self.schedule_tree.insert("", "end", values=values)

    def _search_by_date(self):
        # Lấy ngày khám từ CustomDateEntry
        date_str = self.date_entry.get()
        date = self._format_date_for_db(date_str)

        if not date:
            self._load_appointments()
            return

        self.schedule_tree.delete(*self.schedule_tree.get_children())
        appointments = self.controller.get_appointments_by_date(date)
        self._populate_appointments_tree(appointments)

    def _search_by_doctor(self):
        selected = self.doctor_combo.get()
        if not selected:
            self._load_appointments()
            return

        try:
            doctor_id = int(selected.split(' - ')[0])
            self.schedule_tree.delete(*self.schedule_tree.get_children())
            appointments = self.controller.get_doctor_appointments(doctor_id)

            self._populate_appointments_tree(appointments)
        except (ValueError, IndexError):
            self._load_appointments()

    def _load_calendar_view(self):
        for widget in self.time_slots_frame.winfo_children():
            widget.destroy()

        self.date_label.configure(text=self._format_date(self.current_date))
        appointments = self.controller.get_appointments_by_date(self.current_date)
        appt_by_time = {}
        for appt in appointments:
            time_key = appt.get("GioKham", "")
            if time_key not in appt_by_time:
                appt_by_time[time_key] = []
            appt_by_time[time_key].append(appt)
        header_frame = ttk.Frame(self.time_slots_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(header_frame, text="Thời gian", width=10, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Label(header_frame, text="Bác sĩ", width=20, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Label(header_frame, text="Bệnh nhân", width=20, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Label(header_frame, text="Lý do khám", width=30, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

        for hour in range(8, 18):
            for minute in [0, 30]:
                time_str = f"{hour:02d}:{minute:02d}"

                row_frame = ttk.Frame(self.time_slots_frame)
                row_frame.pack(fill=tk.X, pady=2)

                time_label = ttk.Label(row_frame, text=time_str, width=10)
                time_label.pack(side=tk.LEFT, padx=5)

                if time_str in appt_by_time:
                    for i, appt in enumerate(appt_by_time[time_str]):
                        if i > 0:
                            row_frame = ttk.Frame(self.time_slots_frame)
                            row_frame.pack(fill=tk.X, pady=2)
                            ttk.Label(row_frame, text="", width=10).pack(side=tk.LEFT, padx=5)

                        doctor_label = ttk.Label(row_frame, text=appt.get("TenBacSi", ""), width=20)
                        doctor_label.pack(side=tk.LEFT, padx=5)

                        patient_label = ttk.Label(row_frame, text=appt.get("TenBenhNhan", ""), width=20)
                        patient_label.pack(side=tk.LEFT, padx=5)

                        reason_label = ttk.Label(row_frame, text=appt.get("LydoKham", ""), width=30)
                        reason_label.pack(side=tk.LEFT, padx=5)

                        edit_button = ttk.Button(
                            row_frame,
                            text="Sửa",
                            command=lambda a=appt: self._edit_from_calendar(a),
                            width=8
                        )
                        edit_button.pack(side=tk.LEFT, padx=5)
                else:
                    empty_frame = ttk.Frame(row_frame)
                    empty_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

                    add_button = ttk.Button(
                        row_frame,
                        text="+",
                        command=lambda t=time_str: self._add_at_time(t),
                        width=5
                    )
                    add_button.pack(side=tk.RIGHT, padx=5)

    def _previous_day(self):
        try:
            date_obj = datetime.strptime(self.current_date, "%Y-%m-%d")
            prev_day = date_obj - timedelta(days=1)
            self.current_date = prev_day.strftime("%Y-%m-%d")
            self._load_calendar_view()
        except ValueError:
            pass

    def _next_day(self):
        try:
            date_obj = datetime.strptime(self.current_date, "%Y-%m-%d")
            next_day = date_obj + timedelta(days=1)
            self.current_date = next_day.strftime("%Y-%m-%d")
            self._load_calendar_view()
        except ValueError:
            pass

    def _go_to_today(self):
        self.current_date = self._get_today()
        self._load_calendar_view()

    def _add_at_time(self, time_str):
        self._show_add_form()

        if "GioKham" in self.form_fields:
            self.form_fields["GioKham"].delete(0, tk.END)
            self.form_fields["GioKham"].insert(0, time_str)

        if "NgayKham" in self.form_fields and isinstance(self.form_fields["NgayKham"], CustomDateEntry):
            try:
                date_obj = datetime.strptime(self.current_date, "%Y-%m-%d")
                self.form_fields["NgayKham"].set_date(date_obj)
            except ValueError:
                pass

    def _edit_from_calendar(self, appointment):
        self._show_edit_form(appointment["MaLichKham"])

    def _show_add_form(self):
        self.notebook.select(2)

        for field_name, widget in self.form_fields.items():
            if field_name == "MaLichKham":
                # Để trống trường MaLichKham vì nó là tự động tăng
                widget.configure(state="normal")
                widget.delete(0, tk.END)
                widget.insert(0, "(Tự động tạo)")
                widget.configure(state="disabled")
            elif field_name != "TenBenhNhan" and field_name != "TenBacSi":
                if isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                elif isinstance(widget, CustomDateEntry):
                    today = datetime.now()
                    widget.set_date(today)
                else:
                    widget.delete(0, tk.END)
                    if field_name == "GioKham":
                        widget.insert(0, "08:00")

        for field_name in ["TenBenhNhan", "TenBacSi"]:
            if field_name in self.form_fields:
                widget = self.form_fields[field_name]
                widget.configure(state="normal")
                widget.delete(0, tk.END)
                widget.configure(state="disabled")

        self.form_mode = "add"
        self.current_appointment_id = None

        self.notebook.tab(2, text="Thêm lịch khám mới")

    def _show_edit_form(self, appointment_id=None):
        if appointment_id is None:
            selected_items = self.schedule_tree.selection()

            if not selected_items:
                self.show_error("Lỗi", "Vui lòng chọn lịch khám để sửa!")
                return

            values = self.schedule_tree.item(selected_items[0], "values")
            appointment_id = values[0]

        appointment = self.controller.get_appointment(appointment_id)

        if not appointment:
            self.show_error("Lỗi", "Không thể tải thông tin lịch khám!")
            return

        self.notebook.select(2)

        for field_name, widget in self.form_fields.items():
            if field_name in appointment:
                if isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                    widget.insert("1.0", str(appointment[field_name] or ""))
                elif isinstance(widget, CustomDateEntry):
                    if appointment[field_name]:
                        try:
                            date_parts = appointment[field_name].split('-')
                            if len(date_parts) == 3:
                                year, month, day = date_parts
                                date_obj = datetime(int(year), int(month), int(day))
                                widget.set_date(date_obj)
                        except (ValueError, TypeError):
                            pass
                else:
                    was_disabled = False
                    if widget.cget("state") == "disabled":
                        was_disabled = True
                        widget.configure(state="normal")

                    widget.delete(0, tk.END)
                    widget.insert(0, str(appointment[field_name] or ""))

                    if was_disabled:
                        widget.configure(state="disabled")

            if field_name == "MaBN" and appointment.get("MaBN"):
                for value in self.form_fields["MaBN"]['values']:
                    if value.startswith(f"{appointment['MaBN']} - "):
                        self.form_fields["MaBN"].set(value)
                        self._on_patient_selected(None)
                        break

            if field_name == "MaBS" and appointment.get("MaBS"):
                for value in self.form_fields["MaBS"]['values']:
                    if value.startswith(f"{appointment['MaBS']} - "):
                        self.form_fields["MaBS"].set(value)
                        self._on_doctor_selected(None)
                        break

        self.form_mode = "edit"
        self.current_appointment_id = appointment_id

        self.notebook.tab(2, text="Cập nhật lịch khám")

    def _save_appointment(self):
        appointment_data = {}
        required_fields = ["MaBN", "MaBS", "NgayKham", "GioKham"]

        for field_name, widget in self.form_fields.items():
            if field_name not in ["MaLichKham", "TenBenhNhan", "TenBacSi"]:
                if isinstance(widget, tk.Text):
                    appointment_data[field_name] = widget.get("1.0", tk.END).strip()
                elif isinstance(widget, CustomDateEntry):
                    date_str = widget.get()
                    appointment_data[field_name] = self._format_date_for_db(date_str)
                else:
                    value = widget.get().strip()
                    if field_name in ["MaBN", "MaBS"] and " - " in value:
                        try:
                            appointment_data[field_name] = int(value.split(" - ")[0])
                        except ValueError:
                            appointment_data[field_name] = value
                    else:
                        appointment_data[field_name] = value

        for field in required_fields:
            if not appointment_data.get(field):
                self.show_error("Lỗi", "Vui lòng điền đầy đủ thông tin bắt buộc!")
                return

        success = False
        if self.form_mode == "add":
            success = self.controller.add_appointment(appointment_data)
            message = "Thêm lịch khám thành công!"
        else:
            success = self.controller.update_appointment(self.current_appointment_id, appointment_data)
            message = "Cập nhật lịch khám thành công!"

        if success:
            self.show_info("Thành công", message)
            self._load_appointments()
            self._cancel_form()
        else:
            self.show_error("Lỗi", "Không thể lưu thông tin lịch khám. Vui lòng kiểm tra lại!")

    def _cancel_form(self):
        self.notebook.select(0)

        self.form_mode = "add"
        self.current_appointment_id = None

    def _delete_appointment(self):
        selected_items = self.schedule_tree.selection()

        if not selected_items:
            self.show_error("Lỗi", "Vui lòng chọn lịch khám để xóa!")
            return

        values = self.schedule_tree.item(selected_items[0], "values")
        appointment_id = values[0]
        confirm = self.ask_yes_no(
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa lịch khám này?"
        )

        if not confirm:
            return
        success = self.controller.delete_appointment(appointment_id)

        if success:
            self.show_info("Thành công", "Xóa lịch khám thành công!")
            self._load_appointments()
        else:
            self.show_error("Lỗi", "Không thể xóa lịch khám!")

    def on_resize(self, width, height):
        if width > 1200:
            self.schedule_tree.column("TenBenhNhan", width=200)
            self.schedule_tree.column("TenBacSi", width=200)
            self.schedule_tree.column("LydoKham", width=250)
        elif width > 800:
            self.schedule_tree.column("TenBenhNhan", width=150)
            self.schedule_tree.column("TenBacSi", width=150)
            self.schedule_tree.column("LydoKham", width=200)
        else:
            self.schedule_tree.column("TenBenhNhan", width=120)
            self.schedule_tree.column("TenBacSi", width=120)
            self.schedule_tree.column("LydoKham", width=150)