#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application - Main application window and view management
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
import os
from typing import Dict, Any, Optional, Type

from controllers.auth_controller import AuthController
from .auth_view import LoginView
from .components.nav_menu import NavigationMenu

class Application:
    """Main application window and view manager"""
    
    TITLE = "QUẢN LÝ DỊCH VỤ CHĂM SÓC SỨC KHỎE"
    DEFAULT_SIZE = (1000, 600)
    MIN_SIZE = (800, 500)
    
    def __init__(self):
        """Initialize the application"""
        self.root = tk.Tk()
        self.root.title(self.TITLE)
        self.root.geometry(f"{self.DEFAULT_SIZE[0]}x{self.DEFAULT_SIZE[1]}")
        self.root.minsize(self.MIN_SIZE[0], self.MIN_SIZE[1])
        
        # Configure style
        self._configure_style()
        
        # Set up the main container frame with responsive layout
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid layout for responsiveness
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        
        # Authentication controller
        self.auth_controller = AuthController()
        
        # Dictionary to track active views
        self.views = {}
        self.current_view = None
        
        # Navigation menu (will be created after login)
        self.nav_menu = None
        
        # Content frame where views will be displayed
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        
        # Load login view by default
        self.load_login_view()
    
    def _configure_style(self):
        """Configure the application style"""
        style = ttk.Style()
        
        # Use a modern theme if available
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0')
        style.configure('TButton', font=('Arial', 10))
        
        # Configure button styles
        style.configure('TButton', padding=5, relief=tk.RAISED)
        style.map('TButton', 
                  foreground=[('pressed', 'black'), ('active', 'blue')],
                  background=[('pressed', '!disabled', '#dcdcdc'), ('active', '#ececec')])
        
        # Configure Treeview (data table)
        style.configure('Treeview', rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def start(self):
        """Start the application main loop"""
        self.root.mainloop()
    
    def load_login_view(self):
        """Load the login view"""
        # Import here to avoid circular imports
        from .auth_view import LoginView
        
        # Create login view if it doesn't exist
        if 'login' not in self.views:
            login_view = LoginView(self.content_frame, self)
            self.views['login'] = login_view
        
        # Switch to login view
        self._switch_view('login')
    
    def load_main_interface(self):
        """
        Load the main interface after successful login
        """
        # Make sure content frame is properly configured for grid
        self.content_frame.grid_remove()  # Hide temporarily
        
        # Create navigation menu if it doesn't exist
        if not self.nav_menu:
            self.nav_menu = NavigationMenu(self.main_frame, self)
            
            # Configure grid for main_frame to have two rows
            self.main_frame.rowconfigure(0, weight=0)  # Nav menu row
            self.main_frame.rowconfigure(1, weight=1)  # Content frame row
            
            # Position the menu and content frame
            self.nav_menu.frame.grid(row=0, column=0, sticky="ew")
            self.content_frame.grid(row=1, column=0, sticky="nsew")
        
        # Show navigation menu
        self.nav_menu.show()
        self.content_frame.grid()  # Show content frame again
        
        # Load dashboard view by default
        self.load_dashboard()
    
    def load_dashboard(self):
        """Load the dashboard view"""
        # Import here to avoid circular imports
        from .dashboard_view import DashboardView
        
        # Create dashboard view if it doesn't exist
        if 'dashboard' not in self.views:
            dashboard_view = DashboardView(self.content_frame, self)
            self.views['dashboard'] = dashboard_view
        
        # Switch to dashboard view
        self._switch_view('dashboard')
    
    def load_doctor_management(self):
        """Load the doctor management view"""
        # Import here to avoid circular imports
        from .doctor_view import DoctorView
        
        # Create doctor view if it doesn't exist
        if 'doctor' not in self.views:
            doctor_view = DoctorView(self.content_frame, self)
            self.views['doctor'] = doctor_view
        
        # Switch to doctor view
        self._switch_view('doctor')
    
    def load_patient_management(self):
        """Load the patient management view"""
        # Import here to avoid circular imports
        from .patient_view import PatientView
        
        # Create patient view if it doesn't exist
        if 'patient' not in self.views:
            patient_view = PatientView(self.content_frame, self)
            self.views['patient'] = patient_view
        
        # Switch to patient view
        self._switch_view('patient')
    
    def load_schedule_management(self):
        """Load the schedule management view"""
        # Import here to avoid circular imports
        from .schedule_view import ScheduleView
        
        # Create schedule view if it doesn't exist
        if 'schedule' not in self.views:
            schedule_view = ScheduleView(self.content_frame, self)
            self.views['schedule'] = schedule_view
        
        # Switch to schedule view
        self._switch_view('schedule')
    
    def _switch_view(self, view_name: str):
        """
        Switch to the specified view
        
        Args:
            view_name: Name of the view to switch to
        """
        # Hide current view if exists
        if self.current_view and self.current_view in self.views:
            self.views[self.current_view].hide()
        
        # Show new view
        if view_name in self.views:
            self.views[view_name].show()
            self.current_view = view_name
    
    def logout(self):
        """Log out the current user"""
        # Log out in the auth controller
        self.auth_controller.logout()
        
        # Hide navigation menu if exists
        if self.nav_menu:
            self.nav_menu.hide()
        
        # Reset content frame layout
        self.content_frame.grid_remove()
        
        # Reset main frame layout
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=0)
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        
        # Reset view tracking
        self.current_view = None
        
        # Go back to login view
        self.load_login_view()
    
    def exit(self):
        """Exit the application"""
        self.root.quit()