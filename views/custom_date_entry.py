import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime

class CustomDateEntry(ttk.Frame):
    
    def __init__(self, parent, width=None, date_pattern='dd/mm/yyyy', **kwargs):
        super().__init__(parent)
        
        self.date_pattern = date_pattern

        today = datetime.now()
        year_now = today.year
        month_now = today.month
        day_now = today.day
        
        years = list(range(year_now, year_now - 100, -1))

        months = [(str(i).zfill(2), calendar.month_name[i]) for i in range(1, 13)]

        days = [str(i).zfill(2) for i in range(1, 32)]
        
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.X, expand=True)

        self.day_var = tk.StringVar(value=str(day_now).zfill(2))
        self.day_cb = ttk.Combobox(self.main_frame, textvariable=self.day_var, 
                                  values=days, width=3)
        self.day_cb.pack(side=tk.LEFT)
        self.day_cb.bind("<<ComboboxSelected>>", self._validate_day)

        ttk.Label(self.main_frame, text="/").pack(side=tk.LEFT)
        
        self.month_var = tk.StringVar(value=str(month_now).zfill(2))
        month_values = [m[0] for m in months]
        self.month_cb = ttk.Combobox(self.main_frame, textvariable=self.month_var, 
                                    values=month_values, width=3)
        self.month_cb.pack(side=tk.LEFT)
        self.month_cb.bind("<<ComboboxSelected>>", self._validate_day)
        
        ttk.Label(self.main_frame, text="/").pack(side=tk.LEFT)

        self.year_var = tk.StringVar(value=str(year_now))
        self.year_cb = ttk.Combobox(self.main_frame, textvariable=self.year_var, 
                                   values=years, width=6)
        self.year_cb.pack(side=tk.LEFT)
        self.year_cb.bind("<<ComboboxSelected>>", self._validate_day)
    
    def _validate_day(self, event=None):
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            day = int(self.day_var.get())
            
            _, max_days = calendar.monthrange(year, month)
            
            if day > max_days:
                self.day_var.set(str(max_days).zfill(2))
        except (ValueError, TypeError):
            pass
    
    def get(self):
        day = self.day_var.get()
        month = self.month_var.get()
        year = self.year_var.get()
        
        if self.date_pattern == 'dd/mm/yyyy':
            return f"{day}/{month}/{year}"
        elif self.date_pattern == 'yyyy-mm-dd':
            return f"{year}-{month}-{day}"
        else:
            return f"{day}/{month}/{year}"
    
    def set_date(self, date_obj):
        if isinstance(date_obj, datetime):
            self.day_var.set(str(date_obj.day).zfill(2))
            self.month_var.set(str(date_obj.month).zfill(2))
            self.year_var.set(str(date_obj.year))
    
    def configure(self, **kwargs):
        if 'state' in kwargs:
            self.day_cb.configure(state=kwargs['state'])
            self.month_cb.configure(state=kwargs['state'])
            self.year_cb.configure(state=kwargs['state'])
        
        super().configure(**kwargs)