import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_view import BaseView
from controllers.patient_controller import PatientController
from database.models import Patient
from .custom_date_entry import CustomDateEntry


class PatientView(BaseView):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.controller = PatientController()
        self._create_content()
        self._load_patients()

    def _create_content(self):
        self.clear()

        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        title_label = ttk.Label(top_frame, text="Quản lý bệnh nhân", font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT, pady=10)

        search_frame = ttk.Frame(top_frame)
        search_frame.pack(side=tk.RIGHT)

        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=25)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_button = ttk.Button(
            search_frame,
            text="Tìm",
            command=self._search_patients,
            width=8
        )
        search_button.pack(side=tk.LEFT, padx=5)

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._create_table_view()
        self._create_form_view()

    def _create_table_view(self):
        table_frame = ttk.Frame(self.notebook)
        self.notebook.add(table_frame, text="Danh sách bệnh nhân")

        columns = [
            ("MaBN", "Mã BN", 60),
            ("Ho", "Họ", 120),
            ("Ten", "Tên", 100),
            ("CMND", "CMND", 100),
            ("Gioitinh", "Giới tính", 80),
            ("Ngaysinh", "Ngày sinh", 100),
            ("SDT", "SĐT", 100),
            ("Quequan", "Quê quán", 150),
            ("Ngaykham", "Ngày khám", 100)
        ]

        self.patient_tree, tree_frame = self.create_data_table(table_frame, columns)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        button_frame = ttk.Frame(table_frame)
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
            command=self._delete_patient,
            width=12
        )
        delete_button.pack(side=tk.LEFT, padx=5)

        refresh_button = ttk.Button(
            button_frame,
            text="Làm mới",
            command=self._load_patients,
            width=12
        )
        refresh_button.pack(side=tk.RIGHT, padx=5)

        self.patient_tree.bind("<Double-1>", lambda event: self._show_edit_form())

    def _create_form_view(self):
        self.form_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.form_frame, text="Thêm/Cập nhật bệnh nhân")

        container = ttk.Frame(self.form_frame)
        container.pack(padx=20, pady=20)

        self.form_fields = {}

        form_title = ttk.Label(container, text="THÔNG TIN BỆNH NHÂN", font=("Arial", 14, "bold"))
        form_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        fields_left = [
            {"name": "MaBN", "label": "Mã bệnh nhân:", "row": 1, "disabled": True},
            {"name": "Ho", "label": "Họ:", "row": 2, "required": True},
            {"name": "Ten", "label": "Tên:", "row": 3, "required": True},
            {"name": "CMND", "label": "CMND:", "row": 4, "required": True},
            {"name": "Gioitinh", "label": "Giới tính:", "row": 5, "required": True, "type": "combobox",
             "values": ["Nam", "Nữ"]},
            {"name": "Ngaysinh", "label": "Ngày sinh:", "row": 6, "required": True, "type": "date"},
            {"name": "SDT", "label": "SĐT:", "row": 7},
            {"name": "Quequan", "label": "Quê quán:", "row": 8},
            {"name": "Ngaykham", "label": "Ngày khám:", "row": 9, "type": "date"}
        ]

        for field in fields_left:
            ttk.Label(container, text=field["label"]).grid(
                row=field["row"], column=0, sticky="e", padx=5, pady=5)

            if field.get("type") == "combobox":
                widget = ttk.Combobox(container, values=field.get("values", []), width=30)
                widget.grid(row=field["row"], column=1, sticky="w", padx=5, pady=5)
            elif field.get("type") == "date":
                widget = CustomDateEntry(container, date_pattern='yyyy-mm-dd')
                widget.grid(row=field["row"], column=1, sticky="w", padx=5, pady=5)
            else:
                widget = ttk.Entry(container, width=30)
                widget.grid(row=field["row"], column=1, sticky="w", padx=5, pady=5)

            if field.get("disabled"):
                widget.configure(state="disabled")

            self.form_fields[field["name"]] = widget

        ttk.Separator(container, orient="vertical").grid(
            row=1, column=2, rowspan=12, sticky="ns", padx=20)

        fields_right = [
            {"name": "DiaChi", "label": "Địa chỉ:", "row": 1},
            {"name": "Email", "label": "Email:", "row": 2},
            {"name": "NhomMau", "label": "Nhóm máu:", "row": 3, "type": "combobox",
             "values": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]},
            {"name": "ChieuCao", "label": "Chiều cao (cm):", "row": 4},
            {"name": "CanNang", "label": "Cân nặng (kg):", "row": 5},
            {"name": "TienSuBenhAn", "label": "Tiền sử bệnh:", "row": 6, "type": "text"},
            {"name": "DiUng", "label": "Dị ứng:", "row": 7},
            {"name": "GhiChu", "label": "Ghi chú:", "row": 8, "type": "text"}
        ]

        for field in fields_right:
            ttk.Label(container, text=field["label"]).grid(
                row=field["row"], column=3, sticky="e", padx=5, pady=5)

            if field.get("type") == "combobox":
                widget = ttk.Combobox(container, values=field.get("values", []), width=30)
                widget.grid(row=field["row"], column=4, sticky="w", padx=5, pady=5)
            elif field.get("type") == "text":
                widget = tk.Text(container, width=30, height=4)
                widget.grid(row=field["row"], column=4, sticky="w", padx=5, pady=5)
            else:
                widget = ttk.Entry(container, width=30)
                widget.grid(row=field["row"], column=4, sticky="w", padx=5, pady=5)

            self.form_fields[field["name"]] = widget

        button_frame = ttk.Frame(container)
        button_frame.grid(row=12, column=0, columnspan=5, pady=20)

        self.save_button = ttk.Button(
            button_frame,
            text="Lưu",
            command=self._save_patient,
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

        self.form_mode = "add"
        self.current_patient_id = None

    def _get_today(self):
        return datetime.now().strftime("%Y-%m-%d")

    def _format_date_for_db(self, date_str):
        if not date_str:
            return None
        try:
            day, month, year = date_str.split('/')
            return f"{year}-{month}-{day}"
        except ValueError:
            return date_str

    def _format_date_for_display(self, date_str):
        if not date_str:
            return None
        try:
            year, month, day = date_str.split('-')
            return f"{day}/{month}/{year}"
        except ValueError:
            return date_str

    def _load_patients(self):
        self.patient_tree.delete(*self.patient_tree.get_children())
        patients = self.controller.get_all_patients()
        for patient in patients:
            ngaysinh = self._format_date_for_display(patient.get("Ngaysinh", ""))
            ngaykham = self._format_date_for_display(patient.get("Ngaykham", ""))

            values = (
                patient["MaBN"],
                patient["Ho"],
                patient["Ten"],
                patient["CMND"],
                patient["Gioitinh"],
                ngaysinh,
                patient["SDT"],
                patient["Quequan"],
                ngaykham
            )
            self.patient_tree.insert("", "end", values=values)

    def _search_patients(self):
        search_term = self.search_entry.get().strip()

        if not search_term:
            self._load_patients()
            return

        self.patient_tree.delete(*self.patient_tree.get_children())
        patients = self.controller.search_patients(search_term)
        for patient in patients:
            ngaysinh = self._format_date_for_display(patient.get("Ngaysinh", ""))
            ngaykham = self._format_date_for_display(patient.get("Ngaykham", ""))

            values = (
                patient["MaBN"],
                patient["Ho"],
                patient["Ten"],
                patient["CMND"],
                patient["Gioitinh"],
                ngaysinh,
                patient["SDT"],
                patient["Quequan"],
                ngaykham
            )
            self.patient_tree.insert("", "end", values=values)

    def _show_add_form(self):
        self.notebook.select(1)

        for field_name, widget in self.form_fields.items():
            if field_name == "MaBN":
                # Để trống trường MaBN vì nó là tự động tăng
                widget.configure(state="normal")
                widget.delete(0, tk.END)
                widget.insert(0, "(Tự động tạo)")
                widget.configure(state="disabled")
            else:
                if isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                elif isinstance(widget, CustomDateEntry):
                    today = datetime.now()
                    widget.set_date(today)
                else:
                    widget.delete(0, tk.END)

        self.form_mode = "add"
        self.current_patient_id = None

        self.notebook.tab(1, text="Thêm bệnh nhân mới")

    def _show_edit_form(self):
        selected_items = self.patient_tree.selection()

        if not selected_items:
            self.show_error("Lỗi", "Vui lòng chọn bệnh nhân để sửa!")
            return

        values = self.patient_tree.item(selected_items[0], "values")
        patient_id = values[0]

        patient = self.controller.get_patient(patient_id)

        if not patient:
            self.show_error("Lỗi", "Không thể tải thông tin bệnh nhân!")
            return

        self.notebook.select(1)

        for field_name, widget in self.form_fields.items():
            if field_name in patient:
                if isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                    if patient[field_name]:
                        widget.insert("1.0", str(patient[field_name]))
                elif isinstance(widget, CustomDateEntry):
                    if patient[field_name]:
                        try:
                            date_parts = patient[field_name].split('-')
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
                    if patient[field_name] is not None:
                        widget.insert(0, str(patient[field_name]))

                    if was_disabled:
                        widget.configure(state="disabled")

        self.form_mode = "edit"
        self.current_patient_id = patient_id

        self.notebook.tab(1, text="Cập nhật thông tin bệnh nhân")

    def _save_patient(self):
        patient_data = {}
        required_fields = ["Ho", "Ten", "CMND", "Gioitinh", "Ngaysinh"]

        for field_name, widget in self.form_fields.items():
            if field_name != "MaBN":  
                if isinstance(widget, tk.Text):
                    patient_data[field_name] = widget.get("1.0", tk.END).strip()
                elif isinstance(widget, CustomDateEntry):
                    date_str = widget.get()
                    patient_data[field_name] = self._format_date_for_db(date_str)
                else:
                    patient_data[field_name] = widget.get().strip()

        for field in required_fields:
            if not patient_data.get(field):
                self.show_error("Lỗi", f"Vui lòng điền đầy đủ thông tin bắt buộc!")
                return

        success = False
        if self.form_mode == "add":
            success = self.controller.add_patient(patient_data)
            message = "Thêm bệnh nhân thành công!"
        else:
            success = self.controller.update_patient(self.current_patient_id, patient_data)
            message = "Cập nhật thông tin bệnh nhân thành công!"

        if success:
            self.show_info("Thành công", message)
            self._load_patients()
            self._cancel_form()
        else:
            self.show_error("Lỗi", "Không thể lưu thông tin bệnh nhân. Vui lòng kiểm tra lại!")

    def _cancel_form(self):
        self.notebook.select(0)
        self.form_mode = "add"
        self.current_patient_id = None

    def _delete_patient(self):
        selected_items = self.patient_tree.selection()

        if not selected_items:
            self.show_error("Lỗi", "Vui lòng chọn bệnh nhân để xóa!")
            return
        values = self.patient_tree.item(selected_items[0], "values")
        patient_id = values[0]

        confirm = self.ask_yes_no(
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa bệnh nhân {values[1]} {values[2]}?"
        )

        if not confirm:
            return
        success = self.controller.delete_patient(patient_id)

        if success:
            self.show_info("Thành công", "Xóa bệnh nhân thành công!")
            self._load_patients()
        else:
            self.show_error(
                "Lỗi",
                "Không thể xóa bệnh nhân. Bệnh nhân có thể đang có lịch khám!"
            )

    def on_resize(self, width, height):
        if width > 1200:
            self.patient_tree.column("Ho", width=150)
            self.patient_tree.column("Ten", width=120)
            self.patient_tree.column("CMND", width=120)
            self.patient_tree.column("Quequan", width=200)
        elif width > 800:
            self.patient_tree.column("Ho", width=120)
            self.patient_tree.column("Ten", width=100)
            self.patient_tree.column("CMND", width=100)
            self.patient_tree.column("Quequan", width=150)
        else:
            self.patient_tree.column("Ho", width=100)
            self.patient_tree.column("Ten", width=80)
            self.patient_tree.column("CMND", width=80)
            self.patient_tree.column("Quequan", width=120)