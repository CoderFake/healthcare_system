import tkinter as tk
from tkinter import ttk
from pathlib import Path
import os
from typing import Dict, Any, List, Callable
from PIL import Image, ImageTk

class NavigationMenu:

    def __init__(self, parent, app):

        self.parent = parent
        self.app = app
        
        self.frame = ttk.Frame(parent)
        self.frame.columnconfigure(0, weight=1)
        
        self.images = {}

        self._create_menu_buttons()
    
    def _create_menu_buttons(self):

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        nav_buttons = [
            {
                'text': 'Quản lý bệnh nhân',
                'icon': 'icons/patient.png',
                'command': self.app.load_patient_management,
                'tooltip': 'Quản lý thông tin bệnh nhân'
            },
            {
                'text': 'Quản lý bác sĩ',
                'icon': 'icons/doctor.png',
                'command': self.app.load_doctor_management,
                'tooltip': 'Quản lý thông tin bác sĩ'
            },
            {
                'text': 'Quản lý lịch khám',
                'icon': 'icons/schedule.png',
                'command': self.app.load_schedule_management,
                'tooltip': 'Quản lý lịch hẹn khám'
            }
        ]
        
        for i, btn_info in enumerate(nav_buttons):
            self._create_nav_button(button_frame, btn_info, i)
        
        ttk.Separator(button_frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        logout_button = self._create_button(
            button_frame,
            'Đăng xuất',
            self.app.logout,
            'icons/logout.png',
            'Đăng xuất khỏi hệ thống'
        )
        logout_button.pack(side=tk.LEFT, padx=5)

        exit_button = self._create_button(
            button_frame,
            'Thoát',
            self.app.exit,
            'icons/exit.png',
            'Thoát khỏi ứng dụng'
        )
        exit_button.pack(side=tk.RIGHT, padx=5)
    
    def _create_nav_button(self, parent, btn_info, index):
        button = self._create_button(
            parent,
            btn_info['text'],
            btn_info['command'],
            btn_info['icon'],
            btn_info['tooltip']
        )
        button.pack(side=tk.LEFT, padx=5)
    
    def _create_button(self, parent, text, command, icon_path=None, tooltip=None):
        button_args = {
            'text': text,
            'command': command
        }

        if icon_path:
            icon = self._load_image(icon_path, 20, 20)
            if icon:
                button_args['image'] = icon
                button_args['compound'] = tk.LEFT
        
        button = ttk.Button(parent, **button_args)

        if tooltip:
            self._create_tooltip(button, tooltip)
        
        return button
    
    def _load_image(self, image_path, width=None, height=None):
        try:
            assets_dir = Path(__file__).parent.parent.parent / 'assets'
            full_path = assets_dir / image_path
            
            if not full_path.exists():
                full_path = Path(image_path)
            
            if not full_path.exists():
                print(f"Image not found: {image_path}")
                return None
            
            image = Image.open(full_path)
            
            if width and height:
                image = image.resize((width, height), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            image_key = f"{image_path}_{width}_{height}"
            self.images[image_key] = photo
            
            return photo
            
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None
    
    def _create_tooltip(self, widget, text):

        tooltip = ToolTip(widget, text)
    
    def show(self):
        self.frame.grid(row=0, column=0, sticky="ew")
    
    def hide(self):
        self.frame.grid_remove()
    
    def update_menu_state(self):
        pass


class ToolTip:
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True) 
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1,
            font=("Arial", "9", "normal"), padx=3, pady=2
        )
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None