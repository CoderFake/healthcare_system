#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dashboard View - Main dashboard interface
"""

import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime, timedelta

from .base_view import BaseView
from controllers.patient_controller import PatientController
from controllers.doctor_controller import DoctorController
from controllers.schedule_controller import ScheduleController

class DashboardView(BaseView):
    """Dashboard view implementation"""
    
    def __init__(self, parent, app):
        """
        Initialize the dashboard view
        
        Args:
            parent: Parent widget
            app: Application instance
        """
        super().__init__(parent)
        self.app = app
        
        # Create controllers
        self.patient_controller = PatientController()
        self.doctor_controller = DoctorController()
        self.schedule_controller = ScheduleController()
        
        # Setup UI components
        self._create_content()
        
        # Load initial data
        self._load_dashboard_data()
    
    def _create_content(self):
        """Create the dashboard content"""
        # Clear the frame first
        self.clear()
        
        # Title
        title_frame = ttk.Frame(self.frame)
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title = ttk.Label(
            title_frame, 
            text="Hệ Thống Quản Lý Dịch Vụ Chăm Sóc Sức Khỏe", 
            style="Title.TLabel"
        )
        title.pack(side=tk.LEFT)
        
        # Welcome message with current user
        user = self.app.auth_controller.get_current_user()
        if user:
            welcome_text = f"Xin chào, {user.Hovaten}!"
        else:
            welcome_text = "Xin chào!"
            
        welcome = ttk.Label(
            title_frame, 
            text=welcome_text,
            font=("Arial", 12, "italic")
        )
        welcome.pack(side=tk.RIGHT, padx=10)
        
        # Create main content with responsive layout
        self.content_frame = ttk.Frame(self.frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.content_frame.columnconfigure(0, weight=2)
        self.content_frame.columnconfigure(1, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=1)
        
        # Left side - Today's Appointments
        self._create_todays_appointments()
        
        # Right side top - Statistics
        self._create_statistics()
        
        # Right side bottom - Quick Actions
        self._create_quick_actions()
    
    def _create_todays_appointments(self):
        """Create the today's appointments panel"""
        appointments_frame = ttk.LabelFrame(
            self.content_frame, 
            text="Lịch khám hôm nay", 
            padding=10
        )
        appointments_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)
        
        # Create appointments table
        columns = [
            ("GioKham", "Giờ", 60),
            ("TenBenhNhan", "Bệnh nhân", 150),
            ("TenBacSi", "Bác sĩ", 150),
            ("LydoKham", "Lý do khám", 200)
        ]
        
        self.today_tree, tree_frame = self.create_data_table(appointments_frame, columns, height=15)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add action buttons
        button_frame = ttk.Frame(appointments_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        view_all_button = ttk.Button(
            button_frame,
            text="Xem tất cả lịch khám",
            command=self.app.load_schedule_management,
            width=20
        )
        view_all_button.pack(side=tk.LEFT, padx=5)
        
        add_button = ttk.Button(
            button_frame,
            text="Thêm lịch khám mới",
            command=self._add_new_appointment,
            width=20
        )
        add_button.pack(side=tk.RIGHT, padx=5)
    
    def _create_statistics(self):
        """Create the statistics panel"""
        stats_frame = ttk.LabelFrame(
            self.content_frame, 
            text="Thống kê", 
            padding=10
        )
        stats_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Create stats grid
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure grid
        for i in range(2):
            stats_grid.columnconfigure(i, weight=1)
        for i in range(3):
            stats_grid.rowconfigure(i, weight=1)
        
        # Create stat boxes
        self.stat_doctors = self._create_stat_box(
            stats_grid, "Bác sĩ", "0", 0, 0,
            bg_color="#E6F3FF", icon="icons/doctor.png"
        )
        
        self.stat_patients = self._create_stat_box(
            stats_grid, "Bệnh nhân", "0", 0, 1,
            bg_color="#E6FFF3", icon="icons/patient.png"
        )
        
        self.stat_appointments_today = self._create_stat_box(
            stats_grid, "Lịch khám hôm nay", "0", 1, 0,
            bg_color="#FFF3E6", icon="icons/schedule.png"
        )
        
        self.stat_appointments_week = self._create_stat_box(
            stats_grid, "Lịch khám trong tuần", "0", 1, 1,
            bg_color="#F3E6FF", icon="icons/calendar.png"
        )
    
    def _create_stat_box(self, parent, title, value, row, col, bg_color="#FFFFFF", icon=None):
        """Create a statistics box"""
        frame = tk.Frame(parent, bg=bg_color, relief="ridge", bd=1)
        frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        
        # Icon if provided
        if icon:
            img = self.load_image(icon, 32, 32)
            if img:
                icon_label = tk.Label(frame, image=img, bg=bg_color)
                icon_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Title and value
        inner_frame = tk.Frame(frame, bg=bg_color)
        inner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = tk.Label(
            inner_frame, 
            text=title, 
            font=("Arial", 10),
            bg=bg_color
        )
        title_label.pack(side=tk.TOP, anchor="w")
        
        value_label = tk.Label(
            inner_frame, 
            text=value, 
            font=("Arial", 16, "bold"),
            bg=bg_color
        )
        value_label.pack(side=tk.TOP, anchor="w", pady=5)
        
        return value_label
    
    def _create_quick_actions(self):
        """Create the quick actions panel"""
        actions_frame = ttk.LabelFrame(
            self.content_frame, 
            text="Thao tác nhanh", 
            padding=10
        )
        actions_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        # Configure grid
        actions_inner = ttk.Frame(actions_frame)
        actions_inner.pack(fill=tk.BOTH, expand=True)
        
        for i in range(2):
            actions_inner.columnconfigure(i, weight=1)
        for i in range(2):
            actions_inner.rowconfigure(i, weight=1)
        
        # Create action buttons
        action_buttons = [
            {
                "text": "Quản lý bệnh nhân",
                "icon": "icons/patient.png",
                "command": self.app.load_patient_management,
                "row": 0,
                "column": 0
            },
            {
                "text": "Quản lý bác sĩ",
                "icon": "icons/doctor.png",
                "command": self.app.load_doctor_management,
                "row": 0,
                "column": 1
            },
            {
                "text": "Quản lý lịch khám",
                "icon": "icons/schedule.png",
                "command": self.app.load_schedule_management,
                "row": 1,
                "column": 0
            },
            {
                "text": "Đăng xuất",
                "icon": "icons/logout.png",
                "command": self.app.logout,
                "row": 1,
                "column": 1
            }
        ]
        
        for btn in action_buttons:
            self._create_action_button(
                actions_inner,
                btn["text"],
                btn["command"],
                btn["icon"],
                btn["row"],
                btn["column"]
            )
    
    def _create_action_button(self, parent, text, command, icon=None, row=0, column=0):
        """Create an action button with icon"""
        # Create a frame for the button
        frame = ttk.Frame(parent, padding=5)
        frame.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)
        
        # Load icon if provided
        img = None
        if icon:
            img = self.load_image(icon, 32, 32)
        
        # Create the button
        button = ttk.Button(
            frame,
            text=text,
            image=img,
            compound=tk.LEFT if img else tk.NONE,
            command=command
        )
        button.pack(fill=tk.BOTH, expand=True)
    
    def _load_dashboard_data(self):
        """Load data for the dashboard"""
        # Load today's appointments
        today = self._get_today()
        appointments = self.schedule_controller.get_appointments_by_date(today)
        
        # Clear existing items in the tree
        self.today_tree.delete(*self.today_tree.get_children())
        
        # Add appointments to tree, sorted by time
        sorted_appointments = sorted(appointments, key=lambda x: x.get("GioKham", ""))
        for appt in sorted_appointments:
            values = (
                appt.get("GioKham", ""),
                appt.get("TenBenhNhan", ""),
                appt.get("TenBacSi", ""),
                appt.get("LydoKham", "")
            )
            self.today_tree.insert("", "end", values=values)
        
        # Update statistics
        doctor_count = len(self.doctor_controller.get_all_doctors())
        patient_count = len(self.patient_controller.get_all_patients())
        today_count = len(appointments)
        
        # Calculate week count (appointments for the next 7 days)
        week_count = 0
        today_date = datetime.strptime(today, "%Y-%m-%d")
        for i in range(7):
            date = today_date + timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            week_count += len(self.schedule_controller.get_appointments_by_date(date_str))
        
        # Update stat boxes
        self.stat_doctors.config(text=str(doctor_count))
        self.stat_patients.config(text=str(patient_count))
        self.stat_appointments_today.config(text=str(today_count))
        self.stat_appointments_week.config(text=str(week_count))
    
    def _get_today(self):
        """Get today's date in YYYY-MM-DD format"""
        return datetime.now().strftime("%Y-%m-%d")
    
    def _add_new_appointment(self):
        """Navigate to appointment creation"""
        self.app.load_schedule_management()