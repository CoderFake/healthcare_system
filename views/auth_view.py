import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk

from .base_view import BaseView

class LoginView(BaseView):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        self.frame.columnconfigure(0, weight=1)
        
        self._create_content()
        
        self.showing_form = False
    
    def _create_content(self):
        self.clear()
        
        self._create_splash_screen()
    
    def _create_splash_screen(self):
        container = ttk.Frame(self.frame)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        
        bg_frame = ttk.Frame(container)
        bg_frame.grid(row=0, column=0)
        
        image = self.load_image("images/healthcare.jpg", 1000, 600)
        
        if image:
            image_label = ttk.Label(bg_frame, image=image)
            image_label.pack(fill=tk.BOTH, expand=True)
            
            self.images["healthcare_bg"] = image
        else:
            fallback_label = ttk.Label(bg_frame, text="Hệ thống Quản lý Dịch vụ Chăm sóc Sức khỏe", 
                                     font=("Arial", 20), padding=200)
            fallback_label.pack(fill=tk.BOTH, expand=True)
        
        login_button = ttk.Button(
            bg_frame, 
            text="Đăng nhập hệ thống!!!",
            command=self._show_login_form
        )
        login_button.place(relx=0.95, rely=0.95, anchor="se")
        
        self.showing_form = False
    
    def _show_login_form(self):
        self.clear()
        
        container = ttk.Frame(self.frame)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        
        form_frame = ttk.Frame(container)
        form_frame.grid(row=0, column=0)
        
        title_label = ttk.Label(form_frame, text="ĐĂNG NHẬP HỆ THỐNG", 
                              font=("Arial", 16, "bold"), padding=(0, 20))
        title_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        ttk.Label(form_frame, text="USER:", font=("Arial", 12)).grid(
            row=1, column=0, padx=10, pady=10, sticky="w")
        self.username_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(form_frame, text="PASSWORD:", font=("Arial", 12)).grid(
            row=2, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = ttk.Entry(form_frame, font=("Arial", 12), show="*", width=30)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)
        
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        login_icon = self.load_image("icons/login.png", 20, 20)
        login_button = ttk.Button(
            buttons_frame, 
            text="Đăng nhập", 
            image=login_icon,
            compound=tk.LEFT,
            command=self._handle_login,
            width=15
        )
        login_button.pack(side=tk.LEFT, padx=10)
        
        exit_icon = self.load_image("icons/exit.png", 20, 20)
        exit_button = ttk.Button(
            buttons_frame, 
            text="Thoát", 
            image=exit_icon,
            compound=tk.LEFT,
            command=self.app.exit,
            width=15
        )
        exit_button.pack(side=tk.LEFT, padx=10)
        
        self.username_entry.focus_set()
        
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", lambda event: self._handle_login())
        
        self.showing_form = True
    
    def _handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.show_error("Lỗi đăng nhập", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
            return
        
        success = self.app.auth_controller.login(username, password)
        
        if success:
            self.show_info("Thông báo", "Đăng nhập thành công!")
            self.app.load_main_interface()
        else:
            self.show_error("Lỗi đăng nhập", "Tên đăng nhập hoặc mật khẩu không đúng!")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus_set()
    
    def on_resize(self, width, height):
        if not self.showing_form and width < 800:
            self._show_login_form()
        elif self.showing_form and width >= 800:
            self._create_splash_screen()
    
    def show(self):
        super().show()
        
        width = self.parent.winfo_width()
        if width >= 800 and self.showing_form:
            self._create_splash_screen()
        elif width < 800 and not self.showing_form:
            self._show_login_form()