import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
from pathlib import Path
from typing import Dict, Any, Callable, Optional, Union, List, Tuple

class BaseView:
    def __init__(self, parent: tk.Widget, padding: int = 10):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=padding, pady=padding)
        
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
    
        self._window_width = parent.winfo_width()
        self._window_height = parent.winfo_height()
        self.parent.bind("<Configure>", self._on_window_resize)
        
        self.images = {}
    
    def _on_window_resize(self, event):
        if (event.width != self._window_width or 
            event.height != self._window_height):
            self._window_width = event.width
            self._window_height = event.height
            if hasattr(self, 'on_resize'):
                self.on_resize(event.width, event.height)
    
    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
    
    def hide(self):
        self.frame.pack_forget()
    
    def clear(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
    
    def load_image(self, image_path: str, width: int = None, height: int = None) -> Optional[ImageTk.PhotoImage]:
        try:
            assets_dir = Path(__file__).parent.parent / 'assets'
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
    
    def create_data_table(self, parent: tk.Widget, columns: List[Tuple[str, str, int]], 
                       height: int = 10) -> ttk.Treeview:

        frame = ttk.Frame(parent)

        column_ids = [col[0] for col in columns]
        tree = ttk.Treeview(frame, columns=column_ids, show="headings", height=height)
        
        for col_id, col_text, col_width in columns:
            tree.heading(col_id, text=col_text)
            tree.column(col_id, width=col_width)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=hsb.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        
        return tree, frame
    
    def create_form_field(self, parent: tk.Widget, label_text: str, row: int, 
                       column: int = 0, widget_type=tk.Entry, **widget_kwargs) -> tk.Widget:

        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=column, padx=5, pady=5, sticky="e")
        
        widget = widget_type(parent, **widget_kwargs)
        widget.grid(row=row, column=column+1, padx=5, pady=5, sticky="ew")
        
        return widget
    
    def create_button(self, parent: tk.Widget, text: str, command: Callable, 
                   image_path: str = None, width: int = None, **kwargs) -> ttk.Button:

        button_args = {"text": text, "command": command}
        
        if width:
            button_args["width"] = width
        
        button_args.update(kwargs)
        
        if image_path:
            image = self.load_image(image_path, 20, 20)
            if image:
                button_args["image"] = image
                button_args["compound"] = tk.LEFT
        
        button = ttk.Button(parent, **button_args)
        return button
    
    def show_info(self, title: str, message: str):
        messagebox.showinfo(title, message, parent=self.parent)
    
    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message, parent=self.parent)
    
    def show_warning(self, title: str, message: str):
        messagebox.showwarning(title, message, parent=self.parent)
    
    def ask_yes_no(self, title: str, message: str) -> bool:
        return messagebox.askyesno(title, message, parent=self.parent)
    
    def validate_required_fields(self, fields: Dict[str, tk.Widget], 
                              required_keys: List[str]) -> bool:

        for key in required_keys:
            if key not in fields:
                self.show_error("Validation Error", f"Trường không tồn tại: {key}")
                return False
                
            widget = fields[key]
            value = ""
            
            if isinstance(widget, (tk.Entry, ttk.Entry)):
                value = widget.get()
            elif isinstance(widget, (tk.Text, tk.Text)):
                value = widget.get("1.0", tk.END).strip()
            elif isinstance(widget, ttk.Combobox):
                value = widget.get()
            
            if not value:
                self.show_error("Validation Error", f"Vui lòng điền đầy đủ thông tin bắt buộc!")
                widget.focus()
                return False
                
        return True