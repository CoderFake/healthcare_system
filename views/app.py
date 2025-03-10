import tkinter as tk
from tkinter import ttk
from pathlib import Path
import os
from typing import Dict, Any, Optional, Type

from controllers.auth_controller import AuthController
from .auth_view import LoginView
from .components.nav_menu import NavigationMenu

class Application:
    TITLE = "QUẢN LÝ DỊCH VỤ CHĂM SÓC SỨC KHỎE"
    DEFAULT_SIZE = (1000, 600)
    MIN_SIZE = (800, 500)
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(self.TITLE)
        self.root.geometry(f"{self.DEFAULT_SIZE[0]}x{self.DEFAULT_SIZE[1]}")
        self.root.minsize(self.MIN_SIZE[0], self.MIN_SIZE[1])
        
        self._set_app_icon()
        
        self._configure_style()
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        
        self.auth_controller = AuthController()
        
        self.views = {}
        self.current_view = None
        
        self.nav_menu = None
        
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        
        self.load_login_view()
    
    def _set_app_icon(self):
        icon_path = Path(__file__).parent.parent / "assets" / "icons" / "healthcare_icon.ico"
        
        if icon_path.exists():
            try:
                self.root.iconbitmap(icon_path)
            except tk.TclError as e:
                print(f"Không thể tải icon ICO: {e}")
        else:
            png_icon_path = Path(__file__).parent.parent / "assets" / "icons" / "healthcare_icon.png"
            if png_icon_path.exists():
                try:
                    icon = tk.PhotoImage(file=str(png_icon_path))
                    self.root.iconphoto(True, icon)
                except Exception as e:
                    print(f"Không thể tải icon PNG: {e}")
    
    def _configure_style(self):
        style = ttk.Style()
        
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0')
        style.configure('TButton', font=('Arial', 10))
        
        style.configure('TButton', padding=5, relief=tk.RAISED)
        style.map('TButton', 
                  foreground=[('pressed', 'black'), ('active', 'blue')],
                  background=[('pressed', '!disabled', '#dcdcdc'), ('active', '#ececec')])
        
        style.configure('Treeview', rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def start(self):
        self.root.mainloop()
    
    def load_login_view(self):
        
        from .auth_view import LoginView
        
        self.main_frame.rowconfigure(0, weight=1)
        if hasattr(self.main_frame, 'rowconfigure'):
            for i in range(5):
                self.main_frame.rowconfigure(i, weight=0)
            self.main_frame.rowconfigure(0, weight=1)
        
        if hasattr(self.content_frame, 'grid_remove'):
            self.content_frame.grid_remove()
        
        if self.nav_menu:
            self.nav_menu.hide()
            if hasattr(self.nav_menu.frame, 'destroy'):
                self.nav_menu.frame.destroy()
            self.nav_menu = None
        
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        
        self.content_frame.grid()
        
        if 'login' not in self.views:
            login_view = LoginView(self.content_frame, self)
            self.views['login'] = login_view
        
        self._switch_view('login')
    
    def load_main_interface(self):
        self.content_frame.grid_remove()
        
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)
        
        if not self.nav_menu:
            self.nav_menu = NavigationMenu(self.main_frame, self)
            
            self.nav_menu.frame.grid(row=0, column=0, sticky="ew")
        else:
            self.nav_menu.frame.grid(row=0, column=0, sticky="ew")
        
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        
        self.nav_menu.show()
        
        self.content_frame.grid()
        
        self.load_dashboard()
    
    def load_dashboard(self):
        from .dashboard_view import DashboardView
        
        if 'dashboard' not in self.views:
            dashboard_view = DashboardView(self.content_frame, self)
            self.views['dashboard'] = dashboard_view
        
        self._switch_view('dashboard')
    
    def load_doctor_management(self):
        from .doctor_view import DoctorView
        
        if self.nav_menu:
            self.nav_menu.show()
        
        if 'doctor' not in self.views:
            doctor_view = DoctorView(self.content_frame, self)
            self.views['doctor'] = doctor_view
        
        self._switch_view('doctor')
    
    def load_patient_management(self):
        from .patient_view import PatientView
        
        if self.nav_menu:
            self.nav_menu.show()
        
        if 'patient' not in self.views:
            patient_view = PatientView(self.content_frame, self)
            self.views['patient'] = patient_view
        
        self._switch_view('patient')
    
    def load_schedule_management(self):
        from .schedule_view import ScheduleView
        
        if self.nav_menu:
            self.nav_menu.show()
        
        if 'schedule' not in self.views:
            schedule_view = ScheduleView(self.content_frame, self)
            self.views['schedule'] = schedule_view
        
        self._switch_view('schedule')
    
    def _switch_view(self, view_name: str):
        print(f"Switching to view: {view_name}")
        
        if self.current_view and self.current_view in self.views:
            print(f"Hiding view: {self.current_view}")
            self.views[self.current_view].hide()
        
        if view_name in self.views:
            print(f"Showing view: {view_name}")
            self.views[view_name].show()
            self.current_view = view_name
        else:
            print(f"Error: View {view_name} not found in views dictionary")
    
    def _clear_all_views(self):
        
        views_to_clear = list(self.views.keys())
        
        for view_name in views_to_clear:
            if view_name != 'login':
                if hasattr(self.views[view_name], 'frame') and hasattr(self.views[view_name].frame, 'destroy'):
                    try:
                        print(f"Destroying view: {view_name}")
                        self.views[view_name].frame.destroy()
                        del self.views[view_name]
                    except Exception as e:
                        print(f"Error destroying view {view_name}: {e}")
    
    def logout(self):
        print("Logout called")
        
        self.auth_controller.logout()
        
        prev_view = self.current_view
        
        if self.nav_menu:
            self.nav_menu.hide()
            if hasattr(self.nav_menu.frame, 'destroy'):
                try:
                    self.nav_menu.frame.destroy()
                except Exception as e:
                    print(f"Error destroying nav menu: {e}")
            self.nav_menu = None
        
        self._clear_all_views()
        
        if hasattr(self.content_frame, 'grid_remove'):
            self.content_frame.grid_remove()
        
        self.main_frame.rowconfigure(0, weight=1)
        for i in range(1, 5):
            self.main_frame.rowconfigure(i, weight=0)
        
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        
        self.current_view = None
        
        if 'login' in self.views:
            del self.views['login']
        
        self.load_login_view()
    
    def exit(self):
        self.root.quit()