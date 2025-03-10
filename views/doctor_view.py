import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_view import BaseView
from controllers.doctor_controller import DoctorController
from database.models import Doctor
from .custom_date_entry import CustomDateEntry


class DoctorView(BaseView):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.controller = DoctorController()
        self._create_content()

        self._load_doctors()

    def _create_content(self):
        self.clear()
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        title_label = ttk.Label(top_frame, text="Quản lý bác sĩ", style="Title.TLabel")
        title_label.pack(side=tk.LEFT, pady=10)
        search_frame = ttk.Frame(top_frame)
        search_frame.pack(side=tk.RIGHT)

        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=25)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_button = ttk.Button(
            search_frame,
            text="Tìm",
            command=self._search_doctors,
            width=8
        )
        search_button.pack(side=tk.LEFT, padx=5)
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._create_table_view()
        self._create_form_view()

    def _create_table_view(self):
        table_frame = ttk.Frame(self.notebook)
        self.notebook.add(table_frame, text="Danh sách bác sĩ")

        columns = [
            ("MaBS", "Mã BS", 60),
            ("Ho", "Họ", 120),
            ("Ten", "Tên", 100),
            ("CMND", "CMND", 100),
            ("Gioitinh", "Giới tính", 80),
            ("Ngaysinh", "Ngày sinh", 100),
            ("SDT", "SĐT", 100),
            ("ChuyenKhoa", "Chuyên khoa", 150)
        ]

        self.doctor_tree, tree_frame = self.create_data_table(table_frame, columns)
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
            command=self._delete_doctor,
            width=12
        )
        delete_button.pack(side=tk.LEFT, padx=5)

        refresh_button = ttk.Button(
            button_frame,
            text="Làm mới",
            command=self._load_doctors,
            width=12
        )
        refresh_button.pack(side=tk.RIGHT, padx=5)
        self.doctor_tree.bind("<Double-1>", lambda event: self._show_edit_form())

    def _create_form_view(self):
        self.form_frame = ttk.Frame(self.notebook, style="Form.TFrame")
        self.notebook.add(self.form_frame, text="Thêm/Cập nhật bác sĩ")

        container = ttk.Frame(self.form_frame, style="Form.TFrame")
        container.pack(padx=20, pady=20)

        self.form_fields = {}

        form_title = ttk.Label(container, text="THÔNG TIN BÁC SĨ", style="Title.TLabel")
        form_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        fields = [
            {"name": "MaBS", "label": "Mã bác sĩ:", "row": 1, "disabled": True},
            {"name": "Ho", "label": "Họ:", "row": 2, "required": True},
            {"name": "Ten", "label": "Tên:", "row": 3, "required": True},
            {"name": "CMND", "label": "CMND:", "row": 4, "required": True},
            {"name": "Gioitinh", "label": "Giới tính:", "row": 5, "required": True, "type": "combobox",
             "values": ["Nam", "Nữ"]},
            {"name": "Ngaysinh", "label": "Ngày sinh:", "row": 6, "required": True, "type": "date"},
            {"name": "SDT", "label": "SĐT:", "row": 7},
            {"name": "ChuyenKhoa", "label": "Chuyên khoa:", "row": 8, "required": True},
            {"name": "Email", "label": "Email:", "row": 9},
            {"name": "DiaChi", "label": "Địa chỉ:", "row": 10},
            {"name": "BangCap", "label": "Bằng cấp:", "row": 11},
            {"name": "GhiChu", "label": "Ghi chú:", "row": 12, "type": "text"},
            {"name": "username", "label": "Tài khoản:", "row": 13}
        ]

        for field in fields:
            ttk.Label(container, text=field["label"]).grid(
                row=field["row"], column=0, sticky="e", padx=5, pady=5)

            if field.get("type") == "combobox":
                widget = ttk.Combobox(container, values=field.get("values", []), width=30)
                widget.grid(row=field["row"], column=1, sticky="w", padx=5, pady=5)
            elif field.get("type") == "date":
                widget = CustomDateEntry(container, date_pattern='yyyy-mm-dd')
                widget.grid(row=field["row"], column=1, sticky="w", padx=5, pady=5)
            elif field.get("type") == "text":
                widget = tk.Text(container, width=30, height=4)
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
        button_frame.grid(row=14, column=0, columnspan=2, pady=20)

        self.save_button = ttk.Button(
            button_frame,
            text="Lưu",
            command=self._save_doctor,
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

        self.form_mode = "add"
        self.current_doctor_id = None

    def _format_date_for_display(self, date_str):
        if not date_str:
            return None
        try:
            year, month, day = date_str.split('-')
            return f"{day}/{month}/{year}"
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

    def _load_doctors(self):
        self.doctor_tree.delete(*self.doctor_tree.get_children())
        doctors = self.controller.get_all_doctors()
        for doctor in doctors:
            ngaysinh = self._format_date_for_display(doctor.get("Ngaysinh", ""))
            values = (
                doctor["MaBS"],
                doctor["Ho"],
                doctor["Ten"],
                doctor["CMND"],
                doctor["Gioitinh"],
                ngaysinh,
                doctor["SDT"],
                doctor["ChuyenKhoa"]
            )
            self.doctor_tree.insert("", "end", values=values)

    def _search_doctors(self):
        search_term = self.search_entry.get().strip()

        if not search_term:
            self._load_doctors()
            return

        self.doctor_tree.delete(*self.doctor_tree.get_children())
        doctors = self.controller.search_doctors(search_term)

        for doctor in doctors:
            ngaysinh = self._format_date_for_display(doctor.get("Ngaysinh", ""))
            values = (
                doctor["MaBS"],
                doctor["Ho"],
                doctor["Ten"],
                doctor["CMND"],
                doctor["Gioitinh"],
                ngaysinh,
                doctor["SDT"],
                doctor["ChuyenKhoa"]
            )
            self.doctor_tree.insert("", "end", values=values)

    def _show_add_form(self):
        self.notebook.select(1)
        for field_name, widget in self.form_fields.items():
            if field_name == "MaBS":
                new_id = self._get_next_doctor_id()
                widget.configure(state="normal")
                widget.delete(0, tk.END)
                widget.insert(0, str(new_id))
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
        self.current_doctor_id = None

        self.notebook.tab(1, text="Thêm bác sĩ mới")

    def _get_next_doctor_id(self):
        doctors = self.controller.get_all_doctors()
        if not doctors:
            return 1

        max_id = max(int(doctor.get("MaBS", 0)) for doctor in doctors)
        return max_id + 1

    def _show_edit_form(self):
        selected_items = self.doctor_tree.selection()

        if not selected_items:
            self.show_error("Lỗi", "Vui lòng chọn bác sĩ để sửa!")
            return

        values = self.doctor_tree.item(selected_items[0], "values")
        doctor_id = values[0]

        doctor = self.controller.get_doctor(doctor_id)

        if not doctor:
            self.show_error("Lỗi", "Không thể tải thông tin bác sĩ!")
            return

        self.notebook.select(1)

        for field_name, widget in self.form_fields.items():
            if field_name in doctor:
                if isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                    if doctor[field_name]:
                        widget.insert("1.0", str(doctor[field_name]))
                elif isinstance(widget, CustomDateEntry):
                    if doctor[field_name]:
                        try:
                            date_parts = doctor[field_name].split('-')
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
                    if doctor[field_name] is not None:
                        widget.insert(0, str(doctor[field_name]))

                    if was_disabled:
                        widget.configure(state="disabled")

        self.form_mode = "edit"
        self.current_doctor_id = doctor_id

        self.notebook.tab(1, text="Cập nhật thông tin bác sĩ")

    def _save_doctor(self):
        doctor_data = {}
        required_fields = ["Ho", "Ten", "CMND", "Gioitinh", "Ngaysinh", "ChuyenKhoa"]

        for field_name, widget in self.form_fields.items():
            if field_name != "MaBS" or self.form_mode == "add":
                if isinstance(widget, tk.Text):
                    doctor_data[field_name] = widget.get("1.0", tk.END).strip()
                elif isinstance(widget, CustomDateEntry):

                    date_str = widget.get()
                    doctor_data[field_name] = self._format_date_for_db(date_str)
                else:
                    doctor_data[field_name] = widget.get().strip()

        for field in required_fields:
            if not doctor_data.get(field):
                self.show_error("Lỗi", f"Vui lòng điền đầy đủ thông tin bắt buộc!")
                return

        success = False
        if self.form_mode == "add":
            doctor_data["MaBS"] = self.form_fields["MaBS"].get().strip()
            success = self.controller.add_doctor(doctor_data)
            message = "Thêm bác sĩ thành công!"
        else:
            success = self.controller.update_doctor(self.current_doctor_id, doctor_data)
            message = "Cập nhật thông tin bác sĩ thành công!"

        if success:
            self.show_info("Thành công", message)
            self._load_doctors()
            self._cancel_form()
        else:
            self.show_error("Lỗi", "Không thể lưu thông tin bác sĩ. Vui lòng kiểm tra lại!")

    def _cancel_form(self):
        self.notebook.select(0)

        self.form_mode = "add"
        self.current_doctor_id = None

    def _delete_doctor(self):
        selected_items = self.doctor_tree.selection()

        if not selected_items:
            self.show_error("Lỗi", "Vui lòng chọn bác sĩ để xóa!")
            return

        values = self.doctor_tree.item(selected_items[0], "values")
        doctor_id = values[0]

        confirm = self.ask_yes_no(
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa bác sĩ {values[1]} {values[2]}?"
        )

        if not confirm:
            return
        success = self.controller.delete_doctor(doctor_id)

        if success:
            self.show_info("Thành công", "Xóa bác sĩ thành công!")
            self._load_doctors()
        else:
            self.show_error(
                "Lỗi",
                "Không thể xóa bác sĩ. Bác sĩ có thể đang được sử dụng trong lịch khám!"
            )

    def on_resize(self, width, height):
        if width > 1200:
            self.doctor_tree.column("Ho", width=150)
            self.doctor_tree.column("Ten", width=120)
            self.doctor_tree.column("CMND", width=120)
            self.doctor_tree.column("ChuyenKhoa", width=200)
        elif width > 800:
            self.doctor_tree.column("Ho", width=120)
            self.doctor_tree.column("Ten", width=100)
            self.doctor_tree.column("CMND", width=100)
            self.doctor_tree.column("ChuyenKhoa", width=150)
        else:
            self.doctor_tree.column("Ho", width=100)
            self.doctor_tree.column("Ten", width=80)
            self.doctor_tree.column("CMND", width=80)
            self.doctor_tree.column("ChuyenKhoa", width=120)